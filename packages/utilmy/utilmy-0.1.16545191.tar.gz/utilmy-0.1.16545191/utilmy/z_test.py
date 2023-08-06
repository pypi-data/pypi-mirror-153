# -*- coding: utf-8 -*-
import os, sys, numpy as np


#####################################################################
def google_doc_string_example(package:str="mlmodels.util", name:str="path_norm"):
  """function load_function
  Args:
      package:   package name
      name:      name in string 
  Returns:
      A list of string
      
  """
  import importlib
  return  getattr(importlib.import_module(package), name)




