
import os
import time
from Pras_Server.PRAS import repairPDB 
from Pras_Server.FixHeavyAtoms import fixheavyAtoms
from Pras_Server.RamaChandra import ramachandranTypes
from Pras_Server.SecondaryStructure import assignStructure

# Note that some of the PDB files have 5 to 7 chains
# and each chain will be analyzed (SS assignment and ramachandran plots).
# PRAS over-writes each ouput file except the chain number is such that
# other output are less than the number (i.e., if there's only one PDB file
# with sec_strc_plot_chain5.TIF it cannot be over-written ecxcept another file has up to 5 chains)

startTime = time.time()

for i in os.listdir(os.getcwd()):
	if  i[-3:] == 'ent':

		#print(repairPDB.__doc__) to understand the arguments
		fixheavyAtoms(i, "", "" ,"")

		#out_no_h.pdb is the repaired PDB file written by PRAS
		assignStructure('out_no_h.pdb')

		#out_no_h.pdb same as above
		ramachandranTypes('out_no_h.pdb')

		print("fixed {}".format(i))
		#uncomment if you want to remove each processed file
		#os.remove(i)	
print ('The program took {0} second !'.format(time.time() - startTime))
