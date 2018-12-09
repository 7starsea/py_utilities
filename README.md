python_utilities (py-utilities)
=================
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

We provide some usefull python utilities.

All code are tested under python3.6.

Although we try to be python2 and python3 compatible, but some may failed under python2, if you find some error under python2, please let me know.

# What is New
* add rtn_opt_dates.py for easily generateing a list of dates
* add linear_regression.py, with extraordinary speed improvement over scikit-learn/linear_model for special use cases. We intentionally implement split-conquer method.

# How to use (examples)
* python ensure_exists_screen.py test_screen_name
* python update_json_file.py --update-type update_all examples/test-old.json examples/test.json
* python update_json_file.py --update-type keep_exist examples/test-old.json examples/test.json
* python update_json_file.py --update-type overwrite_exist examples/test-old.json examples/test.json
* python CppGenerator/CPPCSVGenerator.py examples/struct.h

// We internally use [RapidJson](https://github.com/Tencent/rapidjson/) for cpp parsing Json file<br />
* python CppGenerator/CPPJsonGenerator.py examples/struct.h

// merge several static libs into a big one (cross-platform, tested on Window, Linux(Ubuntu), MacOS) 

// see examples/merge-static-libs
* python merge_static_libs.py libboobar_merged.a libboo.a libbar.a

