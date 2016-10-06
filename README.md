# Cloud10
Cloud project autumn 2016

##TO DO 


###REST API
**INPUT**:  <br />
angle_start : smallest anglemof attack (degrees)  <br />
angle_stop  : biggest angle of attack (degrees)  <br />
n_angles    : split angle_stop-angle_start into n_angles parts  <br />
n_nodes     : number of nodes on one side of airfoil  <br />
n_levels : number of refinement steps in meshing 0=no refinement 1=one time 2=two times etc...  <br />

**OUTPUT**: Parameters  


###MASTER
**INPUT:** <br />
Parameters <br />

**OUTPUT:** <br />
Parameters to GENERATE MESH celery worker

###Celery process GENERATE MESH 
This process is going to generate several different meshes 

###Celery process CONVERTER

###Celery process CALCULATOR (AIRFOIL) 

###RESULT
* Need to know what the result looks like

