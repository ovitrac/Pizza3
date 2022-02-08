#!/usr/bin/env python3

# restartsmd2smd.py
# Command to restart an SMD dump to an SMD dump
"""

"""
# INRAE\Olivier Vitrac, INRAE\William Jenkinson - rev. 2022/02/02

# History
# 2022-02-02 RC
# 2022-02-02 add lock file (authorize concurrent executions on the same folder)

# contacts: olivier.vitrac@agroparistech.fr


"""

The following file structure is assumed
    |--- host directory
    |------------- dumpreduce.py                (mandatory)
    |-------------  pizza\                      (mandatory)
    |-------------------------- dump3.py        (mandatory)
    |-------------------------- data3.py        (mandatory)


DESCRIPTION:

For this command, I imagine lammps has dumped a file dedicated for restarts
The dumpfile in question should have minimal redundant information, and
columns be formatted identically to the structure of SMD input file, plus the 
velocities appended i.e.:
    
    #in lammps
    dump            dump_restart all custom 1000 dump.restart id type mol c_vol mass &
                radius c_contact_radius x y z x y z vx vy vz
    dump_modify     dump_restart first yes

The format of this dump file is as follows:
    
   ITEM: TIMESTEP
   0
   ITEM: NUMBER OF ATOMS
   228078
   ITEM: BOX BOUNDS pp ff pp
   0.0000000000000000e+00 6.6600000000000000e+02
   0.0000000000000000e+00 3.6600000000000000e+02
   0.0000000000000000e+00 1.0000000000000000e+00
   ITEM: ATOMS id type mol c_vol mass radius c_contact_radius x y z xu yu zu vx vy vz
   209846 4 5 1 1000 2.1 0.7 2 2 0 2 2 0
   209845 4 5 1 1000 2.1 0.7 1 2 0 1 2 0
   209844 4 5 1 1000 2.1 0.7 0 2 0 0 2 0
   ........................................

For now, I will consider the entirety of the simulation rather than
different components of sub regions

The format of the restart file is as follows:

   #Lammps restart file
   228078 atoms
   5 atom types
   0.000000000000     666.000000000000  xlo xhi
   0.000000000000     366.000000000000  ylo yhi
   0.000000000000       1.000000000000  zlo zhi

   Atoms #id type mol c_vol mass radius c_contact_radius x y z xu yu zu
   
   209846 4 5 1 1000 2.1 0.7 2 2 0 2 2 0 0 0 0
   209845 4 5 1 1000 2.1 0.7 1 2 0 1 2 0 0 0 0
   209844 4 5 1 1000 2.1 0.7 0 2 0 0 2 0 0 0 0
   ..............................
   
   Velocities #id vx vy vz
   209846 0 0 0
   209845 0 0 0
   209844 0 0 0
   ................



"""




# %% dependencies
# external dependencies
import datetime ; import os
import numpy as np

#Dependencies
from pizza.dump3 import dump
from pizza.data3 import data


# %% constants
dumpfile = "./data/play_data/dump.play.restartme"   # dump being restarted
step = 2000                                         # timestep to restart from
restartfile = "./data/play_data/data.play.RESTART"  # name of restart file
tmp_file = datetime.datetime.now().strftime("%y%m%d_%H%M%S") # temp file
name_check = {
    'id': 0, 'type': 1, 'mol': 2, 'c_vol': 3, 'mass': 4, 
    'radius': 5, 'c_contact_radius': 6, 
    'x': 7, 'y': 8, 'z': 9, 'xu': 10, 'yu': 11, 'zu': 12, 
    'vx': 13, 'vy': 14, 'vz': 15
    }

# %% Create dump object and extract necessary data
if os.path.isfile(dumpfile):
    print('Creating dump object ...')
    X = dump(dumpfile)                                  # create dump object
    try:
        print('Selecting timestep: %s' % step)
        X.tselect.one(step)                             # select frame from object
    except:
        print('WARNING: the timestep "%d" does not exist' % step)
else:
    print('WARNING: the file "%s" does not exist' % dumpfile)   

#test to ensure all data is available before continuing
print('Checking all necessary data is available...')
if name_check == X.names:
    print('Columns are correct')
else:
    print('WARNING: columns in dump object do not match expected columns: \n Expected:  '+','.join(list(name_check.keys()))+'\n Actual:    '+",".join(list(X.names.keys())))
    raise ValueError('Stopping')
    
# to retrieve system data such as simulation box dimensions and number of atoms
try:
    time,box,atoms,bonds,tris,lines = X.viz(1,1)
except:
    print('WARNING: data is missing from this dump, exiting restart')

# %% Create data object and fill the header
Y = data() # generates a new data file
# set the header values
Y.headers["xlo xhi"] = (box[0], box[3]); Y.headers["ylo yhi"] = (box[1], box[4]); Y.headers["zlo zhi"] = (box[2], box[5])
Y.headers["atoms"] = len(atoms)
m1, m2 = X.minmax("type") # retrieve the number of atom types
Y.headers["atom types"] = int(m2)

# %% Create Atoms section
# cut the atom data from the selected frame of the dump file
X.write(tmp_file,0,0); X_r = open(tmp_file,"r"); os.remove(tmp_file)
atom_data = X_r.readlines()
# print the atom data to the new data file
Y.sections["Atoms"] = atom_data
mol = Y.get("Atoms",3); mol = np.array(mol, dtype='int'); mol = mol.tolist()
Y.replace("Atoms",3,mol) 
Y.reorder("Atoms", 1,2,3,4,5,6,7,8,9,10,11,12,13) # deletes column 14, 15, 16

# %% Create Velocities section
Y.sections["Velocities"] = atom_data
Y.reorder("Velocities", 1, 14, 15, 16) # delete !columns 1, 14, 15, 16

# %% Write the restart file
Y.write(restartfile)
