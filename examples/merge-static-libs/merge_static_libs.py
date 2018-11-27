# -*- coding: utf-8 -*-
import os.path
import shutil
import subprocess
import glob


def ensure_dir_exists(dirname):
    os.path.isdir(dirname) or os.mkdir(dirname)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Merge Static libs into one bigger static lib')
    parser.add_argument('-v', '--verbose', action='store_true', help='print verbose information.')
    parser.add_argument("target_lib", help='target-lib')
    parser.add_argument("libs", nargs='+', help='static-lib static-lib ...')
    opts = parser.parse_args()

    assert isinstance(opts.libs, list)
    if len(opts.libs) < 1:
        print('We need at least one static lib.')
        exit(-1)

    cmake_ar = 'ar'
    if opts.verbose:
        print('target-lib: %s static-libs: %s' % (opts.target_lib,','.join(opts.libs)))

    target_lib = os.path.basename(opts.target_lib)
    working_dir = 'TMP_FOLDER4%s' % target_lib
    ensure_dir_exists(working_dir)
    for libname in opts.libs:
        assert os.path.isfile(libname)
        libbasename = os.path.basename(libname)

        cwd = os.path.join(working_dir, libbasename)
        ensure_dir_exists(cwd)

        cmd = '%s -x %s' % (cmake_ar, os.path.abspath(libname))
        if opts.verbose:
            print('>>> Running cmd:%s' % cmd)
        p1 = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=cwd)
        if 0 != p1.returncode:
            print(p1.stderr)

    current_dir = os.getcwd()
    os.chdir(working_dir)
    object_files = glob.glob('**/*.o', recursive=True)
    os.chdir(current_dir)

    cmd = '%s -r %s %s' % (cmake_ar, target_lib, ' '.join(object_files))
    if opts.verbose:
        print('>>> Running cmd:%s' % cmd)
    p1 = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=working_dir)
    if 0 != p1.returncode:
        print(p1.stderr)
    else:
        cmd = '%s -s %s' % (cmake_ar, target_lib)
        if opts.verbose:
            print('>>> Running cmd:%s' % cmd)
        p1 = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=working_dir)
        if 0 != p1.returncode:
            print(p1.stderr)

    shutil.copy(os.path.join(working_dir, target_lib), opts.target_lib)
    shutil.rmtree(working_dir)

