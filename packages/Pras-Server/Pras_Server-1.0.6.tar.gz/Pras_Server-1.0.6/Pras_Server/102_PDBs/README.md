Whilst in this folder, execute test_102pdb.py

to run/analyze all 102 PDB files in this folder.

This test with these randomly selected

PDB files is used to show that the code is bug free

to the extent it has been tested. 

All 102 PDBs were processed sucessfully during our test.

If you notice a bug, kindly send a message to osita@protein-science.com


## PERFORMING THIS TEST  ON WINDOWS SUBSYSTEM FOR LINUX (WSL)


In order to run Linux GUI applications e.g., the plots involving 
assignStructure('out_no_h.pdb') and ramachandranTypes('out_no_h.pdb')
using Windows Subsystem for Linux (WSL), you must install X server for Windows.

Thus, you need to:

Install X server for Windows

Configure bash to tell GUIs to use the local X server

For X server, install VcXsrv which is open source by downloading from https://sourceforge.net/projects/vcxsrv/

Configure bash to use the local X server. In bash run:

`echo "export DISPLAY=localhost:0.0" >> ~/.bashrc`

To have the configuration changes take effect, restart bash, or run:

`. ~/.bashrc`

Then open VcXsrv from your taskbar (you should send the icon to taskbar for easy access).
Note that VcXsrv must be open/running each time you use plotting tools in WSL
