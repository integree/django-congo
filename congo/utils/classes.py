# -*- coding: utf-8 -*-
import importlib

def get_class(class_path):
    module_name, class_name = class_path.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)
