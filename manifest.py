#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate the Pizza3.manifest
"""

import os,datetime

manifest = "pizza3.manifest"
ignore = ['.manifest', ".py~", ".sh~", '.pyc',
          ".sample",".cache", ".xml", ".iml", ".zip", ".js"
         ".pdf", ".png", ".mp4", ".avi"]

file = open(manifest, 'w')

file.write("# Pizza3 manifest\n" + \
          f'# {datetime.datetime.now().strftime("%c")}\n\n')


# explore all files
for root, dirs, files in os.walk('./'):
   for name in files:       
       filename = os.path.join(root, name)
       if os.path.splitext(filename)[1] != '' and \
           os.path.splitext(filename)[1] not in ignore:
           file.write("%s\n" % filename)

file.close()