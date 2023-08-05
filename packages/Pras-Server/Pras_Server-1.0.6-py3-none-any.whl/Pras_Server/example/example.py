#computational time varies 
import time

#this function adds both heavy and H-atoms
from Pras_Server.PRAS import repairPDB 

#this function replaces only missing heavy atoms
from Pras_Server.FixHeavyAtoms import fixheavyAtoms
 
#this function draws the 4 ramachandran types
from Pras_Server.RamaChandra import ramachandranTypes 

#this function assigns the secondary structure elements
from Pras_Server.SecondaryStructure import assignStructure 

startTime = time.time()

#print(repairPDB.__doc__) to understand the arguments
fixheavyAtoms('1aho.pdb', "", "" ,"")

#out_no_h.pdb is the repaired PDB file written by PRAS
assignStructure('out_no_h.pdb')

#out_no_h.pdb same as above
ramachandranTypes('out_no_h.pdb')

print ('The program took {0} second !'.format(time.time() - startTime))