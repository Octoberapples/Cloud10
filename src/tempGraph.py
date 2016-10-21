import numpy as np


"""Build a matplotlib graph of angle on x axis and drag/lift on y axis will sort them to correspond to eachother..
   Saves the file in the folder static

"""
def buildGraph(angles,y_axis,type):

    angles, y_axis = zip(*sorted(zip(angles, y_axis))) #Sort angles and sorts y_axis based on angles...
    import matplotlib.pyplot as plt

    plt.ioff()
    plt.plot(angles,y_axis, label="Mean " + type)
    plt.xlabel('Angle')
    plt.title('Results produced by the airfoil application')
    plt.grid(True)
    
    plt.legend(fancybox=True, shadow=True)
    location = "static/"+type+".png"
    plt.savefig(location)
    plt.close()
    return location


""" 
@app.route('/', methods=['POST'])
def data_post():

Should be changed in flaskAPI.py :

    imgsrc,imgsrc1 = t.get()
    return render_template('result.html', filename=imgsrc, filename1=imgsrc1)
 """

"""Example on slightly unsorted list.. """

angle = [21,20,22,23,24,25,26,27,28,29]
lift = [24.50,22.13,25.80,26.62,27.82,28.28,28.22,29.97,30.37,31.45]
drag = [246.29,242.49,244.64,244.64,244.34,243.59,244.14,243.96,243.46,243.90]


imgsrc = buildGraph(angle,lift,"Lift")
imgsrc1 =buildGraph(angle,drag,"Drag")

print imgsrc
print imgsrc1
