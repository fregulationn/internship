# -*- coding: utf-8 -*-
"""
File Name：     __init__.py
Author :       peng.he
-------------------------------------------------
"""
import importlib
import os


def load_settings():
    t = os.environ.get('INTELLI_EXTRACT_SENTENCE_PROFILE', 'dev')
    module = 'rest.settings.{}'.format(t)
    if module != 'rest.settings.online':
        print('==============================')
        print('Using {} as settings'.format(module))
        print('==============================\n')
    settings = importlib.import_module(module)
    return settings


settings = load_settings()
