# Cloud10
Cloud project autumn 2016

##TO DO 


###REST API
* INPUT: 
 ** angle_start : smallest anglemof attack (degrees)
 ** angle_stop  : biggest angle of attack (degrees)
 ** n_angles    : split angle_stop-angle_start into n_angles parts
 ** n_nodes     : number of nodes on one side of airfoil
 ** n_levels : number of refinement steps in meshing 0=no refinement 1=one time 2=two times etc...
* OUTPUT: Parameters 
* Sends parameters to Master

###MASTER

###Celery process GENERATE MESH 
* Parameters generates several MESH

###Celery process CONVERTER

###Celery process CALCULATOR

###RESULT
* Need to know what the result looks like

