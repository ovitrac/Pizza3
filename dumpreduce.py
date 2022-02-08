#!/usr/bin/env python3

# dumpreduce.py
# command to reduce dump files to a prescribed number of frames (20)

# INRAE\Olivier Vitrac, INRAE\William Jenkinson - rev. 2022/02/02

# History
# 2022-02-02 RC
# 2022-02-02 add lock file (authorize concurrent executions on the same folder)

# contacts: olivier.vitrac@agroparistech.fr


"""
Usage:
dumpreduce dump.mysimulation
dumpreduce `find . -type f -iname 'dump*'  -printf '"%p" '`  
find . -type f -iname 'dump*'  -printf '"%p" ' | xargs -i{} dumpreduce {}
find . -type f -iname 'dump*' -exec dumpreduce "{}" \;

Complex search
find /Data/billy/ -type f -iname 'dump*' -size +5M ! \( -name "*.html" -o -name "*.py*" \)
dumpreduce `find . -type f -iname 'dump*' -size +5M ! \( -name "*.html" -o -name "*.py*" \)  -printf '"%p" '`

Convert all in this directory
dumpreduce `find . -type f -iname 'dump.*' ! \( -name "*.lite"
    -o -name "*.html" -o -name "*.py*" -o -name "*.txt" -o -name "*.tar*"
    -o -name "*.zip" -o -name "*.7z" \)`




---- Source folder

The following file structure is assumed
    |--- host directory
    |------------- dumpreduce.py                (mandatory)
    |-------------  pizza\                      (mandatory)
    |-------------------------- dump3.py        (mandatory)


"""


# %% Dependencies
# External dependencies
import os,  sys

# Dependencies
from pizza.dump3 import dump

# %% constants
extension = ".lite"
maxframes = 20
overwrite = False
lockprefix = ".~lock."

# %% touch like
# source: https://stackoverflow.com/questions/1158076/implement-touch-using-python 
def touch(fname, mode=0o666, dir_fd=None, **kwargs):
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(fname, flags=flags, mode=mode, dir_fd=dir_fd)) as f:
        os.utime(f.fileno() if os.utime in os.supports_fd else fname,
            dir_fd=None if os.supports_fd else dir_fd, **kwargs)

# %% loop on all files
nfiles = len(sys.argv)
ifile = 0
if nfiles:
    for tmp in sys.argv:
        dmpfile = str(tmp)
        lockdmpfile = lockprefix + dmpfile
        outfile = dmpfile + extension
        ifile +=1
        if os.path.isfile(dmpfile):
            if (not os.path.isfile(outfile)) or overwrite:
                print('[%d/%d] Processing dump file "%s"...'
                      % (ifile,nfiles,dmpfile) )
                if not os.path.isfile(lockdmpfile):
                    touch(lockdmpfile)      # lock file before processing it
                    X = dump(dmpfile)       # parse the file
                    X.tselect.all()         # select all frames
                    nframes = len(X.time()) # number of frames
                    skip_length = nframes // maxframes # floor division
                    if skip_length: X.tselect.skip(skip_length)
                    if overwrite: os.remove(outfile)   # remove the output file if overwrite
                    X.write(outfile)        # save selected frames
                    os.remove(lockdmpfile)  # unlock the input file
                else:
                    print('skipped, unlock the file with: rm "%s"' % dmpfile)
            else:
                print('[%d/%d] The file "%s" has been already converted, skipped'
                      % (ifile,nfiles,dmpfile) )
        else:
            print('WARNING: the file "%s" does not exist' % dmpfile)   
else:
    print("no file supplied")
    
