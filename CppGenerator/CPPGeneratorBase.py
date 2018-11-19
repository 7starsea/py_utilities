# -*- coding: utf-8 -*-
import re
import os.path
from shutil import copyfile
import CppHeaderParser


def ensure_exists_dir(my_folder):
    return os.path.exists(my_folder) or os.path.isdir(my_folder) or os.makedirs(my_folder)


def unsupported_key(key, name, raw_type, struct_id):
    print(">>> In %s, unsupported key: %s with type: %s for datastruct: %s" % (name, key, raw_type, struct_id))


def format_key(key, max_length=20):
    key = key.replace("-", "_")
    if -1 == key.find("_"):
        a = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
        key = a.sub(r'_\1', key).lower()
    keys = key.split(".")
    header = ""
    if 2 == len(keys):
        header = keys[0].capitalize()[0:3]
        header += "."
        key = keys[1]
        max_length -= 4
    elif 1 != len(keys):
        print ("Unexpected error for key:", key)

    names = key.split("_")
    totalLength = 0
    tmpNames = []
    for name in names:
        tmpNames.append(name.capitalize())
        totalLength += len(name)
    names = tmpNames
    while totalLength > max_length:
        i = 0
        j = i
        while i < len(names):
            if len(names[i]) > len(names[j]):
                j = i
            i += 1
        names[j] = names[j][:-1]
        totalLength -= 1
    return header + ("".join(names))


def comment_remover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " "  # note: a space and not an empty string
        else:
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)


def recap_typedefs(include_cpp_header):
    typedefs = include_cpp_header.typedefs
    t_defs = dict()
    for k in typedefs:
        v = typedefs[k]
        if v not in include_cpp_header.C_FUNDAMENTAL:
            continue
        i = k.find('[')
        if i >= 0:
            t_defs[k[0:i]] = (v, int(k[(i+1):-1]))
        else:
            t_defs[k] = (v, 0)
    print(t_defs)

    for struct_id in include_cpp_header.classes:
        properties = include_cpp_header.classes[struct_id]['properties']['public']
        for property in properties:
            # print property
            if property['raw_type'].startswith("::"):
                sub_properties = property['class']['properties']['public']
                for sub_property in sub_properties:
                    raw_type = sub_property['raw_type']
                    if raw_type not in include_cpp_header.C_FUNDAMENTAL:
                        if raw_type in t_defs:
                            v, s = t_defs[raw_type]
                            sub_property['raw_type'] = v
                            sub_property['type'] = v
                            sub_property['array_size'] = s
                            sub_property['array'] = 1 if s > 0 else 0
                            sub_property['fundamental'] = True
                            sub_property['unresolved'] = False
                        else:
                            print('>>> [recap_typedef] Unknown type:%s' % raw_type)
                            exit(-1)
            else:
                raw_type = property['raw_type']
                if raw_type not in include_cpp_header.C_FUNDAMENTAL:
                    if raw_type in t_defs:
                        v, s = t_defs[raw_type]
                        property['raw_type'] = v
                        property['type'] = v
                        property['array_size'] = s
                        property['array'] = 1 if s > 0 else 0
                        property['fundamental'] = True
                        property['unresolved'] = False
                    elif raw_type in ['unsigned char']:
                        pass
                    else:
                        print('>>> [recap_typedef] Unknown type:', raw_type)
                        exit(-1)


def search_key_id(include_file_name, include_cpp_header, search_reset_keyid=False):
    key_id_map = dict()
    with open(include_file_name, 'rb') as file_obj:
        content_lines = list(map(lambda line: line.decode('utf8').strip(), file_obj.readlines()))

        key_id_pattern = re.compile(r'\skey_id[^{]{2,}{\s*(return\s+this->|return\s+)([\w\\.]+)\s*;\s*}')
        for struct_id in include_cpp_header.classes:
            methods = include_cpp_header.classes[struct_id]['methods']['public']
            key_id_method = None
            reset_key_id_method = None
            for method in methods:
                if method['name'] == 'key_id':
                    key_id_method = method
                elif method['name'] == 'reset_key_id':
                    reset_key_id_method = method

            if not key_id_method:
                # print '> Warning, failed to find method key_id in datastruct:', struct_id
                continue

            key_id = ''
            i1 = key_id_method['line_number'] - 1
            i2 = i1 + 1
            m = re.search(key_id_pattern, ''.join(content_lines[i1:i2]))
            # print ''.join(content_lines[i1:i2]), m.group(0) if m else m
            while not m:
                i2 += 1
                m = re.search(key_id_pattern, ''.join(content_lines[i1:i2]))
                if i2 - i1 >= 20 and (not m):
                    print ('> Warning, in public method key_id of datastruct %s, could not resolve the key_id!' % struct_id)
                    break
            if m:
                key_id = m.group(2)
                key_id_map[struct_id] = key_id
                print ('Found key_id: %s in datastruct: %s ' % (key_id, struct_id))
            else:
                continue

            if not search_reset_keyid:
                continue
            if not reset_key_id_method:
                print ('> Warning, failed to find method reset_key_id in datastruct:', struct_id)
                del key_id_map[struct_id]
                continue
            reset_key_id_pattern = re.compile(r'\sreset_key_id[^{]{2,}{\s*strn?cpy\s*\((this->'+key_id+'|'+key_id+')')
            i1 = reset_key_id_method['line_number'] - 1
            i2 = i1 + 1
            m = re.search(reset_key_id_pattern, ''.join(content_lines[i1:i2]))
            # print (''.join(content_lines[i1:i2]), m.group(0) if m else m)
            while not m:
                i2 += 1
                m = re.search(reset_key_id_pattern, ''.join(content_lines[i1:i2]))
                if i2 - i1 >= 20 and (not m):
                    print ('> Warning, incompatible key_id in methods key_id and reset_key_id of datastruct %s.' % struct_id)
                    del key_id_map[struct_id]
                    break
    return key_id_map


