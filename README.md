# Cloud10
Cloud project autumn 2016

## TODO 
- [ ] Fake Dolfin XML
- [ ] REST API (Flask) 
- [ ] Orchestration (HEAT-template?)
- [ ] A file with the three tasks (GENERATE MESH, CONVERTER and CALCULATOR)
- [ ] Swift, needs to be able to upload and download the Gmsh-meshes, download Gmsh-meshes and upload and download the XML meshes
- [ ] Celery-Master (starts celery tasks (possibly chains them))  
- [ ] Chain, groups, chords.. etc which one is the best? <Paste>

##THE DIFFERENT PARTS

###REST API
**INPUT**:  <br />
angle_start : smallest anglemof attack (degrees)  <br />
angle_stop  : biggest angle of attack (degrees)  <br />
n_angles    : split angle_stop-angle_start into n_angles parts  <br />
n_nodes     : number of nodes on one side of airfoil  <br />
n_levels : number of refinement steps in meshing 0=no refinement 1=one time 2=two times etc...  <br />

* Starting process
* Fetching process
* Status of a process

**OUTPUT**: <br />
Parameters  


###MASTER
**INPUT:** <br />
Parameters <br />

**OUTPUT:** <br />
Parameters to GENERATE MESH celery worker

* Start everything
* Link together tasks

###Celery process GENERATE MESH 
This process is going to generate several different meshes by using Gmsh then store the result in Swift. 

* Send parameters to Gmsh and upload the result to Swift
* Potential authorisation 

###Celery process CONVERTER
This celery process gets mesh (the data) from Swift. This process uses dolfin-convert to convert the meshes into Dolfins XML and then stores it in Swift.  <br />
**WE CAN'T DO THIS RIGHT NOW BECAUSE OF ISSUES** (Link to python converter script https://people.sc.fsu.edu/~jburkardt/py_src/dolfin-convert/dolfin-convert.py)

* Download Gmsh-mesh from Swift 
* Convert to Dolfin XML by using a dolfin-converter (ships with FEniCS)
* Upload Dolfin XML to Swift
* Potential authorisation

###Celery process CALCULATOR 
This celery process gets the dolfin XML with the mesh data and runs this through airfoil (the calculator). 
**WE CAN'T DO THIS RIGHT NOW BECAUSE OF ISSUES**

* Download Dolfin XML from Swift
* Use Airfoil to calculate
* Not yet known what to do with result

###RESULT
* Need to know what the result looks like

### Worker dependencies
```bash
sudo add-apt-repository ppa:fenics-packages/fenics-1.6.x 
sudo apt-get update 
sudo apt-get install libdolfin1.6 gmsh python-pip
sudo pip install numpy
```
