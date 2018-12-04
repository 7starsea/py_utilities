# -*- coding: utf-8 -*-
import os.path
import shutil
import subprocess
import glob
import sys


def ensure_dir_exists(dirname):
    os.path.isdir(dirname) or os.makedirs(dirname)


def internal_run_cmd(cmd, verbose, cwd=None):
    if verbose:
        print('>>> Running cmd:%s' % cmd)    
    p1 = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=cwd)
    if 0 != p1.returncode:
        import chardet
        the_encoding = chardet.detect(p1.stderr)['encoding']
        print(p1.stderr.decode(the_encoding).strip())
        return False
    return True        


def merge_static_libs_win(executable, target_lib_file, libs, verbose=False):
    cwd = os.path.dirname(executable)
    exe = os.path.basename(executable)    
    target_lib_file = os.path.abspath(target_lib_file)
    libs = list(map(lambda lib: os.path.abspath(lib), libs))
    cmd = '%s /OUT:%s %s' % (exe, target_lib_file, ' '.join(libs))
    internal_run_cmd(cmd, verbose, cwd=cwd)

    
def merge_static_libs_macos(target_lib_file, libs, verbose=False):
    cmd = '/usr/bin/libtool -static -o %s %s' % (target_lib_file, ' '.join(libs))
    internal_run_cmd(cmd, verbose)
        
        
def merge_static_libs_linux(target_lib_file, libs, verbose=False):
    cmake_ar = 'ar'
    
    target_lib = os.path.basename(target_lib_file)
    working_dir = 'TMP_FOLDER4%s' % target_lib
    ensure_dir_exists(working_dir)
    for libname in libs:
        assert os.path.isfile(libname)
        libbasename = os.path.basename(libname)

        cwd = os.path.join(working_dir, libbasename)
        ensure_dir_exists(cwd)

        cmd = '%s -x %s' % (cmake_ar, os.path.abspath(libname))
        internal_run_cmd(cmd, verbose, cwd=cwd)

    current_dir = os.getcwd()
    os.chdir(working_dir)
    object_files = glob.glob('**/*.o', recursive=True)
    os.chdir(current_dir)

    cmd = '%s -r %s %s' % (cmake_ar, target_lib, ' '.join(object_files))
    if internal_run_cmd(cmd, verbose, cwd=working_dir):
        cmd = '%s -s %s' % (cmake_ar, target_lib)
        
        internal_run_cmd(cmd, verbose, cwd=working_dir)

    shutil.copy(os.path.join(working_dir, target_lib), target_lib_file)
    shutil.rmtree(working_dir)
    
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Merge Static libs into one bigger static lib')
    parser.add_argument('-v', '--verbose', action='store_true', help='print verbose information.')
    parser.add_argument('-e', '--executable', help='merge executable program (used in window)')
    parser.add_argument("target_lib", help='target-lib')
    parser.add_argument("libs", nargs='+', help='static-lib static-lib ...')
    opts = parser.parse_args()

    assert isinstance(opts.libs, list)
    if len(opts.libs) < 1:
        print('We need at least one static lib.')
        exit(-1)

    if opts.verbose:
        print('target-lib: %s static-libs: %s' % (opts.target_lib,','.join(opts.libs)))
    
    sys_platform = sys.platform.lower()
    if sys_platform.startswith('win'):
        if opts.executable and os.path.isfile(opts.executable): 
            # test_exe = "F:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/lib.exe"
            # merge_static_libs_win(test_exe, opts.target_lib, opts.libs, opts.verbose)
            merge_static_libs_win(opts.executable, opts.target_lib, opts.libs, opts.verbose)
        else:
            print(">>> Error: please provide a valid (merge) executable program, e.g. lib.exe (windows).")
    elif sys_platform.startswith('darwin') and os.path.isfile('/usr/bin/libtool'):
        # Use OSX's libtool to merge archives (ihandles universal binaries properly)        
        merge_static_libs_macos(opts.target_lib, opts.libs, opts.verbose)
    else:
        # Generic Unix, Cygwin or MinGW. In post-build step, call
        # script, that extracts objects from archives with "ar x" 
        # and repacks them with "ar r"        
        merge_static_libs_linux(opts.target_lib, opts.libs, opts.verbose)