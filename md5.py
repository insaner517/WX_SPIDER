#!/usr/bin/env python             
#coding : utf-8
import sys
import os
import hashlib

def get_md5(file_path):
  md5 = None
  if os.path.isfile(file_path):
    f = open(file_path,'rb')
    md5_obj = hashlib.md5()
    md5_obj.update(f.read())
    hash_code = md5_obj.hexdigest()
    f.close()
    md5 = str(hash_code).lower()
  return md5

if __name__ == "__main__":
  file_path = sys.argv[1]
  md5 = get_md5(file_path)
  print(md5)