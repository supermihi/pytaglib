import hashlib
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path

taglib_version = "2.0.1"
taglib_url = f"https://github.com/taglib/taglib/archive/refs/tags/v{taglib_version}.tar.gz"
taglib_sha256sum = "08c0a27b96aa5c4e23060fe0b6f93102ee9091a9385257b9d0ddcf467de0d925"

utfcpp_version = "4.0.5"
utfcpp_url = f"https://github.com/nemtrif/utfcpp/archive/refs/tags/v{utfcpp_version}.tar.gz"

root = Path(__file__).resolve().parent

system = platform.system()


def run_script():
    config = get_config()

    _download(taglib_url, config.taglib_tarball, taglib_sha256sum)
    _download(utfcpp_url, config.utfcpp_tarball)

    if config.force or not config.taglib_extract_dir.exists():
        _del_if_exists(config.taglib_extract_dir)
        _del_if_exists(config.utfcpp_extract_dir)
        _extract(config.taglib_tarball, config.taglib_extract_dir)
        _extract(config.utfcpp_tarball, config.utfcpp_extract_dir)
        shutil.copytree(config.utfcpp_extract_dir, config.taglib_extract_dir / "3rdparty" / "utfcpp",
                        dirs_exist_ok=True)

    if config.force or not config.taglib_install_dir.exists():
        _del_if_exists(config.taglib_install_dir)
        cmake_config(config.taglib_extract_dir, config.taglib_install_dir)
        cmake_build(config.taglib_extract_dir)

    _del_if_exists(config.target_dir)
    shutil.copytree(config.taglib_install_dir, config.target_dir)


@dataclass
class Configuration:
    target_dir: Path
    cache_dir: Path
    force: bool
    platform_id: str

    @property
    def taglib_tarball(self):
        return self.cache_dir / f"taglib-{taglib_version}.tar.gz"

    @property
    def utfcpp_tarball(self):
        return self.cache_dir / f"utfcpp-{utfcpp_version}.tar.gz"

    @property
    def platform_dir(self):
        return self.cache_dir / self.platform_id

    @property
    def taglib_extract_dir(self):
        return self.platform_dir / f"taglib-{taglib_version}"

    @property
    def utfcpp_extract_dir(self):
        return self.platform_dir / f"utfcpp-{utfcpp_version}"

    @property
    def taglib_install_dir(self):
        return self.platform_dir / "taglib-install"


def get_config() -> Configuration:
    parser = ArgumentParser(description="helper to download and build C++ TagLib")
    parser.add_argument(
        "--target",
        help="target directory for TagLib (binaries and headers)",
        type=Path,
        default=root / "lib" / "taglib-cpp",
    )
    parser.add_argument(
        "--cache",
        help="temporary directory for downloads and builds; suitable to be cached in CI",
        type=Path,
        default=root / "build" / "cache",
    )
    parser.add_argument("--force", action="store_true", help="fore clean build even if output already exists")
    args = parser.parse_args()
    return Configuration(target_dir=args.target.resolve(), cache_dir=args.cache.resolve(), force=args.force,
                         platform_id=get_platform_id())


def _download(url: str, target: Path, sha256sum: str = None):
    print(f"downloading {url} ...")
    if target.exists():
        print("skipping download, file exists")
        return
    response = urllib.request.urlopen(url)
    data = response.read()
    target.parent.mkdir(exist_ok=True, parents=True)
    target.write_bytes(data)
    print("download complete")
    if sha256sum is None:
        return
    the_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    if the_hash != taglib_sha256sum:
        error = f'checksum of downloaded file ({the_hash}) does not match expected hash ({taglib_sha256sum})'
        raise RuntimeError(error)


def get_platform_id():
    """Tries to generate a string that is unique for the C compiler configuration used to build
    Python extensions.

    Compiler potentially depends on:
    - OS
    - architecture
    - Python implementation (CPython, PyPy)
    - Python version (major/minor)
    - C library type (uclib for musllinux)

    In cibuildwheel, the AUDITWHEEL_PLAT environment variable is used for all of these except
    Python version and implementation.
    - """
    platform_identifier = os.environ.get('AUDITWHEEL_PLAT', f"{system}-{platform.machine()}")
    python_identifier = f"{sys.implementation.name}-{sys.version_info[0]}.{sys.version_info[1]}"
    return f"{platform_identifier}-{python_identifier}"


def _extract(archive: Path, target: Path):
    """Extracts `archive` into `target`.
    """
    print(f"extracting {archive} to {target} ...")
    tar = tarfile.open(archive)
    tar.extractall(target.parent)


def _del_if_exists(dir: Path):
    if dir.exists():
        shutil.rmtree(dir)


def _cmake(cwd: Path, *args):
    print(f"running cmake {' '.join(args)}")
    return subprocess.run(["cmake", *args], cwd=cwd, check=True)


def cmake_config(source_dir: Path, install_dir: Path):
    print("running cmake ...")
    args = ["-DWITH_ZLIB=OFF"]  # todo fix building wheels with zlib support
    if system == "Windows":
        args += ["-A", "x64"]
    elif system == "Linux":
        args.append("-DCMAKE_POSITION_INDEPENDENT_CODE=ON")
    args.append("-DBUILD_TESTING=OFF")
    args.append(f"-DCMAKE_INSTALL_PREFIX={install_dir}")
    args.append(f"-DCMAKE_CXX_FLAGS=-I{source_dir / '3rdparty' / 'utfcpp' / 'source'}")
    args.append(".")
    install_dir.mkdir(exist_ok=True, parents=True)
    _cmake(source_dir, *args)


def cmake_build(source_dir: Path):
    print("building taglib ...")
    build_configuration = "Release"
    _cmake(
        source_dir,
        "--build",
        ".",
        "--config",
        build_configuration
    )
    print("installing cmake ...")
    _cmake(source_dir, "--install", ".", "--config", build_configuration)


if __name__ == "__main__":
    run_script()
