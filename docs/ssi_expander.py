#!/usr/bin/python3
'''
This script copies the files in one directory to another, expanding any SSI
<!-- #include --> statements it encounters along the way.
Only files that end in '.html' are processed. Copy or symlink anything else
manually.

Usage:

  ./ssi_expander.py [source_directory] destination_directory

If source_directory is not specified, then the current directory is used.
'''

import os
import pathlib
import ssi
import sys

def process(source, dest):
  for dirpath, dirnames, filenames in os.walk(source):
    dest_dir = os.path.realpath(os.path.join(dest, os.path.relpath(dirpath, source)))
    if not os.path.exists(dest_dir):
      os.mkdir(dest_dir)
    assert os.path.isdir(dest_dir)
    for filename in filenames:
      if not filename.endswith('.html'):
        continue
      src_path = os.path.abspath(os.path.join(source, dirpath, filename))
      dest_path = os.path.join(dest_dir, filename)
      pathlib.Path(dest_path).unlink(missing_ok=True)
      with open(dest_path, 'wb') as f:
        f.write(ssi.InlineIncludes(src_path))

    # ignore hidden directories
    for dirname in dirnames[:]:
      if dirname.startswith('.'):
        dirnames.remove(dirname)


if __name__ == '__main__':
  if len(sys.argv) == 2:
    source = '.'
    dest = sys.argv[1]
  elif len(sys.argv) == 3:
    source, dest = sys.argv[1:]
  else:
    sys.stderr.write('Usage: %s [source_directory] destination_directory\n' % sys.argv[0])
    sys.exit(1)

  process(source, dest)
