# Cloud10
Cloud project autumn 2016

##TO DO 
* Fake Dolfin XML


##THE DIFFERENT PARTS

###REST API
**INPUT**:  <br />
angle_start : smallest anglemof attack (degrees)  <br />
angle_stop  : biggest angle of attack (degrees)  <br />
n_angles    : split angle_stop-angle_start into n_angles parts  <br />
n_nodes     : number of nodes on one side of airfoil  <br />
n_levels : number of refinement steps in meshing 0=no refinement 1=one time 2=two times etc...  <br />

**OUTPUT**: <br />
Parameters  


###MASTER
**INPUT:** <br />
Parameters <br />

**OUTPUT:** <br />
Parameters to GENERATE MESH celery worker

###Celery process GENERATE MESH 
This process is going to generate several different meshes by using Gmsh then store the result in Swift. 

###Celery process CONVERTER
This celery process gets mesh (the data) from Swift. This process uses dolfin-convert to convert the meshes into Dolfins XML and then stores it in Swift.  <br />
**WE CAN'T DO THIS RIGHT NOW BECAUSE OF ISSUES**

###Celery process CALCULATOR (AIRFOIL) 
This celery process gets the dolfin XML with the mesh data and runs this through airfoil (the calculator). 
**WE CAN'T DO THIS RIGHT NOW BECAUSE OF ISSUES**

###RESULT
* Need to know what the result looks like

