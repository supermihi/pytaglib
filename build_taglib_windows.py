from pathlib import Path
import sys
import urllib.request
import tarfile
import shutil
import subprocess
from dataclasses import dataclass
from argparse import ArgumentParser
import hashlib


taglib_version = '1.12'
taglib_release = f'https://github.com/taglib/taglib/releases/download/v{taglib_version}/taglib-{taglib_version}.tar.gz'
taglib_sha256sum = '7fccd07669a523b07a15bd24c8da1bbb92206cb19e9366c3692af3d79253b703'
build_config = 'Release'

is_x64 = sys.maxsize > 2**32
arch = "x64" if is_x64 else "x32"


here = Path(__file__).resolve().parent

@dataclass
class Configuration:
    tl_install_dir: Path = here / 'build' / 'taglib-install'
    tl_download_dest: Path = here / 'build' / f'taglib-{taglib_version}.tar.gz'
    tl_extract_dir: Path = here / 'build' / f'taglib-{taglib_version}'

def download(config: Configuration):
    target = config.tl_download_dest
    if not target.exists():
        response = urllib.request.urlopen(taglib_release)
        data = response.read()
        target.parent.mkdir(exist_ok=True,parents=True)
        target.write_bytes(data)
    the_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    assert the_hash == taglib_sha256sum
 

def extract_and_clean(config: Configuration):
    if not config.tl_extract_dir.exists():
        tar = tarfile.open(config.tl_download_dest)
        tar.extractall(config.tl_extract_dir.parent)
    taglib_clean_cmake(config)

def taglib_clean_cmake(config: Configuration):
    cache = config.tl_extract_dir / 'CMakeCache.txt'
    if cache.exists():
        cache.unlink()
        shutil.rmtree(config.tl_extract_dir / 'CMakeFiles', ignore_errors=True)
 
def generate_vs_project(config: Configuration):
    print("*** calling cmake generate ...")
    cmake_arch = 'x64' if is_x64 else "Win32"
    install_prefix = f'-DCMAKE_INSTALL_PREFIX={config.tl_install_dir}'
    config.tl_install_dir.mkdir(exist_ok=True, parents=True)
    subprocess.run(
       ['cmake', '-A', cmake_arch, install_prefix, '.'],
       cwd=config.tl_extract_dir, check=True
    )

def build(config: Configuration, clean_first: bool = True):
    print("*** calling cmake build ...")
    subprocess.run(
        ['cmake', '--build', '.', '--config', build_config] + (['--clean-first'] if clean_first else []),
        cwd=config.tl_extract_dir, check=True
    )
    print("*** calling cmake install ...")
    subprocess.run(
        ['cmake', '--install', '.', '--config', build_config],
        cwd=config.tl_extract_dir, check=True
    )

def make_path(str_path: str) -> Path:
    path = Path(str_path)
    if not path.is_absolute():
        path = here / path
    return path

def parse_args() -> Configuration:
    parser = ArgumentParser()
    parser.add_argument('--install-dest', help='destination directory for taglib', default=f'taglib-{arch}')
    args = parser.parse_args()
    return Configuration(tl_install_dir=make_path(args.install_dest))

def run():
    print(f"*** building taglib on {arch}...")
    config = parse_args()
    print(config)
    download(config)
    extract_and_clean(config)
    generate_vs_project(config)
    build(config)
    

if __name__ == '__main__':
    run()
