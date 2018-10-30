# -*- coding: utf-8 -*-
import os.path
import json


def loadJson(fname):
    fp = open(fname, 'r')
    j_data = json.load(fp)
    fp.close()
    return j_data


def saveJson(fname, obj, verbose=False):
    fp = open(fname, 'w')
    json.dump(obj, fp, indent=4, sort_keys=True)
    fp.close()
    if verbose:
        print('>>> Save json data to file: %s' % fname)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Update Json File (assuming Json files are dict)')
    parser.add_argument('-v', '--verbose', action='store_true', help='print verbose information.')
    parser.add_argument("-t", "--update-type", dest='update_type', default='update_all',
                            choices=['update_all', 'overwrite_exist', 'keep_exist'],
                            help="update type (how to update new data by using old data), default:update_all")
    parser.add_argument("json_file", nargs=2, help='old_json_file new_json_file')
    opts = parser.parse_args()

    if len(opts.json_file) < 2:
        print('>>> We need at least two json file to proceed!')
        print(parser.usage)
        exit(-1)

    assert os.path.isfile(opts.json_file[0]) and os.path.isfile(opts.json_file[1])    
    data_old = loadJson(opts.json_file[0])
    data_new = loadJson(opts.json_file[1])
    if opts.verbose:
        print('>>> update_type is %s' % opts.update_type)
    if 'update_all' == opts.update_type:
        data_new.update(data_old)
    elif 'keep_exist' == opts.update_type:
        for key_id in data_old:
            if key_id not in data_new:
                data_new[key_id] = data_old[key_id]
                if opts.verbose:
                    print('>>> Add key_id %s from old_data.' % key_id)
    elif 'overwrite_exist' == opts.update_type:
        for key_id in data_old:
            if key_id in data_new:
                data_new[key_id] = data_old[key_id]
                if opts.verbose:
                    print('>>> update key_id %s from old_data' % key_id)

    saveJson(opts.json_file[1], data_new, verbose=opts.verbose)
