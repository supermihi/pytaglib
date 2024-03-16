import hashlib
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from argparse import ArgumentParser
from pathlib import Path

system = platform.system()
here = Path(__file__).resolve().parent

taglib_version = "2.0"
taglib_release = f"https://github.com/taglib/taglib/archive/refs/tags/v{taglib_version}.tar.gz"
taglib_sha256sum = "e36ea877a6370810b97d84cf8f72b1e4ed205149ab3ac8232d44c850f38a2859"

utfcpp_version = "4.0.5"
utfcpp_release = f"https://github.com/nemtrif/utfcpp/archive/refs/tags/v{utfcpp_version}.tar.gz"

sys_identifier = f"{system}-{platform.machine()}-{sys.implementation.name}-{platform.python_version()}"

class Configuration:
    def __init__(self):
        self.build_base = here / "build"
        self.build_path = self.build_base / sys_identifier
        self.tl_install_dir = self.build_path / "taglib"
        self.clean = False

    @property
    def tl_download_dest(self):
        return self.build_base / f"taglib-{taglib_version}.tar.gz"

    @property
    def utfcpp_download_dest(self):
        return self.build_base / f"utfcpp-{utfcpp_version}.tar.gz"

    @property
    def tl_extract_dir(self):
        return self.build_path / f"taglib-{taglib_version}"

    @property
    def utfcpp_extract_dir(self):
        return self.build_path / f"utfcpp-{utfcpp_version}"

    @property
    def utfcpp_include_dir(self):
        return self.utfcpp_extract_dir / "source"


def _download_file(url: str, target: Path, sha256sum: str = None):
    if target.exists():
        print("skipping download, file exists")
        return
    print(f"downloading {url} ...")
    response = urllib.request.urlopen(url)
    data = response.read()
    target.parent.mkdir(exist_ok=True, parents=True)
    target.write_bytes(data)
    if sha256sum is None:
        return
    the_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    if the_hash != taglib_sha256sum:
        error = f'checksum of downloaded file ({the_hash}) does not match expected hash ({taglib_sha256sum})'
        raise RuntimeError(error)


def download(config: Configuration):
    _download_file(taglib_release, config.tl_download_dest, taglib_sha256sum)
    _download_file(utfcpp_release, config.utfcpp_download_dest)


def _extract_tar(archive: Path, target: Path):
    if target.exists():
        print(f"extracted directory {target} found; skipping tar")
        return
    print(f"extracting {archive} ...")
    tar = tarfile.open(archive)
    tar.extractall(target.parent)


def extract(config: Configuration):
    _extract_tar(config.tl_download_dest, config.tl_extract_dir)
    _extract_tar(config.utfcpp_download_dest, config.utfcpp_extract_dir)


def copy_utfcpp(config: Configuration):
    target = config.tl_extract_dir / "3rdparty" / "utfcpp"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(config.utfcpp_extract_dir, target)


def cmake_clean(config: Configuration):
    if not config.clean:
        return
    print("removing previous cmake cache ...")
    cache = config.tl_extract_dir / "CMakeCache.txt"
    if cache.exists():
        cache.unlink()
        shutil.rmtree(config.tl_extract_dir / "CMakeFiles", ignore_errors=True)


def call_cmake(config, *args):
    return subprocess.run(
        ["cmake", *[a for a in args if a is not None]],
        cwd=config.tl_extract_dir,
        check=True,
    )


def cmake_config(config: Configuration):
    print("running cmake ...")
    args = ["-DWITH_ZLIB=OFF"]  # todo fix building wheels with zlib support
    if system == "Windows":
        args += ["-A", "x64"]
    elif system == "Linux":
        args.append("-DCMAKE_POSITION_INDEPENDENT_CODE=ON")
    args.append(f"-DCMAKE_INSTALL_PREFIX={config.tl_install_dir}")
    args.append(f"-DCMAKE_CXX_FLAGS=-I{config.tl_extract_dir / '3rdparty' / 'utfcpp' / 'source'}")
    args.append(".")
    config.tl_install_dir.mkdir(exist_ok=True, parents=True)
    call_cmake(config, *args)


def cmake_build(config: Configuration):
    print("building taglib ...")
    build_configuration = "Release"
    call_cmake(
        config,
        "--build",
        ".",
        "--config",
        build_configuration,
        "--clean-first" if config.clean else None,
    )
    print("installing cmake ...")
    call_cmake(config, "--install", ".", "--config", build_configuration)


def to_abs_path(str_path: str) -> Path:
    path = Path(str_path)
    if not path.is_absolute():
        path = here / path
    return path


def parse_args() -> Configuration:
    parser = ArgumentParser()
    config = Configuration()
    parser.add_argument(
        "--install-dest",
        help="destination directory for taglib",
        type=Path,
        default=config.tl_install_dir,
    )
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    config.tl_install_dir = to_abs_path(args.install_dest)
    config.clean = args.clean
    return config


def run():
    print(f"building taglib on {sys_identifier} ...")
    config = parse_args()
    tag_lib = (
            config.tl_install_dir
            / "lib"
            / ("tag.lib" if system == "Windows" else "libtag.a")
    )
    if tag_lib.exists() and not config.clean:
        print("installed TagLib found, exiting")
        return
    download(config)
    extract(config)
    copy_utfcpp(config)
    cmake_clean(config)
    cmake_config(config)
    cmake_build(config)


if __name__ == "__main__":
    run()
