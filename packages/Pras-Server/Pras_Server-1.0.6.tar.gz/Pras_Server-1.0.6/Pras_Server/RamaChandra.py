__doc__ = """
This program requires python 3.6 or higher.

print(functionName.__doc__) to see the 

documentation for the function or usage.

Send enquiries to osita@protein-science.com
"""
import itertools
import numpy as np
from . import ReadStructure
import matplotlib.pyplot as plt
from .ReadStructure import nextRes
from pkg_resources import resource_stream

def ramachandranTypes(filename, cmap = ""):
	"""
	This program plots 4 types of Ramanchandran 
	(general, glycine,proline,pre-proline) in TIF format 

	This funtion & the dependency (ReadStructure.py) read PRAS 
	output PDB file in a quick and complex manner. Since it is a 
	PRAS output there will not be error (missing atoms, bad format, etc).

	In general, this program can be used for any standard PDB file.
	However, if there are missing backbone C atoms or a bad format,
	this program will run into trouble. Thus, it is better to run the PDB
	through PRAS first and then use the PRAS output here.

	Arguments
	----------
	filename: PRAS generated PDB file

	cmap    : Colour for the plot (e.g, viridis,magma,inferno,jet,plasma)

	Returns
	-------
	None:  plots 4 types of  Ramanchandran in TIF format
	"""
	lines = open(filename, 'r').readlines()
	rf = [i.strip("\n") for i in lines if i[:4] == 'ATOM' or i[0:3] == "TER"]
	chains = [i for i,j in enumerate(rf) if j[:3].strip(' ')  == "TER"]

	count = 0
	for n in range(len(chains)):
		line = [i for i in list(itertools.chain(*[rf[count:i]for i,j in enumerate(rf) if i == chains[n]]))]
		i = ReadStructure.phiDihedral(line)
		j = ReadStructure.psiDihedral(line)

		general_phi    = [ i[l] for l,m in enumerate(nextRes(line)) if nextRes(line)[l] == 'General']
		general_psi    = [ j[l] for l,m in enumerate(nextRes(line)) if nextRes(line)[l] == 'General']
		glycine_phi    = [ i[l] for l,m in enumerate(nextRes(line)) if nextRes(line)[l] == 'Glycine']
		glycine_psi    = [ j[l] for l,m in enumerate(nextRes(line)) if nextRes(line)[l] == 'Glycine']
		preproline_phi = [ i[l] for l,m in enumerate(nextRes(line)) if nextRes(line)[l] == 'Pre-Pro']
		preproline_psi = [ j[l] for l,m in enumerate(nextRes(line)) if nextRes(line)[l] == 'Pre-Pro']
		proline_phi    = [ i[l] for l,m in enumerate(nextRes(line)) if nextRes(line)[l] == 'Proline']
		proline_psi    = [ j[l] for l,m in enumerate(nextRes(line)) if nextRes(line)[l] == 'Proline']

		if not cmap:
			cmap='viridis'
		alpha=0.75; dpi=100 
		fig, ax = plt.subplots(2,2,figsize=(9.5, 9), dpi=dpi)
		Z = np.fromfile(resource_stream(__name__, 'data/KD.dat'))
		Z = np.reshape(Z, (100, 100))

		ax[0, 0].set_aspect('equal')
		ax[0, 0].set_xlabel('φ')
		ax[0, 0].set_ylabel('ψ')
		ax[0, 0].set_xlim(-180, 180)
		ax[0, 0].set_ylim(-180, 180)
		ax[0, 0].set_xticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
		ax[0, 0].set_yticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
		ax[0, 0].set_title("General")

		ax[1, 0].set_aspect('equal')
		ax[1, 0].set_xlabel('φ')
		ax[1, 0].set_ylabel('ψ')
		ax[1, 0].set_xlim(-180, 180)
		ax[1, 0].set_ylim(-180, 180)
		ax[1, 0].set_xticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
		ax[1, 0].set_yticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
		ax[1, 0].set_title("Proline")

		ax[0, 1].set_aspect('equal')
		ax[0, 1].set_xlabel('φ')
		ax[0, 1].set_ylabel('ψ')
		ax[0, 1].set_xlim(-180, 180)
		ax[0, 1].set_ylim(-180, 180)
		ax[0, 1].set_xticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
		ax[0, 1].set_yticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
		ax[0, 1].set_title("Glycine")

		ax[1, 1].set_aspect('equal')
		ax[1, 1].set_xlabel('φ')
		ax[1, 1].set_ylabel('ψ')
		ax[1, 1].set_xlim(-180, 180)
		ax[1, 1].set_ylim(-180, 180)
		ax[1, 1].set_xticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
		ax[1, 1].set_yticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
		ax[1, 1].set_title("Pre-proline")

		data = np.log(np.rot90(Z))

		ax[0, 0].imshow(data, cmap=plt.get_cmap(cmap), extent=[-180, 180, -180, 180], alpha=alpha)
		ax[1, 0].imshow(data, cmap=plt.get_cmap(cmap), extent=[-180, 180, -180, 180], alpha=alpha)
		ax[0, 1].imshow(data, cmap=plt.get_cmap(cmap), extent=[-180, 180, -180, 180], alpha=alpha)
		ax[1, 1].imshow(data, cmap=plt.get_cmap(cmap), extent=[-180, 180, -180, 180], alpha=alpha)

		data = np.rot90(np.fliplr(Z))
		ax[0, 0].contour(data, colors='k', linewidths=0.5,
		           levels=[10 ** i for i in range(-7, 0)],
		           antialiased=True, extent=[-180, 180, -180, 180], alpha=0.65)
		ax[1, 0].contour(data, colors='k', linewidths=0.5,
		           levels=[10 ** i for i in range(-7, 0)],
		           antialiased=True, extent=[-180, 180, -180, 180], alpha=0.65)
		ax[0, 1].contour(data, colors='k', linewidths=0.5,
		           levels=[10 ** i for i in range(-7, 0)],
		           antialiased=True, extent=[-180, 180, -180, 180], alpha=0.65)
		ax[1, 1].contour(data, colors='k', linewidths=0.5,
		           levels=[10 ** i for i in range(-7, 0)],
		           antialiased=True, extent=[-180, 180, -180, 180], alpha=0.65)

		ax[0,0].scatter(general_phi, general_psi, marker='.', s=3, c="k")
		ax[1,0].scatter(proline_phi, proline_psi, marker='.', s=3, c="k")
		ax[0,1].scatter(glycine_phi, glycine_psi, marker='.', s=3, c="k")
		ax[1,1].scatter(preproline_phi, preproline_psi, marker='.', s=3, c="k")

		plt.savefig('ramachandra'+'_'+'chain'+str(n+1)+'.tif')
		plt.close(fig)

		if n == 0:
			count+= chains[n]+1
		else:
			count+= (chains[n]-chains[n-1])
