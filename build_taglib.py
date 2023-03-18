from pathlib import Path
import platform
import sys
import urllib.request
import tarfile
import shutil
import subprocess
from dataclasses import dataclass
from argparse import ArgumentParser
import hashlib


taglib_version = "1.13"
taglib_release = f"https://github.com/taglib/taglib/releases/download/v{taglib_version}/taglib-{taglib_version}.tar.gz"
taglib_sha256sum = "58f08b4db3dc31ed152c04896ee9172d22052bc7ef12888028c01d8b1d60ade0"
build_config = "Release"

is_x64 = sys.maxsize > 2**32
arch = "x64" if is_x64 else "x32"
system = platform.system()
python_version = platform.python_version()


here = Path(__file__).resolve().parent

default_taglib_path = here / "build" / "taglib" / f"{system}-{arch}-py{python_version}"


@dataclass
class Configuration:
    tl_install_dir: Path = default_taglib_path
    build_path: Path = here / "build"
    clean: bool = True

    @property
    def tl_download_dest(self):
        return self.build_path / f"taglib-{taglib_version}.tar.gz"

    @property
    def tl_extract_dir(self):
        return self.build_path / f"taglib-{taglib_version}"


def download(config: Configuration):
    target = config.tl_download_dest
    if target.exists():
        print("skipping download, file exists")
    else:
        print(f"downloading taglib {taglib_version} ...")
        response = urllib.request.urlopen(taglib_release)
        data = response.read()
        target.parent.mkdir(exist_ok=True, parents=True)
        target.write_bytes(data)
    the_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    assert the_hash == taglib_sha256sum


def extract(config: Configuration):
    if config.tl_extract_dir.exists():
        print("extracted taglib found. Skipping tar")
    else:
        print("extracting tarball")
        tar = tarfile.open(config.tl_download_dest)
        tar.extractall(config.tl_extract_dir.parent)


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
    args = []
    args.append("-DWITH_ZLIB=OFF")
    if system == "Windows":
        cmake_arch = "x64" if is_x64 else "Win32"
        args += ["-A", cmake_arch]
    elif system == "Linux":
        args.append("-DCMAKE_POSITION_INDEPENDENT_CODE=ON")
    args.append(f"-DCMAKE_INSTALL_PREFIX={config.tl_install_dir}")
    args.append(".")
    config.tl_install_dir.mkdir(exist_ok=True, parents=True)
    call_cmake(config, *args)


def cmake_build(config: Configuration):
    print("building ...")
    call_cmake(
        config,
        "--build",
        ".",
        "--config",
        build_config,
        "--clean-first" if config.clean else None,
    )
    print("installing ...")
    call_cmake(config, "--install", ".", "--config", build_config)


def make_path(str_path: str) -> Path:
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
    args = parser.parse_args()
    config.tl_install_dir = make_path(args.install_dest)
    return config


def run():
    print(f"building taglib on {system}, arch {arch}, for python {python_version} ...")
    config = parse_args()
    tag_lib = config.tl_install_dir / "lib" / "tag.lib"
    if tag_lib.exists():
        print("installed TagLib found, exiting")
        return
    download(config)
    extract(config)
    cmake_clean(config)
    cmake_config(config)
    cmake_build(config)


if __name__ == "__main__":
    run()
