# -*- coding: utf-8 -*-
from sys import platform as sys_platform
import os.path
import re
from shutil import copyfile
import subprocess
from CPPGeneratorBase import CPPGeneratorBase, ensure_exists_dir, unsupported_key
import datetime

internal_json_writer_map = dict({
    "int": "Int",
    "short": "Int",
    "enum": "Int",
    "unsigned int": "Uint",
    "unsigned short": "Uint",
    "long": "Int64",
    "unsigned long": "Uint64",
    "long long": "Int64",
    "double": "Double",
    "long double": "Double",
    "float": "Double",
    "bool": "Bool",
    "char": "String",
    "str": "String",
    "unsigned char": "String",
})

internal_json_reader_map = dict({
    "int": ("GetInt", "IsInt"),
    "short": ("GetInt", "IsInt"),
    "enum": ("GetInt", "IsInt"),
    "unsigned int": ("GetUint", "IsUint"),
    "unsigned short": ("GetUint", "IsUint"),
    "long": ("GetInt64", "IsInt64"),
    "unsigned long": ("GetUint64", "IsUint64"),
    "long long": ("GetInt64", "IsInt64"),
    "double": ("GetDouble", "IsNumber"),
    "long double": ("GetDouble", "IsNumber"),
    "float": ("GetFloat", "IsNumber"),
    "bool": ("GetBool", "IsBool"),
    "char": ("GetString", "IsString"),
    "str": ("GetString", "IsString"),
    "unsigned char": ("GetString", "IsString"),
})


def internal_json_reader(cpp_key, py_key, raw_type):
    cpp = ''
    if raw_type in ['char', 'unsigned char', 'str']:
        if raw_type == 'unsigned char':
            cpp = 'data.%s = obj["%s"].GetString()[0];' % (cpp_key, py_key)
        else:
            cpp = 'strncpy(data.%s, obj["%s"].GetString(), sizeof(data.%s)-1);' % (cpp_key, py_key, cpp_key)

            check_str_size_fmt = """
    if(obj["%s"].GetStringLength() <= sizeof(data.%s)-1){
        %s
    }else{
        std::cerr<<">>> String is too bigger for char %s[] with py_key %s."<<std::endl;
        flag = false;
    }
"""
            cpp = check_str_size_fmt % (py_key, cpp_key, cpp, cpp_key, py_key)

    elif raw_type in internal_json_reader_map:
        methods = internal_json_reader_map[raw_type]
        cpp = 'data.%s = (%s)(obj["%s"].%s());' % (cpp_key, raw_type, py_key, methods[0])
    else:
        print('Unknow json reader type:', raw_type)
        exit(-1)
    return cpp


