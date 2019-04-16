# -*- coding: utf-8 -*-
from sys import platform as sys_platform
import os.path
from shutil import copyfile
import re
import datetime
import subprocess
import functools
from CPPGeneratorBase import CPPGeneratorBase, ensure_exists_dir


internal_csv_reader_map = dict({
    "int": ("get<int>", "is_int"),
    "short": ("get<int>", "is_int"),
    "enum": ("get<int>", "is_int"),
    "unsigned int": ("get<int>", "is_int"),
    "unsigned short": ("get<int>", "is_int"),
    "long": ("get<long>", "is_int"),
    "unsigned long": ("get<unsigned long>", "is_int"),
    "long long": ("get<long long>", "is_int"),
    "double": ("get<double>", "is_num"),
    "long double": ("get<double>", "is_num"),
    "float": ("get<double>", "is_num"),
    "bool": ("get<int>", "is_int"),
    "char": ("get<std::string>", "is_str"),
    "str": ("get<std::string>", "is_str"),
    "unsigned char": ("get<std::string>", "is_str"),
})


def internal_csv_reader(cpp_key, py_key, raw_type):
    cpp = ''
    if raw_type in ['char', 'unsigned char', 'str']:
        if raw_type == 'unsigned char':
            cpp = 'data.%s = row["%s"].get<std::string>()[0];' % (cpp_key, py_key)
        else:
            cpp = 'strncpy(data.%s, row["%s"].get<std::string>().c_str(), sizeof(data.%s)-1);' % (cpp_key, py_key, cpp_key)

            check_str_size_fmt = """
        if(row["%s"].get().size() <= sizeof(data.%s)-1){
            %s
        }else{
            std::cerr<<">>> String is too bigger for char %s[] with py_key %s."<<std::endl;
            flag = false;
        }
"""
            cpp = check_str_size_fmt % (py_key, cpp_key, cpp, cpp_key, py_key)

    elif raw_type in internal_csv_reader_map:
        methods = internal_csv_reader_map[raw_type]
        cpp = 'data.%s = (%s)(row["%s"].%s());' % (cpp_key, raw_type, py_key, methods[0])
    else:
        print('Unknow csv reader type:', raw_type)
        exit(-1)
    return cpp


def _csv_writer_header(keys, struct_id, get_property=None):
    source = "template<>\nstd::string CSVWriteRtnHead<%s>()\n{\n\tstd::string header;\n" % struct_id
    num = len(keys)
    for j in range(num):
        key = keys[j]
        title = key[1]
        # title = key[1].title().replace("_", "").replace("-", "")

        is_array = False
        if get_property and callable(get_property):
            if key[2] != 'char' and 1 == get_property(key[1], 'array'):
                is_array = True
        sep = 'CSV_SPLITTER_SYMBOL' if j != num - 1 else "'\\n'"
        if is_array:
            array_size = int(get_property(key[1], 'array_size'))
            assert array_size > 0
            for i in range(array_size):
                if j == num - 1 and i == array_size - 1:
                    sep = "'\\n';"
                source += "\theader.append(\"%s%s\");\theader.push_back(%s);\n" % (title, i + 1, sep)
        else:
            source += "\theader.append(\"%s\");\theader.push_back(%s);\n" % (title, sep)

    source += "\n\treturn header;\n}\n"

    source += "template<>\nvoid Internal_CSVWriteHead<%s>(std::ostream &ofs)" % struct_id
    source += "\n{\n\tofs << CSVWriteRtnHead<%s>();" % struct_id
    source += "\n}\n"
    return source


