from pathlib import Path
import sys
import urllib.request
import tarfile
import shutil
import subprocess

taglib_version = '1.11.1'
taglib_release = f'https://github.com/taglib/taglib/releases/download/v1.11.1/taglib-{taglib_version}.tar.gz'
cmake = 'c:\Program Files (x86)\Microsoft Visual Studio\\2019\BuildTools\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\\bin\cmake.exe'
repo = Path(__file__).resolve().parent
def build_dir():
    arch = "x64" if sys.maxsize > 2**32 else "x32"
    dirname = f'build_win_{sys.implementation.name}-{sys.version_info.major}.{sys.version_info.minor}-{arch}'
    path = repo / dirname
    path.mkdir(parents=True, exist_ok=True)
    return path


def download_taglib():
    target = build_dir() / 'taglib-release.tar.gz'
    if not target.exists():
        response = urllib.request.urlopen(taglib_release)
        data = response.read()
        target.write_bytes(data)
    return target
 

def extract_taglib():
    target = build_dir() / f'taglib-{taglib_version}'
    if not target.exists():
        taglib_archive = download_taglib()
        tar = tarfile.open(taglib_archive)
        tar.extractall(build_dir())
    cache = target / 'CMakeCache.txt'
    if cache.exists():
        cache.unlink()
        shutil.rmtree(target / 'CMakeFiles', ignore_errors=True)

    return target
 
def generate_vs_projects(taglib_dir: Path):
    subprocess.run(
       [cmake , '-G',  'Visual Studio 16 2019', '-A', 'x64', '-DCMAKE_INSTALL_PREFIX=../taglib-build'],
       cwd=taglib_dir, check=True
    )
    subprocess.run(
        [cmake, '--build', '.'],
        cwd=taglib_dir, check=True
    )
    subprocess.run(
        [cmake, '--install', '.', '--config', 'Release']
    )
def script():
    tl_dir = extract_taglib()
    generate_vs_projects(tl_dir)


if __name__ == '__main__':
    script()
