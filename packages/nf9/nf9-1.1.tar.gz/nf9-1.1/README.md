# nf9

A high level module to allow one to quickly display images from Python that relies on the pyds9 module (https://github.com/ericmandel/pyds9)


# Installing: #
```
pip install nf9
```

or clone github depo and
```
python setup.py install
```

# Sample Usage: #
```
import nf9

# Display a file
nf9.disp("file.fits",1)

# Display a numpy array
arr = np.ones((100,100))
nf9.disp(arr,1)

# Display catalog in DS9
xs = [10,100,20]
ys = [20,20,100]
nf9.tvm(x=xs,y=ys,frame=1,circle=20, color='Red')

# Read value from DS9
i,j,v = nf9.imexam(frame=1) 
```