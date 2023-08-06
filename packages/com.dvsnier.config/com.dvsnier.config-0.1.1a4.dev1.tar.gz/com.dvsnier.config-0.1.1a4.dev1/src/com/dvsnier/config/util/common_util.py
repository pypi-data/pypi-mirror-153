# -*- coding:utf-8 -*-

import os
import time


def generate_complex_file_name(output_dir_name, file_name):  # type: (str, str) -> str
    'the generate complex file name'
    output_dir = mk_output_dir(output_dir_name)
    name = str("%s_%s.log" % (file_name, int(time.time())))
    return os.path.join(output_dir, name)


def mk_output_dir(output_dir_name):  # type: (str) -> str
    'the initialize output dir'
    # root_dir = os.path.dirname(os.path.abspath('.'))
    # logging.debug('the current root_dir is %s' % root_dir)
    project_dir = os.path.abspath('.')
    # logging.debug('the current project_dir is %s' % project_dir)
    # src_dir = os.path.join(project_dir, 'src')
    # logging.debug('the current src_dir is %s' % src_dir)
    out_dir = os.path.join(project_dir, 'out')
    # logging.debug('the current out_dir is %s' % out_dir)
    output_dir = os.path.join(out_dir, output_dir_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # logging.debug('the current output_dir is %s' % output_dir)
    return output_dir
