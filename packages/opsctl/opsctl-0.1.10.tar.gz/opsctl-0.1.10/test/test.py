#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com

import subprocess
import os
import json
import yaml


def shell_cmd(cmd):
    print('\n# %s' % cmd)
    _status_code, _output = subprocess.getstatusoutput(cmd)
    print(_output)
    return [_status_code, _output]


def setup():
    for tmpfile in os.listdir('.'):
        if tmpfile.startswith('case') or tmpfile == 'tmpl.yml':
            shell_cmd('rm -rf %s' % tmpfile)


def teardown():
    setup()


def test_case_1():
    status_code, output = shell_cmd('opsctl')
    assert status_code == 1
    assert 'version' in output
    assert 'tmpl2art' in output
    assert 'env2json' in output
    assert 'env2yaml' in output

    status_code, output = shell_cmd('opsctl version')
    assert status_code == 0
    assert 'opsctl v0.0.1' in output

    status_code, output = shell_cmd('opsctl tmpl2art')
    assert status_code == 1
    assert '--config' in output
    assert '--tmpl' in output
    assert '--output' in output

    status_code, output = shell_cmd('opsctl env2json')
    assert status_code == 1
    assert '--input' in output
    assert '--output' in output

    status_code, output = shell_cmd('opsctl env2yaml')
    assert status_code == 1
    assert '--input' in output
    assert '--output' in output


def test_case_2():
    status_code, output = shell_cmd(' '.join([
        'opsctl tmpl2art',
        '--config config/env.yaml',
        '--tmpl template',
        '--output .'
    ]))
    assert status_code == 0
    shell_cmd('cat tmpl.yml')

    status_code, output = shell_cmd(' '.join([
        'opsctl tmpl2art',
        '--config config/env.yaml',
        '--tmpl template',
        '--output case2-1.yaml'
    ]))
    assert status_code == 1

    status_code, output = shell_cmd(' '.join([
        'opsctl tmpl2art',
        '--config config/env.yaml',
        '--tmpl template/tmpl.yml',
        '--output case2-2.yaml'
    ]))
    assert status_code == 0
    shell_cmd('cat case2-2.yaml')

    os.makedirs('case2-3')
    status_code, output = shell_cmd(' '.join([
        'opsctl tmpl2art',
        '--config config/env.yaml',
        '--tmpl template/tmpl.yml',
        '--output case2-3'
    ]))
    assert status_code == 0
    shell_cmd('cat case2-3/tmpl.yml')


def test_case_3():
    status_code, output = shell_cmd(' '.join([
        'opsctl env2json',
        '--output case3-1.json'
    ]))
    assert status_code == 0
    with open('case3-1.json', 'r') as f:
        assert json.dumps(f.read())

    status_code, output = shell_cmd(' '.join([
        'opsctl env2json',
        '--output case3-2.json',
        '--input case3env'
    ]))
    assert status_code == 1

    status_code, output = shell_cmd('env > case3env')
    assert status_code == 0
    status_code, output = shell_cmd(' '.join([
        'opsctl env2json',
        '--output case3-3.json',
        '--input case3env'
    ]))
    assert status_code == 0
    with open('case3-3.json', 'r') as f:
        assert json.dumps(f.read())

    status_code, output = shell_cmd(' '.join([
        'opsctl env2json',
        '--output case3dir/case3-4.json',
        '--input case3env'
    ]))
    assert status_code == 1


def test_case_4():
    status_code, output = shell_cmd(' '.join([
        'opsctl env2yaml',
        '--output case4-1.yaml'
    ]))
    assert status_code == 0
    with open('case4-1.yaml', 'r') as f:
        assert yaml.safe_dump(f.read())

    status_code, output = shell_cmd(' '.join([
        'opsctl env2yaml',
        '--output case4-2.yaml',
        '--input case4env'
    ]))
    assert status_code == 1

    status_code, output = shell_cmd('env > case4env')
    assert status_code == 0
    status_code, output = shell_cmd(' '.join([
        'opsctl env2yaml',
        '--output case4-3.yaml',
        '--input case4env'
    ]))
    assert status_code == 0
    with open('case4-3.yaml', 'r') as f:
        assert yaml.safe_dump(f.read())

    status_code, output = shell_cmd(' '.join([
        'opsctl env2yaml',
        '--output case4dir/case4-4.yaml',
        '--input case4env'
    ]))
    assert status_code == 1


if __name__ == '__main__':
    print('This is pytest scripts')