class CPPJsonGenerator(CPPGeneratorBase):
    def __init__(self, src_folder, dest_folder, datastructs, file_name, check_key_when_read):
        CPPGeneratorBase.__init__(self, src_folder, dest_folder, file_name, search_keyid=True)

        self.datastructs = datastructs
        self.check_structs(datastructs, check_key_id=True)

        python_dir = (os.path.dirname(os.path.realpath(__file__)))

        json_hpp = 'read_parameters_json_base.hpp'
        dest = os.path.join(dest_folder, json_hpp)
        os.path.isfile(dest) or copyfile(os.path.join(python_dir, json_hpp), dest)

        json_hpp = 'read_parameters_json_base.cpp'
        dest = os.path.join(dest_folder, json_hpp)
        os.path.isfile(dest) or copyfile(os.path.join(python_dir, json_hpp), dest)

        json_hpp = 'save_parameters_json_base.hpp'
        dest = os.path.join(dest_folder, json_hpp)
        os.path.isfile(dest) or copyfile(os.path.join(python_dir, json_hpp), dest)

        self.check_key_when_read = check_key_when_read

    def _JsonParameterReader(self, keys, struct_id):
        cpp = """template<>
bool ReadJsonParametersHelper<%s>(const rapidjson::Value::ConstObject & obj, %s & data){
    bool flag = true;
"""
        cpp %= (struct_id, struct_id)

        tpl_fmt = """
    [init_impl]
    if(obj.HasMember( "%s" )){
        if(obj["%s"].%s()){
            [core_impl]
        }else{
            %s
        }
    }%s
"""

        for key in keys:
            tmpKey = key[1].replace(".", "_")

            raw_type = key[2]
            if raw_type not in internal_json_reader_map:
                unsupported_key(key[1], '_JsonParameterReader', key[2], struct_id)
                exit(-1)

            # DisplayProperty : DataStructProperty
            has_valid_type = 'std::cerr<<">>> Failed to resolve key: %s with type: %s in DataStruct: %s."<<std::endl;\n'
            has_valid_type += '\t\t\tflag = false;'
            has_valid_type %= (tmpKey, key[2], struct_id)

            if self.check_key_when_read:
                has_member = 'else{\n\t\tstd::cerr<<">>> Failed to find key: %s in DataStruct: %s."<<std::endl;\n\t\tflag = false;\n\t}'
                has_member %= (tmpKey, struct_id)
            else:
                has_member = ''

            methods = internal_json_reader_map[raw_type]


            # # read data
            if key[2] not in ['char', 'str'] and 1 == self.get_property(struct_id, key[1], 'array'):
                array_size = int(self.get_property(struct_id, key[1], 'array_size'))
                assert array_size > 0
                cpp_tpl_code = tpl_fmt % (tmpKey, tmpKey, "IsArray", has_valid_type, has_member)

                cpp_arr_tpl = """
            const rapidjson::Value & arr = obj["%s"];
            if(%d != (int) arr.Size()){
                std::cerr<<">>> array_size of %s is invalid in DataStruct %s"<<std::endl;
                flag = false;
            }else{
                for (int i = 0; i < %d; ++i){
                    data.%s[i] = (%s)(arr[i].%s());
                }
            } 
"""

                cpp_arr_tpl %= (tmpKey, array_size, key[1], struct_id, array_size, key[1], raw_type, methods[0])
                cpp += cpp_tpl_code.replace('[core_impl]', cpp_arr_tpl).replace('[init_impl]', '')

            else:
                cpp_tpl_code = tpl_fmt % (tmpKey, tmpKey, methods[1], has_valid_type, has_member)
                cpp_tpl_init = ''
                cpp_core_impl = internal_json_reader(key[1], tmpKey, raw_type)

                if key[2] in ['int', 'short', 'unsigned short', 'unsigned int', 'long long',
                              'double', 'float', 'long double']:
                    cpp_tpl_init = 'data.%s = (%s)std::numeric_limits<%s>::max();' % (key[1], key[2], key[2])
                elif key[2] in ['enum']:
                    cpp_tpl_init = 'data.%s = (%s)(0);' % (key[1], key[3])
                elif key[2] in ["bool", "unsigned char"]:
                    cpp_tpl_init = 'data.%s = (%s)(0);' % (key[1], key[2])

                if raw_type in ['char', 'str'] and key[1] == self.key_id_map[struct_id]:
                    cpp += cpp_core_impl
                else:
                    cpp += cpp_tpl_code.replace('[core_impl]', cpp_core_impl).replace('[init_impl]', cpp_tpl_init)

        cpp += "\treturn flag;\n}\n\n"
        return cpp.replace('\t', '    ')

    def JsonParameterReader(self, json_reader_file_prefix, include_header=None):
        cpp = """#include "%s.h"
#include <iostream>
#include <limits>

"""

        hfile = """#ifndef READ_JSONFILE_USING_RAPIDJSON_%s
#define READ_JSONFILE_USING_RAPIDJSON_%s

#include "read_parameters_json_base.hpp"
#include "%s"

"""
        h_tpl = """template<>
bool ReadJsonParametersHelper<%s>(const rapidjson::Value::ConstObject & obj, %s & data);\n
"""

        if not isinstance(include_header, str):
            include_header = self.datastruct_file
        tod = datetime.datetime.today().strftime('%Y%m%dT%H%M%S')
        hfile %= (tod, tod, include_header)
        cpp %= json_reader_file_prefix

        for struct_id in self.datastructs:
            if struct_id in self.datastruct_property_dict:
                cpp += self._JsonParameterReader(self.datastruct_property_dict[struct_id], struct_id)
                hfile += h_tpl % (struct_id, struct_id)

        hfile += "\n#endif"

        json_reader_file = json_reader_file_prefix + ".cpp"
        self.writeToFile(json_reader_file, cpp)
        json_reader_file = json_reader_file_prefix + ".h"
        self.writeToFile(json_reader_file, hfile)

    def _JsonParameterWriter(self, keys, struct_id):
        cpp = """template<>
void SaveJsonParametersHelper<%s>(rapidjson::PrettyWriter<rapidjson::FileWriteStream>  & writer, const %s & data){
    char unsigned_char_helper[2]; unsigned_char_helper[0]=0; unsigned_char_helper[1]=0;
    (void)unsigned_char_helper;
    writer.String(data.%s);
    writer.StartObject();
"""
        cpp %= (struct_id, struct_id, self.key_id_map[struct_id])

        unsigned_char_fmt = """
    unsigned_char_helper[0] = (char)data.%s;
    writer.String(unsigned_char_helper);
"""

        for key in keys:
            tmpKey = key[1].replace(".", "_")
            cpp += '\twriter.String("%s");\n' % tmpKey

            raw_type = key[2]
            if raw_type not in internal_json_writer_map:
                unsupported_key(key[1], '_JsonParameterWriter', key[2], struct_id)
                exit(-1)

            method = internal_json_writer_map[raw_type]
            # # array
            if key[2] != 'char' and 1 == self.get_property(struct_id, key[1], 'array'):
                cpp += "\twriter.StartArray();\n"
                array_size = int(self.get_property(struct_id, key[1], 'array_size'))
                assert array_size > 0
                for i in range(array_size):
                    cpp += "\t\twriter.%s(data.%s[%d]);\n" % (method, key[1], i)
                cpp += "\twriter.EndArray();\n"
            else:
                # DisplayProperty : DataStructProperty
                if key[2] == "unsigned char":
                    cpp += unsigned_char_fmt % (key[1], tmpKey)
                else:
                    cpp += "\twriter.%s(data.%s);\n" % (method, key[1])

        cpp += "\twriter.EndObject();\n}\n\n"
        return cpp.replace('\t', '    ')

    def JsonParameterWriter(self, json_writer_file_prefix, include_header=None):
        cpp = """#include "%s.h"

"""
        tod = datetime.datetime.today().strftime('%Y%m%dT%H%M%S')
        hfile = """#ifndef SAVE_JSONFILE_USING_RAPIDJSON_%s
#define SAVE_JSONFILE_USING_RAPIDJSON_%s
#include "save_parameters_json_base.hpp"
#include "%s"

"""
        h_tpl = """template<>
void SaveJsonParametersHelper<%s>(rapidjson::PrettyWriter<rapidjson::FileWriteStream>  & writer, const %s &);\n
"""

        if not isinstance(include_header, str):
            include_header = self.datastruct_file
        hfile %= (tod, tod, include_header)
        cpp %= json_writer_file_prefix

        for struct_id in self.datastructs:
            if struct_id in self.datastruct_property_dict:
                cpp += self._JsonParameterWriter(self.datastruct_property_dict[struct_id], struct_id)
                hfile += h_tpl % (struct_id, struct_id)

        hfile += "\n#endif"

        json_writer_file = json_writer_file_prefix + ".cpp"
        self.writeToFile(json_writer_file, cpp)
        json_writer_file = json_writer_file_prefix + ".h"
        self.writeToFile(json_writer_file, hfile)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Json Reader/Writer cpp Generator')
    parser.add_argument('-c', '--check', action='store_true',
                        help="check every member variable in DataStruct")
    parser.add_argument('-i', '--include', help="include other header file instead of the parsing header file")
    parser.add_argument('-l', '--lib', default='rwjson', help="library name")
    parser.add_argument("-s", "--struct", default='',
                        help="Specify the datastruct names(separated by comma(,)) for createing csv reader/writer")
    parser.add_argument('header', help="The cpp header file that need to parse;")

    opt = parser.parse_args()
    print(opt)
    destination = opt.header
    if not os.path.isfile(destination):
        print("The file: %s is not a valid file!" % destination)
        exit(-1)

    project_struct_file = os.path.basename(destination)
    if not re.match(r'.{3,}\.h$', project_struct_file):
        print("A valid datastruct file at least contains three characters!")
        exit(-1)

    raw_destination = os.path.dirname(destination)
    project_name = os.path.splitext(project_struct_file)[0]
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
                print("You need to specify a configuration in the first line starting with //Configuration: for file:",
                      opt.header)
                exit(-1)

            t1 = t1.replace("//Configuration:", "")
            datastruct_dict = t1.split(",")

    if len(datastruct_dict) < 1:
        print("There is no datastruct, please configure!")
        exit(1)

    cpp_generator = CPPJsonGenerator(raw_destination, src_destination, datastruct_dict, project_struct_file, opt.check)

    cpp_generator.JsonParameterReader("read_json_parameters", opt.include)
    cpp_generator.JsonParameterWriter("save_json_parameters", opt.include)
    cpp_generator.create_cmakelists(opt.lib)
