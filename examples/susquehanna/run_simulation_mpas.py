import os, sys
from pathlib import Path
from os.path import realpath

from pyflowline.pyflowline_read_model_configuration_file import pyflowline_read_model_configuration_file


sPath_data = str(Path(__file__).parents[2]) # data is located two dir's up
sWorkspace_data = realpath( sPath_data +  '/data/susquehanna' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')

sPath = str( Path().resolve() )
sSlurm = 'short'
sWorkspace_output = '/compyfs/liao313/04model/pyflowline/susquehanna'
sFilename = sWorkspace_output + '/' +  'mpas.bash'
ofs = open(sFilename, 'w')
sLine  = '#!/bin/bash' + '\n'
ofs.write(sLine)

sFilename_configuration_in = realpath( sPath +  '/examples/susquehanna/pyflowline_susquehanna_mpas.json' )
if os.path.isfile(sFilename_configuration_in):
    pass
else:
    print('This configuration does not exist: ', sFilename_configuration_in )

iFlag_visualization =0 
iCase_index = 1
sMesh_type = 'mpas'
sDate='20220630'

#visualization spatial extent
aExtent_full = [-78.5,-75.5, 39.2,42.5]
aExtent_meander = [-76.5,-76.2, 41.6,41.9] #meander
aExtent_braided = [-77.3,-76.5, 40.2,41.0] #braided
aExtent_confluence = [-77.3,-76.5, 40.2,41.0] #confluence
aExtent_outlet = [-76.0,-76.5, 39.5,40.0] #outlet
aExtent_dam = [-75.75,-76.15, 42.1,42.5] #dam     


oPyflowline = pyflowline_read_model_configuration_file(sFilename_configuration_in, \
    iCase_index_in=iCase_index, sDate_in=sDate)
oPyflowline.aBasin[0].dLatitude_outlet_degree=39.462000
oPyflowline.aBasin[0].dLongitude_outlet_degree=-76.009300
oPyflowline.create_hpc_job(sSlurm_in = sSlurm )  
    
sLine  = 'cd ' + oPyflowline.sWorkspace_output + '\n'
ofs.write(sLine)
sLine  = 'sbatch submit.job' + '\n'
ofs.write(sLine)        


if iFlag_visualization == 1:
    sFilename =  'filtered_flowline.png'
    oPyflowline._plot(sFilename, sVariable_in = 'flowline_filter', aExtent_in =aExtent_full  )
    
    sFilename =  'conceptual_flowline_with_mesh.png'
    oPyflowline._plot(sFilename,  iFlag_title=1 ,sVariable_in='overlap',   aExtent_in =aExtent_full )  
    
    sFilename =  'meander.png'
    oPyflowline._plot(sFilename, iFlag_title=0, sVariable_in='overlap',    aExtent_in =aExtent_meander )    

    sFilename =  'braided.png'
    oPyflowline._plot(sFilename, iFlag_title=0, sVariable_in='overlap',    aExtent_in =aExtent_braided )    

    sFilename =  'confluence.png'
    oPyflowline._plot(sFilename, iFlag_title=0, sVariable_in='overlap',    aExtent_in =aExtent_confluence )    

    sFilename =  'outlet.png'
    oPyflowline._plot(sFilename, iFlag_title=0, sVariable_in='overlap',    aExtent_in =aExtent_outlet )         

    sFilename =  'area_of_difference.png'
    oPyflowline._plot( sFilename,sVariable_in = 'aof',  aExtent_in=aExtent_full)
    pass

ofs.close()
print('Finished')