class CPPGeneratorBase:
    def __init__(self, src_folder, dest_folder, cpp_header_file, search_keyid=True, search_reset_keyid=False):
        self.cpp_header = None
        self.enums_ = []
        self.dest_folder = dest_folder
        self.datastruct_file = cpp_header_file
        self.key_id_map = dict()

        file_name = os.path.join(src_folder, cpp_header_file)
        # # copy
        copyfile(file_name, os.path.join(dest_folder, cpp_header_file))

        try:
            self.cpp_header = CppHeaderParser.CppHeader(file_name)
            self._parse_enum(self.cpp_header.enums)
            # print(self.cpp_header.enums)
            print(self.cpp_header.C_FUNDAMENTAL)
            if self.cpp_header.typedefs:
                recap_typedefs(self.cpp_header)

            if search_keyid:
                self.key_id_map.update(search_key_id(file_name, self.cpp_header, search_reset_keyid))

            for include in self.cpp_header.includes:
                if include.startswith('"') and include.endswith('"'):
                    include_file_name = include.strip('"')

                    include_file = os.path.join(src_folder, include_file_name)

                    if os.path.exists(include_file):
                        copyfile(include_file, os.path.join(dest_folder, include_file_name))

                        include_file_name = os.path.join(dest_folder, include_file_name)
                        include_cpp_header = CppHeaderParser.CppHeader(include_file_name)
                        if include_cpp_header.typedefs:
                            recap_typedefs(include_cpp_header)

                        if search_keyid:
                            self.key_id_map.update(search_key_id(include_file_name, include_cpp_header,
                                                                 search_reset_keyid))
                        self.cpp_header.classes.update(include_cpp_header.classes)
                    else:
                        print('[Warning] Failed to find include_file: %s' % include_file_name)

        except CppHeaderParser.CppParseError as e:
            print(e)
            exit(1)

        self.datastruct_property_dict = dict()
        self.init()

    def _parse_enum(self, enums):
        for e in enums:
            assert (not e['typedef'])
            self.enums_.append(e['name'])

    def create_header_wrapper(self, header_wrapper):
        f = os.path.join(self.dest_folder, header_wrapper)
        if os.path.isfile(f):
            print(">>> [Waring] header wrapper: %s already exists." % f)
            input("Press any key to continue")

        import datetime
        tod = datetime.datetime.today().strftime('%Y%m%dT%H%M%S')
        hfile = """#ifndef CPP_GENERATOR_BASE_GENERATRED_AT_%s
#define CPP_GENERATOR_BASE_GENERATRED_AT_%s

#include "%s"   ///original datastruct file

#endif
"""
        hfile %= (tod, tod, self.datastruct_file)
        self.writeToFile(header_wrapper, hfile)
        self.datastruct_file = header_wrapper

    def check_structs(self, datastruct_ids, check_key_id=False):
        exit_flag = False
        for struct_id in datastruct_ids:
            if struct_id not in self.datastruct_property_dict:
                print("Configuration Error: %s is not contained in the source code!" % struct_id)
                exit_flag = True
            if check_key_id and struct_id not in self.key_id_map:
                print("Source code Error: %s does not have method key_id or reset_key_id!" % struct_id)
                exit_flag = True

        if exit_flag:
            exit(-1)

    def writeToFile(self, file_name, content):
        file_name = os.path.join(self.dest_folder, file_name)
        with open(file_name, 'w') as f:
            f.write(content)
            f.close()
            print("Updated file: ", file_name)

    def _check_raw_type(self, raw_type):
        if raw_type not in self.cpp_header.C_FUNDAMENTAL:
            if raw_type.split(' ')[-1] not in self.cpp_header.C_FUNDAMENTAL:
                print('Unexpected raw_type: %s, all raw_type must be C_FUNDAMENTAL: %s' % (raw_type, ','.join(self.cpp_header.C_FUNDAMENTAL)))
                exit(-1)

    # # initialize datastruct_dict with key=struct_id values=all member variable and related information in that sturct
    # # values = list of tuple with (fmt_name, original_member_variable_name, raw_type, extr_info_for_enum(name))
    def init(self):
        for struct_id in self.cpp_header.classes:
            max_length = 20
            keys = []
            tmp_keys = []
            # methods = self.cpp_header.classes[struct_id]['methods']['public']
            properties = self.cpp_header.classes[struct_id]['properties']['public']
            # print(properties)
            for property0 in properties:
                #print property0
                if property0['raw_type'].startswith("::"):
                    sub_properties = property0['class']['properties']['public']
                    for sub_property0 in sub_properties:
                        tmpName = property0['name']
                        tmpName += "."
                        tmpName += sub_property0['name']
                        fmt_name = format_key(tmpName, max_length)
                        raw_type = sub_property0['raw_type']
                        self._check_raw_type(raw_type)
                        if 0 == sub_property0['array'] and 'char' == raw_type:
                            raw_type = 'unsigned char'

                        tmp_keys.append(fmt_name)
                        if sub_property0['raw_type'] == sub_property0['type']:
                            keys.append((fmt_name, tmpName, raw_type))
                        else:
                            if sub_property0['type'] in self.enums_:
                                keys.append((fmt_name, tmpName, 'enum', sub_property0['type']))
                            else:
                                print('Unknown property:', sub_property0['type'], raw_type, sub_property0)
                                exit(-1)
                else:
                    fmt_name = format_key(property0['name'], max_length)
                    tmp_keys.append(fmt_name)
                    raw_type = property0['raw_type']
                    self._check_raw_type(raw_type)
                    if 0 == property0['array'] and 'char' == raw_type:
                        raw_type = 'unsigned char'
                    if property0['raw_type'] == property0['type']:
                        keys.append((fmt_name, property0['name'], raw_type))
                    else:
                        if property0['type'] in self.enums_:
                            keys.append((fmt_name, property0['name'], 'enum', property0['type']))
                        else:
                            print('Unknown property:', property0['type'], raw_type, property0)
                            exit(-1)

            if len(set(tmp_keys)) != len(tmp_keys):
                print("There are duplicate formatted key for datastruct: ", struct_id)
                exit(1)
            self.datastruct_property_dict[struct_id] = keys

    def _get_property(self, struct_id, member_var):
        properties = self.cpp_header.classes[struct_id]['properties']['public']
        for property0 in properties:
            if property0['raw_type'].startswith("::"):
                if not member_var.startswith(property0['name']):
                    continue
                sub_properties = property0['class']['properties']['public']
                for sub_property0 in sub_properties:
                    tmpName = property0['name']
                    tmpName += "."
                    tmpName += sub_property0['name']
                    if tmpName == member_var:
                        return sub_property0
            else:
                if property0['name'] == member_var:
                    return property0
        return None

    def get_property(self, struct_id, member_var, prop=None):
        prop0 = self._get_property(struct_id, member_var)
        if prop and len(prop) >= 1:
            if prop0 and prop in prop0:
                return prop0[prop]
            else:
                return None
        return prop0

    def checknfilter_keyntype(self, key, name, struct_id, filter_types, filter_keys, filter_key_id=True):
        if not isinstance(filter_types, list):
            filter_types = []
        if not isinstance(filter_keys, list):
            filter_keys = []

        res = False
        if not isinstance(key, tuple) or len(key) < 3:   # # for enum (that is 4-tuple)
            print(">> In %s, unexpected error for key: %s with data-struct: %s" % (name, key, struct_id))
            res = True
        if key[2] in filter_types:
            print(">> In %s, filtered key: %s by type!" % (name, key))
            res = True
        if key[1] in filter_keys:
            print(">> In %s, filtered key: %s by key!" % (name, key))
            res = True
        if filter_key_id and struct_id in self.key_id_map and key[1] == self.key_id_map[struct_id]:
            print(">> In %s, filtered key: %s by key_id!" % (name, key))
            res = True
        return res

    def create_cmakelists(self, libname):
        cmake_lists = """CMAKE_MINIMUM_REQUIRED(VERSION 3.4)

file(GLOB headers ${CMAKE_CURRENT_SOURCE_DIR} *.h)
file(GLOB sources ${CMAKE_CURRENT_SOURCE_DIR} *.cpp)

add_library(%s ${headers} ${sources})
"""
        self.writeToFile("CMakeLists.txt", cmake_lists % libname)

