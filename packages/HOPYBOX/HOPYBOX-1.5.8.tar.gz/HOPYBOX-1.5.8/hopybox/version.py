import sys
from platform import system,python_version

version_number = 158
version_code = '1.5.8'
version_type = 'default'
# version_type = 'Beta'
gcc_version = sys.version.split(' ')[8].split(']')[0]

head_version = 'HOPYBOX {} ({}, May 29 2022, 12:54:01)\n[Python {}] on {}\nType "help" , "copyright" , "version" , "update" or "license" for more information'.format(version_code,version_type,python_version(),system())

def system_version():
  print('\033[96mHOPYBOX:{}\nPython:{}\nGCC:{}'.format(version_code,python_version(),gcc_version))