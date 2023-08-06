import sys
from .ycmd import CMD

def main():
  cmd = CMD()
  if len(sys.argv) == 2:
    cmd.cmdrun_file(sys.argv[1])
  if len(sys.argv) == 2:
    cmd.cmdrun_method_file(sys.argv[1],sys.argv[2])
  if len(sys.argv) == 1:
    print("ファイルパスを指定してください")
