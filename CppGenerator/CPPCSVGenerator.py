# coding=utf-8
#####!/usr/bin/python
#######! /usr/bin/python
# -*- coding: utf-8 -*-
from sys import platform as sys_platform
import os.path
from shutil import copyfile
import re
import datetime
import subprocess
from CPPGeneratorBase import CPPGeneratorBase, ensure_exists_dir


def _csv_writer_header(keys, struct_id):
    source = "template<>\nstd::string CSVWriteRtnHead<%s>()\n{\n\tstd::string header;\n" % struct_id
    last_key = keys.pop()
    for key in keys:
        title = key[1].title().replace("_", "").replace("-", "")
        source += "\theader.append(\"%s\");\theader.push_back(CSV_SPLITTER_SYMBOL);\n" % title;
        
    title = last_key[1].title().replace("_", "").replace("-", "")
    source += "\theader.append(\"%s\");\theader.push_back('\\n');\n" % title;

    source += "\n\treturn header;\n}\n"
    keys.append(last_key)

    source += "template<>\nvoid Internal_CSVWriteHead<%s>(std::ofstream &ofs)" % struct_id
    source += "\n{\n\tofs << CSVWriteRtnHead<%s>();" % struct_id
    source += "\n}\n"
    # source += "\n{\n\tofs"
    # last_key = keys.pop()
    # for key in keys:
        # title = key[1].title().replace("_", "").replace("-", "")
        # source += '<<"%s"<<CSV_SPLITTER_SYMBOL\n\t\t' % title
        # # source += "<<\"" + title + "\"<<CSV_SPLITTER_SYMBOL\n\t\t"

    # title = last_key[1].title().replace("_", "").replace("-", "")
    # source += '<<"%s\\n";' % title

    # source += "\n}\n"
    # keys.append(last_key)
       
    return source

def _csv_writer_content(keys, struct_id):
    source = "template<>\nvoid Internal_CSVWriteContent<%s>( const %s & data, std::ofstream &ofs)" % (
        struct_id, struct_id)
    source += "\n{\n\tofs"
    last_key = keys.pop()
    for key in keys:
        source += '<<data.%s<<CSV_SPLITTER_SYMBOL\n\t\t' % key[1]
        # source += "<<data." + key[1] + "<<CSV_SPLITTER_SYMBOL\n\t\t"
    source += '<<data.%s<<\"\\n\";' % last_key[1]
    # source += "<<data." + last_key[1] + "<<\"\\n\";"
    keys.append(last_key)
    source += "\n}\n"

    csv_writer_cpp = """
template<>
void CSVWriter<%s>(const std::vector<%s> & vec_data, std::ofstream & ofs){
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
void Internal_CSVWriteHead(std::ofstream &ofs){}
template<typename DataStruct>
void Internal_CSVWriteContent(const DataStruct &, std::ofstream &){}
template<typename DataStruct>
void CSVWriter(const std::vector<DataStruct> &, std::ofstream &){}
template<typename DataStruct>
bool CSVWriter(const std::vector<DataStruct> &, const std::string &){return false;}


"""

        h_tpl = """template<>
std::string CSVWriteRtnHead<%s>();
template<>
void Internal_CSVWriteHead<%s>(std::ofstream &ofs);
template<>
void Internal_CSVWriteContent<%s>(const %s &, std::ofstream &);
template<>
void CSVWriter<%s>(const std::vector<%s> &, std::ofstream &);
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
                cpp += _csv_writer_header(self.datastruct_property_dict[struct_id], struct_id)
                cpp += _csv_writer_content(self.datastruct_property_dict[struct_id], struct_id)
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
    cpp_generator.create_cmakelists(opt.lib)
