import os
import subprocess
import sys


def main():
  command = os.path.join(
      os.path.dirname(os.path.realpath(__file__)), 'sourcery')
  return subprocess.call([command, *sys.argv[1:]], bufsize=0)
