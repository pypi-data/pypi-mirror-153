import os
from astropy.io import fits
import pyds9 
import numpy as np
import string, random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


targets = pyds9.ds9_targets()
print("Found",targets)


if targets==None or len(targets)==0:
	ds9_id = id_generator()
else:
	ds9_id = targets[0]

print("Connecting to",ds9_id)
nf_ds9 = pyds9.DS9(ds9_id)


disp_z1 = None
disp_z2 = None
imhist_z1 = None
imhist_z2 = None

def check_dir():
	"""Ensure that DS( looks in the right place"""
	dir = os.getcwd()
	nf_ds9.set("cd %s" % (dir))

def reinit():
	nf_ds9 = pyds9.DS9(ds9_id)

def ext_parser(name):
	if "[" in name:
		filename = name.split("[")[0]
		ext = name.split("[")[-1].split("]")[0]
		try:
			ext = int(ext)
		except:
			pass
	else:
		filename = name
		ext = 0

	return filename,ext

def lock():
	check_dir()
	nf_ds9.set("lock frame image" )

def disp(f,frame=1,z1=None,z2=None,zoom=None):
	"""Display a file, a list of files or a numpy array into DS9, defaulting to frame 1. Data range can be specified with z1,z2 
	as well as a zoom factor"""
	global disp_z1
	global disp_z2

	check_dir()

	if type(f)==np.ndarray or type(f)==np.ma.core.MaskedArray:
		if frame!=None:
			nf_ds9.set("frame %d" % (frame))
		nf_ds9.set_np2arr(f)
		return

	if type(f)==type(" ") and "*" in f:
		import glob
		files = glob.glob(f.split("[")[0])
		ext = ""
		if len(f.split("["))>1:
			ext = "["+f.split("[")[1]

		files = [x+ext for x in files]
	else:
		ext = ""
		if len(f.split("["))>1:
			ext = "["+f.split("[")[1]
		files = [f]

	#print "files:",files,ext

	for i,f in enumerate(files):
		if i>0:
			frame = i+1
		if not os.path.isfile(f.split("[")[0]):
			print(f,"Not found")
			return

		if z1==None and disp_z1!=None:
			z1 = disp_z1
		if z1!=None:
			disp_z1 = z1

		if z2==None and disp_z2!=None:
			z2 = disp_z2
		if z2!=None:
			disp_z2 = z2
	
		if frame!=None:
			nf_ds9.set("frame %d" % (frame))
		nf_ds9.set("file %s" % (f))
		if z1==None and z2==None:
			nf_ds9.set("scale zscale")

		#print "check:",z1,z2
		if z1!=None and z2!=None:
			nf_ds9.set("scale limits %e %e" % (z1,z2))
		if zoom!=None:
			nf_ds9.set("zoom to %d" % (zoom))
			
def circle(i,j,r,frame=None,c="green",ra=False):
	"""Draw a circle defined by (i,j) and radius r (pixels)"""
	check_dir()

	if frame!=None:
		nf_ds9.set("frame %d" % (frame))
	if ra==False:
		nf_ds9.set('regions', 'physical; circle(%f, %f, %f) # color = %s' % (i,j,r,c))
	else:
		nf_ds9.set('regions', 'fk5; circle(%f, %f, %f) # color = %s' % (i,j,r,c))

def ellipse(i,j,a,b,theta,c="green"):
	"""Draw an ellipse defined by (i,j) and axes (a,b) (pixels)"""
	check_dir()
	nf_ds9.set('regions', 'physical; ellipse(%f, %f, %f, %f, %f) # color = %s' % (i,j,a,b,theta,c))


def box(i,j,a,b,t,c="green"):
	"""Draw a box defined by (i,j) and size (a,b) (pixels)"""
	check_dir()

	nf_ds9.set('regions', 'image; box(%f, %f, %f, %f, %f) # color = %s' % (i,j,a,b,t,c))

def pan(i,j,frame=None,ra=False):
	"""Pan DS9 to a specific image coordinate"""
	check_dir()
	if frame!=None:
		nf_ds9.set("frame %d" % (frame))
	if not ra:
		nf_ds9.set("pan to %d %d" % (i,j))
	else:
		nf_ds9.set("pan to %f %f wcs fk5" % (i,j))

def zoom(s,frame=None):
	"""Zoom on image by factor s"""
	check_dir()
	if frame!=None:
		nf_ds9.set("frame %d" % (frame))
	nf_ds9.set("zoom to %d" % (s))

def scale(z1,z2):
	"""Set display scale to z1<z2"""
	check_dir()

	nf_ds9.set("scale limits %e %e" % (z1,z2))


