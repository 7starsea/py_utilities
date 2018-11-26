# -*- coding: utf-8 -*-
import os.path
import shutil
import subprocess
import glob


def ensure_dir_exists(dirname):
    os.path.isdir(dirname) or os.mkdir(dirname)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Merge Static libs')
    parser.add_argument('-v', '--verbose', action='store_true', help='print verbose information.')
    parser.add_argument("libs", nargs='+', help='target static-lib static-lib ...')
    opts = parser.parse_args()

    assert isinstance(opts.libs, list)
    if len(opts.libs) < 2:
        print('We need a target-name and at least one static lib')
        exit(-1)

    cmake_ar = 'ar'
    if opts.verbose:
        print(opts.libs)

    target_lib = os.path.basename(opts.libs[0])
    opts.libs.pop(0)
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
    # print(object_files)
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

    shutil.copy(os.path.join(working_dir, target_lib), opts.libs[0])
    shutil.rmtree(working_dir)

