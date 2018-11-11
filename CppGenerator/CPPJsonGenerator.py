# coding=utf-8
#####!/usr/bin/python
#######! /usr/bin/python
# -*- coding: utf-8 -*-
from sys import platform as sys_platform
import os.path
import re
from shutil import copyfile
import subprocess
from CPPGeneratorBase import CPPGeneratorBase, ensure_exists_dir, unsupported_key
import datetime


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
bool ReadJsonParametersHelper<%s>(const rapidjson::Value::ConstObject & obj, %s & pConfig){
    bool flag = true;
"""
        cpp %= (struct_id, struct_id)

        double_fmt = """
    pConfig.%s = (%s)std::numeric_limits<%s>::max();
    if(obj.HasMember( "%s" )){
        if(obj["%s"].IsNumber()){
            pConfig.%s = (%s)( obj["%s"].GetDouble() );
        }else{
            %s
        }
    }else{
        %s
    }
"""
        enum_fmt = """
    pConfig.%s = (%s)(0);
    if(obj.HasMember( "%s" )){
        if(obj["%s"].IsInt()){
            pConfig.%s = (%s)( obj["%s"].GetInt() );
        }else{
            %s
        }
    }else{
        %s
    }
"""
        int_fmt = """
    pConfig.%s = (%s)std::numeric_limits<%s>::max();
    if(obj.HasMember( "%s" )){
        if(obj["%s"].IsInt()){
            pConfig.%s = (%s)( obj["%s"].GetInt() );
        }else{
            %s
        }
    }else{
        %s
    }
"""
        bool_fmt = """
    pConfig.%s = false;
    if(obj.HasMember( "%s" )){
        if(obj["%s"].IsBool()){
            pConfig.%s = obj["%s"].GetBool();
        }else{
            %s
        }
    }else{
        %s
    }
"""
        unsigned_char_fmt = """
    pConfig.%s = 0;
    if(obj.HasMember( "%s" )){
        if(obj["%s"].IsString()){
            pConfig.%s = obj["%s"].GetString()[0];
        }else{
            %s
        }
    }else{
        %s
    }
"""
        str_fmt = """
    if(obj.HasMember( "%s" )){
        if(obj["%s"].IsString()){
            strncpy(pConfig.%s, obj["%s"].GetString(), sizeof(pConfig.%s)-1);
        }else{
            %s
        }
    }else{
        %s
    }
"""
        keystr_fmt = """
    strncpy(pConfig.%s, obj["%s"].GetString(), sizeof(pConfig.%s)-1);
"""

        for key in keys:
            # DisplayProperty : DataStructProperty
            tmpKey = key[1].replace(".", "_")

            has_valid_type = 'flag = false;\n'
            has_valid_type += '\t\t\tstd::cerr<<">>> Failed to resolve key: %s with type: %s in DataStruct: %s."<<std::endl;'
            has_valid_type %= (tmpKey, key[2], struct_id)

            if self.check_key_when_read:
                has_member = 'std::cerr<<">>> Failed to find key: %s in DataStruct: %s."<<std::endl;\n\t\tflag = false;'
                has_member %= (tmpKey, struct_id)
            else:
                has_member = ''
            # prop = self.get_property(struct_id, key[1])
            # print(prop)

            if key[2] in ['int', 'short', 'unsigned short', 'unsigned int']:
                cpp += (int_fmt % (key[1], key[2], key[2], tmpKey, tmpKey, key[1], key[2], tmpKey, has_valid_type, has_member))
            elif key[2] in ['enum']:
                cpp += (enum_fmt % (key[1], key[3], tmpKey, tmpKey, key[1], key[3], tmpKey, has_valid_type, has_member))
            elif key[2] in ['double', 'float']:
                cpp += (double_fmt % (key[1], key[2], key[2], tmpKey, tmpKey, key[1], key[2], tmpKey, has_valid_type, has_member))
            elif key[2] == "bool":
                cpp += (bool_fmt % (key[1], tmpKey, tmpKey, key[1], tmpKey, has_valid_type, has_member))
            elif key[2] == "unsigned char":
                cpp += unsigned_char_fmt % (key[1], tmpKey, tmpKey, key[1], tmpKey, has_valid_type, has_member)
            elif key[2] in ["char", "str"]:
                if key[1] == self.key_id_map[struct_id]:
                    cpp += keystr_fmt % (key[1], tmpKey, key[1])
                else:
                    cpp += str_fmt % (tmpKey, tmpKey, key[1], tmpKey, key[1], has_valid_type, has_member)
            else:
                unsupported_key(key[1], '_JsonParameterReader', key[2], struct_id)

        cpp += "\treturn flag;\n}\n\n"
        return cpp

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
bool ReadJsonParametersHelper<%s>(const rapidjson::Value::ConstObject & obj, %s & pConfig);\n
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
        double_fmt = """
    writer.String("%s");
    writer.Double((double)data.%s);
"""
        int_fmt = """
    writer.String("%s");
    writer.Int((int)data.%s);
"""
        bool_fmt = """
    writer.String("%s");
    writer.Bool(data.%s);
"""
        unsigned_char_fmt = """
    unsigned_char_helper[0] = (char)data.%s;
    writer.String("%s");
    writer.String(unsigned_char_helper);
"""
        str_fmt = """
    writer.String("%s");
    writer.String(data.%s);
"""

        for key in keys:
            # DisplayProperty : DataStructProperty
            tmpKey = key[1].replace(".", "_")
            if key[2] in ['int', 'short', 'unsigned short', 'unsigned int', 'enum']:
                cpp += (int_fmt % (tmpKey, key[1]))
            elif key[2] in ['double', 'float']:
                cpp += (double_fmt % (tmpKey, key[1]))
            elif key[2] == "bool":
                cpp += (bool_fmt % (tmpKey, key[1]))
            elif key[2] == "unsigned char":
                cpp += unsigned_char_fmt % (key[1], tmpKey)
            elif key[2] in ["char", "str"]:
                cpp += str_fmt % (tmpKey, key[1])
            else:
                unsupported_key(key[1], '_JsonParameterWriter', key[2], struct_id)

        cpp += "\twriter.EndObject();\n}\n\n"
        return cpp

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
        print ("The file: %s is not a valid file!" % destination)
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
                print ("You need to specify a configuration in the first line starting with //Configuration: for file:", opt.header)
                exit(-1)

            t1 = t1.replace("//Configuration:", "")
            datastruct_dict = t1.split(",")
       
    if len(datastruct_dict) < 1:
        print ("There is no datastruct, please configure!")
        exit(1)

    cpp_generator = CPPJsonGenerator(raw_destination, src_destination, datastruct_dict, project_struct_file, opt.check)

    cpp_generator.JsonParameterReader("read_json_parameters", opt.include)
    cpp_generator.JsonParameterWriter("save_json_parameters", opt.include)
    cpp_generator.create_cmakelists(opt.lib)
