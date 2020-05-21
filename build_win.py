from pathlib import Path
import sys
import os
import urllib.request
import tarfile
import shutil
from setuptools import sandbox
import subprocess


TAGLIB_VERSION = '1.11.1'
taglib_release = f'https://github.com/taglib/taglib/releases/download/v{TAGLIB_VERSION}/taglib-{TAGLIB_VERSION}.tar.gz'
cmake = r'c:\Program Files (x86)\Microsoft Visual Studio\\2019\BuildTools\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe'
build_config = 'Release'

x64 = sys.maxsize > 2**32
arch = "x64" if x64 else "x32"
sys.path.append('src')

repository_root = Path(__file__).resolve().parent

def make_build_dir():    
    dirname = f'taglib-build-{arch}'
    path = repository_root / dirname
    path.mkdir(parents=True, exist_ok=True)
    return path

build_dir = make_build_dir()

taglib_root = build_dir/ f'taglib-{TAGLIB_VERSION}'
taglib_out_dirname = f'install-{arch}'
taglib_out = build_dir/ taglib_out_dirname

def taglib_download():
    target = build_dir / f'taglib-{TAGLIB_VERSION}.tar.gz'
    if not target.exists():
        response = urllib.request.urlopen(taglib_release)
        data = response.read()
        target.write_bytes(data)
    return target
 

def taglib_prepare():
    if not taglib_root.exists():
        taglib_archive = taglib_download()
        tar = tarfile.open(taglib_archive)
        tar.extractall(build_dir)
    taglib_clean_cmake()

def taglib_clean_cmake():
    cache = taglib_root / 'CMakeCache.txt'
    if cache.exists():
        cache.unlink()
        shutil.rmtree(taglib_root / 'CMakeFiles', ignore_errors=True)
 
def taglib_gen_vs_projects():
    print("*** calling cmake generate ...")
    cmake_arch = 'x64' if x64 else "Win32"
    install_prefix = f'-DCMAKE_INSTALL_PREFIX=../{taglib_out_dirname}'
    subprocess.run(
       [cmake ,'-G',  'Visual Studio 16 2019', '-A', cmake_arch, install_prefix, '.'],
       cwd=taglib_root, check=True
    )

def taglib_build(clean_first: bool = True):
    print("*** calling cmake build ...")
    subprocess.run(
        [cmake, '--build', '.', '--config', build_config] + (['--clean-first'] if clean_first else []),
        cwd=taglib_root, check=True
    )
    print("*** calling cmake install ...")
    subprocess.run(
        [cmake, '--install', '.', '--config', build_config],
        cwd=taglib_root, check=True
    )

def taglib_ensure_build():
    if taglib_out.exists():
        return
    print(f"*** building taglib on {arch}...")
    taglib_prepare()
    taglib_gen_vs_projects()
    taglib_build()

def pytaglib_build():
    print("*** building pytaglib ...")
    os.environ['TAGLIB_HOME'] = str(taglib_out)
    os.environ['PYTAGLIB_CYTHONIZE'] = '1'
    sandbox.run_setup('setup.py', ['build_ext', '--inplace'])
    
    import pytest
    pytest.main()
    sandbox.run_setup('setup.py', ['build', 'bdist_wheel'])
    

def script():
    taglib_ensure_build()
    pytaglib_build()


if __name__ == '__main__':
    script()
