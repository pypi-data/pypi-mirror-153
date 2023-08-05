#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com

import os
import yaml
from jinja2 import Environment as jjEnvironment
from jinja2 import FileSystemLoader as jjFileSystemLoader


class Render(object):
    def __init__(self, config_file, template_path='template', output_path='output'):
        with open(config_file, 'r', encoding='utf-8') as f:
            self.__config = yaml.full_load(f.read())
        self.__tmpl_dir = template_path if os.path.isdir(template_path) else os.path.dirname(template_path)
        self.__tmpl_file = None if os.path.isdir(template_path) else os.path.basename(template_path)
        self.__jjenv = jjEnvironment(loader=jjFileSystemLoader(self.__tmpl_dir))
        self.__output = output_path

    def render_file(self, tmpl_file=None):
        """
        渲染模板生成文件
        :param tmpl_file:
        :return:
        """
        if not tmpl_file and not self.__tmpl_file:
            return False
        if not tmpl_file:
            tmpl_file = self.__tmpl_file
        print('Render template: %s' % os.path.join(self.__tmpl_dir, tmpl_file))
        if os.path.isdir(self.__output):
            output_file = os.path.join(self.__output, tmpl_file)
        else:
            output_file = self.__output
        content = self.__jjenv.get_template(tmpl_file).render(self.__config)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print('\tSucceed to generate %s' % output_file)
        return True

    def render_all(self):
        """
        渲染目录下所有的模板
        :return:
        """
        print('Start to render template dir: %s' % self.__tmpl_dir)
        for tmpl_file in self.__jjenv.list_templates():
            self.render_file(tmpl_file=tmpl_file)
        print('\nComplete all')
        return True


if __name__ == '__main__':
    print('This is Python scripts')
