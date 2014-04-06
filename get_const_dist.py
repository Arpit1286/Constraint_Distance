# Author Arpit Tandon, atandon@email.unc.edu
# read the convergence of the constraints from the pdb files
##pdb files should be in a folder, be careful with the file names
##if needed just change the folder name or have it input from user

from os import listdir
import re

lrc_file = raw_input("enter constraint file name: ")
#distance function, read from the lists containing x,y and z coordinates
def distance(n1,n2):
    X_dist = (n1[0]-n2[0])**2
    Y_dist = (n1[1]-n2[1])**2
    Z_dist = (n1[2]-n2[2])**2
    distance = (X_dist + Y_dist + Z_dist)**(0.5)
    return distance

# read from the constraint file
file1 = open(lrc_file,'r')
lines_list = file1.readlines()
AT1 = []
AT2 = []
type1 = []
type2 = []
const_dist = []

for line in lines_list:
    each_line = re.split(r'[\t\s]\s*',line)   #use regular expression to split
    AT1.append(each_line[0])
    AT2.append(each_line[2])
    type1.append(each_line[1])
    type2.append(each_line[3])
    const_dist.append(float(each_line[6])+float(each_line[10]))

for i,string in enumerate(AT1):
    string = re.sub(r'[A]','',string)
    AT1[i]=string

for i,string in enumerate(AT2):
    string = re.sub(r'[A]','',string)
    AT2[i]=string
	
for i,type in enumerate(type1):
    if type == 'B':
        type1[i]='O'
    elif type == 'S':
        type1[i]='C'

for i,type in enumerate(type2):
    if type == 'B':
        type2[i]='O'
    elif type == 'S':
        type2[i]='C'
file1.close()

#read the directory and pass the distances in a dictionary
distance_dict = {}
names = []
for filenames in listdir('./test_pdb'): 
    names.append(filenames)
    
# read the coordinates
for file_names in names:   
    file2 = open('./test_pdb/%s' %file_names ,'r')
    pdb_lines = []
    pdb_lines = file2.readlines()
    dist = []
    Atom1 = {}
    Atom2 = {}
    # list for passing into distance function
    n1 = []
    n2 = []
            
    for lines in pdb_lines:
        pdb_line = re.split(r'[\t\s]\s*',lines)
        if pdb_line[0]=='ENDMDL':  #use continue there are lot of conditions to fulfill
            continue
        for i in range(0,len(AT1)):
            if AT1[i] == pdb_line[5] and type1[i] == pdb_line[2]:
                key_value=int(pdb_line[5])
                Atom1[key_value]=[]
                Atom1[key_value].append(float(pdb_line[6]))
                Atom1[key_value].append(float(pdb_line[7]))
                Atom1[key_value].append(float(pdb_line[8]))
        
        for i in range(0,len(AT2)):
            if AT2[i] == pdb_line[5] and type2[i] == pdb_line[2]:
                key_value=int(pdb_line[5])
                Atom2[key_value]=[]
                Atom2[key_value].append(float(pdb_line[6]))
                Atom2[key_value].append(float(pdb_line[7]))
                Atom2[key_value].append(float(pdb_line[8]))
                    
    for i in range(0,len(AT1)):
        n1 = Atom1[int(AT1[i])]  
        n2 = Atom2[int(AT2[i])] 
        dist_i = distance(n1,n2)
        dist.append(dist_i)    
        distance_dict[file_names]=dist
    file2.close()
file1.close()

for key in distance_dict:
    for i in range(0,len(AT1)):
        output_file = open('out%s.txt'%(i),'a+')
        output_file.write(str(distance_dict[key][i])+"\n")
        output_file.close()

#this will print single column text file for each constraint
# use any stat tool for doing analysis the single columns. The script
# is not perfect but I wrote it on a hunch