def _csv_writer_content(keys, struct_id, get_property=None):
    source = "template<>\nvoid Internal_CSVWriteContent<%s>( const %s & data, std::ostream &ofs)" % (
        struct_id, struct_id)
    source += "\n{\n\tofs"
    num = len(keys)
    for j in range(num):
        key = keys[j]
        is_array = False
        if get_property and callable(get_property):
            if key[2] != 'char' and 1 == get_property(key[1], 'array'):
                is_array = True

        sep = 'CSV_SPLITTER_SYMBOL\n\t\t' if j != num - 1 else "'\\n';"
        if is_array:
            array_size = int(get_property(key[1], 'array_size'))
            assert array_size > 0
            for i in range(array_size):
                if j == num - 1 and i == array_size - 1:
                    sep = "'\\n';"
                source += "<<data.%s[%d]<<%s" % (key[1], i, sep)
        else:
            source += "<<data.%s<<%s" % (key[1], sep)
    source += "\n}\n"

    csv_writer_cpp = """
template<>
void CSVWriter<%s>(const std::vector<%s> & vec_data, std::ostream & ofs){
    for(auto it = vec_data.begin(); it != vec_data.end(); ++it){
        Internal_CSVWriteContent<%s>(*it, ofs);
    }
}
template<>
bool CSVWriter<%s>(const std::vector<%s> & vec_data, const std::string & csv_file){
    std::ofstream ofs( csv_file.c_str(), std::ios::out | std::ios::trunc);
    if(ofs.is_open()){
        ofs.setf(std::ios_base::fixed);
        Internal_CSVWriteHead<%s>(ofs);
        CSVWriter<%s>(vec_data, ofs);
        return true;
    }
    return false;
}
"""
    source += csv_writer_cpp % tuple([struct_id] * 7)
    return source