def tvm(cat=None,frame=None,label=None,x=None,y=None,fontsize=7,color="green",circle=None, world=None, xoff=0., yoff=0.):
	"""Rough implementation of the old rvm command. This lets you mark regions on an image using circles. Input can be 
	a catalog (default is SEXtractor format with X_IMAGE, Y_IMAGE coordinated). x and y can specify different column names 
	in the catalog. cat can be the name of a text file or an astropy Table. If cat is None, coordinates can be passed as
	x and y and these can be lists"""
	import tempfile, string
	from astropy.table import Table

	check_dir()

	if frame!=None:
		nf_ds9.set("frame %d" % (frame))
	font="helvetica %d normal roman" % (fontsize)
	
	if type(cat)==type("s") or type(cat)==Table or type(cat)==type({}):
		if type(cat)==Table:
			data = cat
		elif type(cat)==type({}):
			data = cat
		elif cat[-4:]==".cat":
			data = Table.read(cat,format="ascii.sextractor")
		else:
			data = Table.read(cat)


		colnames = data.keys()


		if world==None and x==None and y==None:
			xindex = "X_IMAGE"
			yindex = "Y_IMAGE"
			aindex = "A_IMAGE"
			bindex = "B_IMAGE"
			tindex = "THETA_IMAGE"
			coordsys = "image"
		elif world!=None and x==None and y==None:
			xindex = "X_WORLD"
			yindex = "Y_WORLD"
			aindex = "A_WORLD"
			bindex = "B_WORLD"
			tindex = "THETA_WORLD"
			coordsys = "J2000"
		elif world==None and x!=None and y!=None:
			xindex = x
			yindex = y
			circle = 5
			coordsys = "image"
		elif world!=None and x!=None and y!=None:
			xindex = x
			yindex = y
			circle = 5*0.128/3600
			coordsys = "J2000"

		if circle==None and (aindex not in colnames or bindex not in colnames or tindex not in colnames):
			print("Size information not found.. using circle=5")
			if coordsys=="image":
				circle = 5
			else:
				circle = 5*0.128/3600

		x_image = data[xindex] + xoff
		y_image = data[yindex] + yoff

		if circle==None:
			a_image = data[aindex]
			b_image = data[bindex]
			theta_image = data[tindex]
		else:
			a_image = x_image*0.+circle
			b_image = x_image*0.+circle
			theta_image = x_image*0.

	else:
		if world==None:
			if circle==None:
				circle = 5
			coordsys = "image"
		else:
			if circle==None:
				circle = 5*0.128/3600
			coordsys = "J2000"
		if cat!=None:
			x_image = np.asarray(cat[x])
			y_image = np.asarray(cat[y])
			a_image = x_image*0.+circle
			b_image = x_image*0.+circle
			theta_image = x_image*0.
		else:
			if type(x)==type(list([])):
				x = np.array(x)
				y = np.array(y)
			elif type(x)==type(1) or type(x)==type(1.0):
				x = np.array([x])
				y = np.array([y])

			x_image = x
			y_image = y
			a_image = x_image*0.+circle
			b_image = x_image*0.+circle
			theta_image = x_image*0.

	if label!=None:
		label = data[label]

	vg1 = np.isnan(a_image)
	vg2 = np.isnan(b_image)
	b_image[vg2] = 0.
	tmp = tempfile.mkstemp()[1]

	if label!=None:
		lines = ["%s; ellipse(%f,%f,%f,%f,%f) # color = %s text={%s} font=\"%s\"\n" % (coordsys,x_image[i],y_image[i],a_image[i],b_image[i],
			theta_image[i],color,label[i],font) for i in range(len(x_image))]
	else:
		lines = ["%s; ellipse(%f,%f,%f,%f,%f) # color = %s \n" % (coordsys,x_image[i],y_image[i],a_image[i],b_image[i],theta_image[i],color) for i in range(len(x_image))]

	nf_ds9.set("regions color %s" % (color))
	nf_ds9.set("regions load %s" % (tmp))

def imexam(frame=None):
	"""Causes DS9 to wait for a mouse click with a blinking cursor. Upon mouse click, returns (i,j) and the value of the pixel"""
	if frame!=None:
		nf_ds9.set("frame %d" % (frame))

	s = nf_ds9.get("iexam coordinate image")
	ws = s.split()
	x = int(ws[0])
	y = int(ws[1])
	s = nf_ds9.get("data image {} {} 1 1 yes".format(x,y))

	return x,y,float(s)



	
