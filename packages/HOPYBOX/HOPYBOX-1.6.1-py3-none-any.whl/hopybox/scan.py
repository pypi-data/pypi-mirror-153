import os
import os.path
from rich import console,syntax

def scan(filename,extension,num=0,found_num=0):
  global scan_num,file_num
  scan_num = num
  file_num = found_num
  path = filename
  try:
    for item in os.listdir(path):
      scan_num+= 1
      file_extension = os.path.splitext(item)[1]
      if file_extension == extension:
        file_num+=1
        print('\033[94;1m'+str(file_num)+'\033[0m','\033[95m'+path+'/'+item+'\033[0m','\033[92m(Scanned:'+str(scan_num)+')\033[0m')
      new_item = path + '/' + item
      if os.path.isdir(new_item):
        scan(new_item,extension,scan_num,file_num)
  except:
    pass