class CPPCsvWriterGenerator(CPPGeneratorBase):
    def __init__(self, src_folder, dest_folder, datastructs, file_name):
        CPPGeneratorBase.__init__(self, src_folder, dest_folder, file_name, search_keyid=False)

        self.datastructs = datastructs

        self.check_structs(datastructs)

        # python_dir = (os.path.dirname(os.path.realpath(__file__)))
        #
        # csv_hpp = 'read_parameters_csv_base.hpp'
        # dest = os.path.join(dest_folder, csv_hpp)
        # os.path.isfile(dest) or copyfile(os.path.join(python_dir, csv_hpp), dest)

    def _csv_reader(self, keys, struct_id):
        cpp = """template<>
bool ReadCsvParametersHelper<%s>(const csv::CSVRow & row, %s & data){
    bool flag = true;
"""
        cpp %= (struct_id, struct_id)

        tpl_fmt = """
    [init_impl]   
    if(row["%s"].%s()){
        [core_impl]
    }else{
        %s
    }
    
"""
        for key in keys:
            tmpKey = key[1].replace(".", "_")

            raw_type = key[2]
            if raw_type not in internal_csv_reader_map:
                unsupported_key(key[1], '_CsvReader', key[2], struct_id)
                exit(-1)

            # DisplayProperty : DataStructProperty
            has_valid_type = 'std::cerr<<">>> Failed to resolve key: %s with type: %s in DataStruct: %s."<<std::endl;\n'
            has_valid_type += '\t\t\tflag = false;'
            has_valid_type %= (tmpKey, key[2], struct_id)

            # if self.check_key_when_read:
            #     has_member = 'else{\n\t\tstd::cerr<<">>> Failed to find key: %s in DataStruct: %s."<<std::endl;\n\t\tflag = false;\n\t}'
            #     has_member %= (tmpKey, struct_id)
            # else:
            #     has_member = ''

            methods = internal_csv_reader_map[raw_type]

            # # read data
            if key[2] not in ['char', 'str'] and 1 == self.get_property(struct_id, key[1], 'array'):
                array_size = int(self.get_property(struct_id, key[1], 'array_size'))
                assert array_size > 0

                for i in range(array_size):
                    arrTmpKey = '%s%d' % (tmpKey, i + 1)
                    cpp_tpl_code = tpl_fmt % (arrTmpKey, methods[1], has_valid_type)
                    cpp_core_impl = internal_csv_reader('%s[%d]' % (key[1], i), arrTmpKey, raw_type)
                    cpp += cpp_tpl_code.replace('[core_impl]', cpp_core_impl).replace('[init_impl]', '')

            else:
                cpp_tpl_code = tpl_fmt % (tmpKey, methods[1], has_valid_type)
                cpp_tpl_init = ''
                cpp_core_impl = internal_csv_reader(key[1], tmpKey, raw_type)

                if key[2] in ['int', 'short', 'unsigned short', 'unsigned int', 'long long',
                              'double', 'float', 'long double']:
                    cpp_tpl_init = 'data.%s = (%s)std::numeric_limits<%s>::max();' % (key[1], key[2], key[2])
                elif key[2] in ['enum']:
                    cpp_tpl_init = 'data.%s = (%s)(0);' % (key[1], key[3])
                elif key[2] in ["bool", "unsigned char"]:
                    cpp_tpl_init = 'data.%s = (%s)(0);' % (key[1], key[2])

                # if raw_type in ['char', 'str'] and key[1] == self.key_id_map[struct_id]:
                #     cpp += cpp_core_impl
                # else:
                #     cpp += cpp_tpl_code.replace('[core_impl]', cpp_core_impl).replace('[init_impl]', cpp_tpl_init)
                cpp += cpp_tpl_code.replace('[core_impl]', cpp_core_impl).replace('[init_impl]', cpp_tpl_init)

        cpp += "\treturn flag;\n}\n\n"
        return cpp.replace('\t', '    ')

    def csv_reader(self, csvfile_prefix, include_header=None):
        hfile = """#ifndef CSVReader_AUTO_GENERATED_AT_%s_H
#define CSVReader_AUTO_GENERATED_AT_%s_H
#include <vector>
#include <string>
#include <fstream>
#include <cstring>
#include "csv.hpp"
#include "%s"

template<typename DataStruct>
bool ReadCsvParametersHelper(const csv::CSVRow &, DataStruct &){return false;}

template<typename DataStruct>
bool ReadCsvnParameters2Vector(const char * fileName, std::vector<DataStruct> & vec_data ){
    bool flag = true;
    csv::CSVReader reader(fileName, csv::DEFAULT_CSV_STRICT);    
    csv::CSVRow row;
    DataStruct data;
    while (reader.read_row(row)) {
        
        std::memset(&data, 0, sizeof(DataStruct));;
        if( ReadCsvParametersHelper<DataStruct>(row, data) ){
            vec_data.push_back(data);
        }else{
             flag = false;
        }
    }
    return flag;
};


"""
        cpp = """#include "%s.h"
#include <iostream>
#include <limits>

"""

        h_tpl = "template<>\nbool ReadCsvParametersHelper<%s>(const csv::CSVRow & row, %s & data);\n\n"

        if not isinstance(include_header, str):
            include_header = self.datastruct_file
        tod = datetime.datetime.today().strftime('%Y%m%dT%H%M%S')
        hfile %= (tod, tod, include_header)
        cpp %= csvfile_prefix

        for struct_id in self.datastructs:
            if struct_id in self.datastruct_property_dict:
                cpp += self._csv_reader(self.datastruct_property_dict[struct_id], struct_id)
                hfile += h_tpl % (struct_id, struct_id)

        hfile += "\n#endif"

        csv_reader_file = csvfile_prefix + ".cpp"
        self.writeToFile(csv_reader_file, cpp)
        csv_reader_file = csvfile_prefix + ".h"
        self.writeToFile(csv_reader_file, hfile)
        pass

    def csv_writer(self, csvfile_prefix, include_header=None):
        hfile = """#ifndef CSVWriter_AUTO_GENERATED_AT_%s_H
#define CSVWriter_AUTO_GENERATED_AT_%s_H
#include <vector>
#include <string>
#include <fstream>
#include <string>
#include "%s"

template<typename DataStruct>
std::string CSVWriteRtnHead(){ return ""; }
template<typename DataStruct>
void Internal_CSVWriteHead(std::ostream &ofs){}
template<typename DataStruct>
void Internal_CSVWriteContent(const DataStruct &, std::ostream &){}
template<typename DataStruct>
void CSVWriter(const std::vector<DataStruct> &, std::ostream &){}
template<typename DataStruct>
bool CSVWriter(const std::vector<DataStruct> &, const std::string &){return false;}


"""

        h_tpl = """template<>
std::string CSVWriteRtnHead<%s>();
template<>
void Internal_CSVWriteHead<%s>(std::ostream &ofs);
template<>
void Internal_CSVWriteContent<%s>(const %s &, std::ostream &);
template<>
void CSVWriter<%s>(const std::vector<%s> &, std::ostream &);
template<>
bool CSVWriter<%s>(const std::vector<%s> &, const std::string &);
"""

        cpp = """#include "%s.h"
#define CSV_SPLITTER_SYMBOL    ','

"""
        if not isinstance(include_header, str):
            include_header = self.datastruct_file
        tod = datetime.datetime.today().strftime('%Y%m%dT%H%M%S')
        hfile %= (tod, tod, include_header)
        cpp %= csvfile_prefix

        for struct_id in self.datastructs:
            if struct_id in self.datastruct_property_dict:
                cpp += "/*\n * @brief csv_writer_for datastruct:%s\n */\n" % struct_id
                fun = functools.partial(self.get_property, struct_id)
                cpp += _csv_writer_header(self.datastruct_property_dict[struct_id], struct_id, fun)
                cpp += _csv_writer_content(self.datastruct_property_dict[struct_id], struct_id, fun)
                cpp += "\n\n"

                hfile += "/*\n * @brief csv_writer_for datastruct:%s\n */\n" % struct_id
                hfile += h_tpl % tuple([struct_id] * 8)
                hfile += "\n\n"
            else:
                print('[Warning] Failed to parse struct_id %s from file %s' % (struct_id, self.datastruct_file))
        hfile += "#endif"

        self.writeToFile(csvfile_prefix + ".cpp", cpp)
        self.writeToFile(csvfile_prefix + ".h", hfile)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='CSV Reader/Writer cpp Generator')
    parser.add_argument('-i', '--include', help="include other header file instead of the parsing header file")
    parser.add_argument('-l', '--lib', default='csv', help="library name")
    parser.add_argument("-s", "--struct", default='',
                      help="Specify the datastruct names(separated by comma(,)) for createing csv reader/writer")
    parser.add_argument('header', help="The cpp header file that need to parse.")

    opt = parser.parse_args()
    print(opt)
    destination = opt.header
    if not os.path.isfile(destination):
        print ("The file: %s is not a valid file!" % destination)
        exit(-1)

    project_dstruct_file = os.path.basename(destination)
    if not re.match(r'.{3,}\.h$', project_dstruct_file):
        print ("A valid datastruct filename should at least contain three characters!")
        exit(-1)

    raw_destination = os.path.dirname(destination)
    project_name = os.path.splitext(project_dstruct_file)[0]
    destination = os.path.join(raw_destination, project_name)
    ensure_exists_dir(destination)

    src_destination = os.path.join(destination, opt.lib)
    ensure_exists_dir(src_destination)

    # -------------- folder structure has been setup ------------------------

    datastruct_dict = []
    if opt.struct:
        datastruct_dict = opt.struct.split(',')
    else:
        with open(opt.header, "rb") as f:
            t1 = f.readline().decode('utf8')
            f.close()
            t1 = t1.strip()

            if not t1.startswith("//Configuration:"):
                print ("You need to specify a configuration in the first line starting with //Configuration: for file:", opt.header)
                exit(-1)

            t1 = t1.replace("//Configuration:", "")
            datastruct_dict = t1.split(",")
       
    if len(datastruct_dict) < 1:
        print ("There is no datastruct, please configure!")
        exit(1)

    cpp_generator = CPPCsvWriterGenerator(raw_destination, src_destination, datastruct_dict, project_dstruct_file)

    cpp_generator.csv_writer("csv_writer", opt.include)
    cpp_generator.csv_reader("csv_reader", opt.include)
    cpp_generator.create_cmakelists(opt.lib)
