####################################################################################################
# This is a developing code through jupyter notebook - see alternative version [name].py
####################################################################################################
#
# NEW_dump2smd.py
#
###         GOAL: convert standard dump.* files (from LAMMPS) to SMD- (machdyn-) compatible files
###  DESCRIPTION: SMD cannot create restart files, so alternatively a new input file could be made
#                from the dump files from smd.
### DEPENDENCIES: 
###   INPUT FILE: dump.*
#
###      AUTHORS: INRAE\Billy Jenkinson
###      CONTACT: william.jenkinson@agroparistech.fr
# 
### VERSIONS
#  $2022-01-13$ alpha version (modify_atom_type.py)
#
#
### LICENCE: GPL2 (please keep the header) 
### ORIGINAL FILE: (billy@LX-Willy2021):
### IMPROVEMENTS FROM V1 (20xx-xx-xx)
#   > N/A
#   > N/A
#   > N/A
### TODO
#   > Add original coordinates to data
#   > Add velocity (or investigate how to)
#   > Explore options for restart file, and what the dump file should look like
#   > Generalise aspects, the order of the variables, choosing the timestep etc.
#   > Investigate better methods for data manipulation in Python
####################################################################################################
import sys

scale = float(1) # sys.argv[2] -> 1
#atom_types = sys.argv[3]
file = "restart" # sys.argv[1] -> v3#call the first arguement
fname = "dump."+file
fname_mod = "dump."+file+"_mod"
print("6400") #call the first arguement


fdump = open(fname,"r")
fsmd_w = open(fname_mod,"w")

fsmd_a = open(fname_mod,"a")
fsmd_r = open(fname_mod,"r+")

#fsmd_r.truncate(0)
#fsmd_r.close()
#fsmd_r = open(fname_mod,"r")


file_list = list(file)




i = 0
for line in fdump.readlines():
    i += 1
    if i == 1:
        newline = line.replace("ITEM: TIMESTEP", "# The first line which is not read")
        fsmd_a.write(newline)
    elif i == 2:
        newline = "\n"
        fsmd_a.write(newline)
    elif i == 3:
        newline = ""
        fsmd_a.write(newline)
    elif i == 4:
        number_of_atoms = int(line)
        print(number_of_atoms)
        newline = "     "+line[:-1]+"  atoms\n"
        fsmd_a.write(newline)
    elif i == 5:
        newline = "      2 atom types\n\n"
        fsmd_a.write(newline)
    elif i == 6:
        newline = "     "+line[:-1]+"  xlo xhi\n"
        fsmd_a.write(newline)
    elif i == 7:
        newline = "     "+line[:-1]+"  ylo yhi\n"
        fsmd_a.write(newline)
    elif i == 8:
        newline = "     "+line[:-1]+"  zlo zhi\n\n"
        fsmd_a.write(newline)
    elif i == 9:
        properties_string = line
        properties_string = properties_string.split()
        fsmd_a.write("Atoms # tag type mol vfrac rmass radius contact_radius x y z x0 y0 z0\n")
        break
    else:
        fsmd_a.write(line)

fname_modproperties_string = properties_string[2:]




print(properties_string)
items = ["id", "type", "mol","c_vol", "mass", "radius", "c_contact_radius", "x", "y", "z"]

index = [0,0,0,0,0,0,0,0,0,0]


for item in items:
    if item not in properties_string:
        print("error, incomplete data to create a restart file")
        print("you're missing "+item)

for i, item in enumerate(items):
        index[i] = properties_string.index(item)

for i in [1,2,3]:
    index.append(index[-3])
    
print(index)

i = 0
fsmd_a.close
fsmd_a = open(fname_mod,"a")
fsmd_r.close()
fdump.close()

fsmd_r = open(fname_mod,"r+")
fdump = open(fname,"r")
count = len(fdump.readlines(  ))
fdump = open(fname,"r")
lines = fdump.readlines()


for i, line in enumerate(fsmd_r):
    if  "Atoms" in line:
        while i < count:
            numberstring = lines[i]
            #print(lines_r[n+9])
            split_string = numberstring.split()
            new_split_string = ['0','0','0','0','0','0','0','0','0','0','0','0','0']
            for j, ind in enumerate(index):
                new_split_string[j] = split_string[ind-2]
            new_split_string[2] = '1'
            new_string = ' '.join(new_split_string) #reconnect strings 0 to 8
            fsmd_a.write('\n         '+new_string)
            i += 1
        break
print(i)
fsmd_a.close()


fsmd_w.close()
fsmd_r.close()
fsmd_a.close()
fdump.close()
