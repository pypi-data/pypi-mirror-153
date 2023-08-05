import sys
from platform import system,python_version

version_number = 161
version_code = '1.6.1'
version_type = 'default'
# version_type = 'Beta'
try:
  gcc_version = sys.version.split(' ')[8].split(']')[0]
except:
  gcc_version = 'Failed'

head_version = 'HOPYBOX {} ({}, May 30 2022, 12:54:01)\n[Python {}] on {}\nType "help" , "copyright" , "version" , "update" or "license" for more information'.format(version_code,version_type,python_version(),system())

def system_version():
  print('\033[96mHOPYBOX:{}\nPython:{}\nGCC:{}'.format(version_code,python_version(),gcc_version))