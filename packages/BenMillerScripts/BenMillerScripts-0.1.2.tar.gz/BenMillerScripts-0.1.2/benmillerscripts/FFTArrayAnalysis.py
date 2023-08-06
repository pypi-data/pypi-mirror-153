import DigitalMicrograph as DM
import numpy as np
import sys
import time
if not DM.IsScriptOnMainThread(): print('Scipy scripts cannot be run on Background Thread.'); exit()
import scipy
import scipy.ndimage as sND
import skimage.morphology as morph
from skimage.io import imsave
from numpy.lib.stride_tricks import as_strided
sys.argv.extend(['-a', ' '])
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import tkinter as tk
import tkinter.filedialog as tkfd
import os

#Use TQDM??
GUI_Progress_Bar = True
if GUI_Progress_Bar: from  tqdm.gui import tqdm

#User-Set Parameters XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#Set FFT Size and Spacing (Default 128,32)
FFTsize = 128
spacing = 32
#Set Percentage of Radial Profile (from center) to be Ignored (Default 10)
maskP = 10
#Set the minimum distance between spots (to generate masked 4D dataset)
min_spot_dist = 5
#Set to number to also mask the center vertical and horizontal lines in the FFT, set to 0 to not mask (Default 2)
maskC_width = 2
#Set memory usage level (GB) above which the code will ask user if they want to continue. (Default 6)
mem_warn_limit = 6
#Set whether to pad the result border so that the result image has the exact same shape as the input data (Default True)
pad_border = True
#Set the padding mode. Available options are given here: https://numpy.org/doc/stable/reference/generated/numpy.pad.html (Default 'constant')
pad_mode = 'constant'
#Set how much to bin the raw image data prior to computing FFTs higher values save time, but may result in loss of information (Default 1)
binning = 1
#Set whether to filter data prior to analysis (for FFTs this is a gaussian filter, and for 4D STEM a more computationally expensive median filter)
pre_filter = True

#Parameters for time series only
#(For a time-series of images) Set a single intensity scale maximum so that all colormaps in the series are scaled the same (Default None)
RGB_scale_max = None
#(For a time-series of images) Set which frame in the dataset is displayed as a datacube  (Default -1)
#Set this to -1 to not display a datacube
showdatacube_frame = -1
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

high_lims=[]
#Define dummy function named TQDM in case user has chosen not to use this package
if not GUI_Progress_Bar: 
	def tqdm(list):
		return list

#FunctionsXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

def strided_binning2D(array,binning=(1,1)):
	"""
	Function to Bin 2D Data 
	Accepts:
		array		2D numpy array to be binned
		binning		2 element tuple of integer binning amounts (bin_x, bin_y)
	Returns: A binned 2D array
	"""
	bin=np.flip(binning)
	nh = (array.shape[0]-bin[0])//bin[0]+1
	nw = (array.shape[1]-bin[1])//bin[1]+1
	strides = (array.strides[0],array.strides[1],array.strides[0]*bin[0],array.strides[1]*bin[1])
	strides = (array.strides[0],array.strides[1],array.strides[0]*bin[0],array.strides[1]*bin[1])
	shape = (bin[0],bin[1],nh,nw)
	virtual_datacube = as_strided(array,shape=shape,strides=strides)
	result = np.sum(virtual_datacube,axis=(0,1))
	return result

def DrawColorScale(matplotlibscale=False, map_var = 'theta'):
	"""
	Function to Create Radial Color Scale
	Accepts:
		matplotlibscale		boolean- determines whether to plot something with matplotlib.
		if matplotlibscale is false (default) then an image is produced in GMS instead
		map_var				string ('theta' or 'radius') This is the same as the input into Process_Dataset or STEMx_Process_Cube functions
		
	Returns: function returns nothing, but this outputs a color scale to either a GMS image or a matplotlib plot
	"""
	if map_var is 'theta':
		scalesize = 256
		(x,y) = np.meshgrid(range(-scalesize,scalesize),range(-scalesize,scalesize))
		t = np.arctan2(-y, x)/np.pi*180
		t[t<0]+=180
		r = np.hypot(x, y)/scalesize
		r[r>1] = 0
		ShowRGB(hue_brightness_RGB(t, r,(0,180),"gist_rainbow", original_im_data=None),"Map Scale")
		if matplotlibscale:
			# Using linspace so that the endpoint of 360 is included
			actual = np.radians(np.linspace(0, 180, 90))
			expected = np.arange(0,256)
			r, theta = np.meshgrid(expected, actual)
			values = theta
			fig, ax = plt.subplots(2,subplot_kw=dict(projection='polar'))
			ax[0].contourf(-theta, r, -r,256,cmap='Greys')
			ax[1].contourf(-theta, r, theta,256,cmap='gist_rainbow')
			ax[0].set_axis_off()
			ax[1].set_axis_off()
			plt.show()
	else:
		print("Color Scale for map_var='radius' is not implemented yet")
		scalesize = 256
		(x,y) = np.meshgrid(range(0,scalesize),range(0,scalesize))
		clims=(np.percentile(cal_image,5),np.percentile(cal_image,95))
		scale_im = CreateDM_RGB(hue_brightness_RGB(x, y,(0,scalesize),"jet", original_im_data=None))
		scale_im.SetDimensionCalibration(0,clims[0],(clims[1]-clims[0])/scalesize,'nm',0)
		scale_im.ShowImage()
		del scale_im
def ShowRGB(X,name):
	"""
	#Function to Show RGB Image in GMS (Hybrid DM-Python)
	Accepts:
		X		3D numpy array representing a 2D image with red green and blue channels [x,y,color]
		name	string specifying the name of the original data
	Returns: function returns nothing, but this outputs an RGB image to GMS
	"""
	# Create DM images for each color
	r_ = DM.CreateImage(X[:,:,0].copy())
	g_ = DM.CreateImage(X[:,:,1].copy())
	b_ = DM.CreateImage(X[:,:,2].copy())
	# Build one-liner DM-script to show RGB image 
	dms = 'rgb(' + r_.GetLabel() + ',' + g_.GetLabel() + ',' + b_.GetLabel() + ').ShowImage()'
	DM.ExecuteScriptString(dms)
	Final_Im = DM.GetFrontImage()
	Final_Im.SetName("FFT Final Result: "+name)
	del Final_Im
	# Always delete Py_Image references in the script
	del r_
	del g_
	del b_

def UpdateRGB(DM_RGB_ID,X):
	"""
	#Function to Update RGB Image in GMS (Hybrid DM-Python)
	Accepts:
		DM_RGB_ID	DM image ID number of existing RGB image in GMS
		X			3D numpy array representing a 2D image with red green and blue channels [x,y,color]
	Returns: function returns nothing, but this outputs an RGB image to an existing GMS image window
	"""
	# Create DM images for each color
	r_ = DM.CreateImage(X[:,:,0].copy())
	g_ = DM.CreateImage(X[:,:,1].copy())
	b_ = DM.CreateImage(X[:,:,2].copy())
	#DM-script to update RGB image
	dms = 'RGBimage img := FindImageByID('+ str(DM_RGB_ID) +')\n' 
	dms+= 'img = rgb(' + r_.GetLabel() + ',' + g_.GetLabel() + ',' + b_.GetLabel() + ')\n'
	dms+= 'img.UpdateImage()'
	DM.ExecuteScriptString(dms)
	# Always delete Py_Image references in the script
	del r_
	del g_
	del b_

def CreateDM_RGB(X):
	"""
	#Function to Create RGB Image in GMS (Hybrid DM-Python)
	Accepts:
		X			3D numpy array representing a 2D image with red green and blue channels [x,y,color]
		name		string specifying the name of the original data
	Returns: 
		Final_Im 	a DM RGB image
	"""
	# Create DM images for each color
	r_ = DM.CreateImage(X[:,:,0].copy())
	g_ = DM.CreateImage(X[:,:,1].copy())
	b_ = DM.CreateImage(X[:,:,2].copy())
	# Build one-liner DM-script to show RGB image 
	dms = 'rgb(' + r_.GetLabel() + ',' + g_.GetLabel() + ',' + b_.GetLabel() + ').ShowImage()'
	DM.ExecuteScriptString(dms)
	Final_Im = DM.GetFrontImage()
	DM.DeleteImage(Final_Im)
	# Always delete Py_Image references in the script
	del r_
	del g_
	del b_
	return Final_Im

def UpScaleRGB(X,scale=1):
	"""
	#Function to increase the size of an RGB image using the Scipy ndimage zoom command
	Accepts:
		X		3D numpy array representing a 2D image with red green and blue channels [x,y,color]
		scale	number >=1 specifying the scaling factor to use. 
					scale can also be a string: 'match' if scale is set to 'match' then the scale factor is automatically determined 
					such that the RGB image is the same size as the original input image
	Returns:	a 3D numpy array representing a 2D image with red green and blue channels [x,y,color]
	"""
	if scale=='match':
		scale = spacing
	Xup = sND.zoom(X,[scale,scale,1])
	return Xup

def Upscale_4D_STEM(array,scale):
	"""
	Function to upscale a 4D STEM data cube 
	Accepts: 
		array	4D numpy array (x,y,u,v) representing an array of diffraction patterns
		scale	number >=1 specifying the scaling factor to upscale the real-space dimensions by
	Returns:	an upscaled 4D array
	"""
	shape = array.shape
	if(len(shape) != 4): 
		DM.OkDialog('Data is not 4D... script aborted')
		sys.exit()
	if ((shape[2]%scale == 0) and (shape[3]%scale == 0)):
		new_array = scipy.ndimage.zoom(array,(scale,scale,1/scale,1/scale),order=1)
	else: 
		print("Error: Diffraction Pattern size (%s x %s) not divisible by scale (%s)" %(shape[2],shape[3],scale))
		exit()
	return new_array
	
def Get_DM_RGB_Image_Data(image):
	RGB_ID = str(image.GetID())
	dm_script_string = ('RGBimage img1 := FindImageByID ('+RGB_ID+')\n'
		'image imR := red(img1)\n'
		'image imG := green(img1)\n'
		'image imB := blue(img1)\n'
		'imR.ShowImage()\n'
		'imG.ShowImage()\n'
		'imB.ShowImage()\n'
		'number idR = ImageGetID(imR)\n'
		'number idG = ImageGetID(imG)\n'
		'number idB = ImageGetID(imB)\n'
		'GetPersistentTagGroup().TagGroupSetTagAsLong("Python_Temp:idR",idR)\n'
		'GetPersistentTagGroup().TagGroupSetTagAsLong("Python_Temp:idG",idG)\n'
		'GetPersistentTagGroup().TagGroupSetTagAsLong("Python_Temp:idB",idB)')
	DM.ExecuteScriptString(dm_script_string)
	(b,idR) = DM.GetPersistentTagGroup().GetTagAsUInt32("Python_Temp:idR")
	(b,idG) = DM.GetPersistentTagGroup().GetTagAsUInt32("Python_Temp:idG")
	(b,idB) = DM.GetPersistentTagGroup().GetTagAsUInt32("Python_Temp:idB")
	red = DM.FindImageByID(idR)  
	green = DM.FindImageByID(idG)  
	blue = DM.FindImageByID(idB)  
	RGB_array = np.dstack((red.GetNumArray(),green.GetNumArray(),blue.GetNumArray()))
	DM.DeleteImage(red)
	DM.DeleteImage(green)
	DM.DeleteImage(blue)
	del red
	del green
	del blue
	return RGB_array

def hue_brightness_RGB(hue,brightness,clims,colormap,original_im_data=None,scale_max=None):
	"""
	Function to convert 2 greyscale images to 1 RGB image 
	Accepts:
		hue					2D numpy array representing a 2D image This will be used to determine the hue of the RGB image
		brightness			2D numpy array representing a 2D image This will be used to determine the brightness of the RGB image
		clims				2 element tuple containing the minimum and maximum values for the hue colorscale
		colormap			string specifying the matplotlib colormap to use for the hue colorscale
		original_im_data	optional 2D numpy array providing an image to be blended/overlaid together with the RGB image
		scale_max			optional fixed maximum for the brightness scale 
								this can be used to make brightness comparable over every frame in a dataset.
								otherwise each frame's brightness will be autoscaled independently
	Returns: X				3D numpy array representing a 2D image with red green and blue channels [x,y,color]
	"""
	if scale_max is None: bright_lims=np.percentile(brightness, (0,100))
	else: bright_lims=(np.percentile(brightness, 0),scale_max)
	global high_lims
	high_lims.append(np.max(brightness))
	scaled = (brightness-bright_lims[0])/(bright_lims[1]-bright_lims[0])
	scaled = np.transpose(scaled*np.ones((4,1,1)),(1,2,0))*255
	scaled[scaled>255] = 255
	cNorm  = colors.Normalize(vmin=clims[0], vmax=clims[1])
	scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=colormap)
	X = (scalarMap.to_rgba(hue)*scaled).astype('uint8')
	if original_im_data is not None:
		LS = colors.LightSource()
		im_lims=np.percentile(original_im_data, (1,99))
		scaled_im = 2*((original_im_data-im_lims[0])/(im_lims[1]-im_lims[0])*((brightness-bright_lims[0])/(bright_lims[1]-bright_lims[0]))**0.5-0.5)
		X = LS.blend_hsv(X[:,:,:3]/256,np.transpose(scaled_im*np.ones((3,1,1)),(1,2,0)))*255
	return X
	
def create_4D_circular_dilation_element(r):
		r=int(r)
		size=2*r+1
		Y, X = np.ogrid[:size, :size]
		dist_from_center = np.sqrt((X - (r))**2 + (Y-(r))**2)
		image_mask = np.zeros((3,3,size,size))
		center = int(size//2)
		image_mask[1,1,center-r:center+r+1,center-r:center+r+1]=dist_from_center <= r
		return image_mask
		
def mask_FFT_center(array,mask_percent,mask_cross_width):
	"""
	Function to mask diffractogram or diffraction-pattern central spot and cross lines
	Accepts:
		array				2D (or 4D) numpy array representing a single diffractogram/diffraction-pattern (or a 4D cube of them)
		mask_percent		number between 0 and 100 specifying the central circlular mask diameter as a percentage of the diffractogram/diffraction-pattern size 
		mask_cross_width	integer number specifying the number of pixels to mask (both vertically and horizontally) on either side of the pattern center 
	Returns:				a masked 2D (or 4D) numpy array representing a single diffractogram/diffraction-pattern (or a 4D cube of them)
	"""
	def create_circular_center_mask(r,FFT_size):
		r=int(r)
		size=2*r+1
		Y, X = np.ogrid[:size, :size]
		dist_from_center = np.sqrt((X - (r))**2 + (Y-(r))**2)
		image_mask = np.zeros((FFT_size,FFT_size))
		center = int(FFT_size//2)
		image_mask[center-r:center+r+1,center-r:center+r+1]=dist_from_center <= r
		return image_mask.astype('bool')
	
	m = mask_cross_width
	FFT_size = array.shape[-1]
	if len(array.shape)==4:
		maskval = np.median(np.min(array, axis=(0,1)))
		if mask_cross_width>0:
			array[:,:,FFT_size//2-m+1:FFT_size//2+m,:] = maskval
			array[:,:,:,FFT_size//2-m+1:FFT_size//2+m] = maskval
		if mask_percent>0:
			mask = create_circular_center_mask(mask_percent/100*FFT_size/2,FFT_size)
			array[:,:,mask] = maskval
		return array
	if len(array.shape)==2:
		maskval = np.percentile(array,1)
		if mask_cross_width>0:
			array[FFT_size//2-m+1:FFT_size//2+m,:] = maskval
			array[:,FFT_size//2-m+1:FFT_size//2+m] = maskval
		if mask_percent>0:
			mask = create_circular_center_mask(mask_percent/100*FFT_size/2,FFT_size)
			array[mask] = maskval
		return array

def FFT_Result_Shape(imo,FFTsize=FFTsize, spacing=spacing, scale=1):
	"""
	Function to calculate the shape of the resulting map for a DM image or numpy array
	Accepts:
		imo			original image to be processed (can be a DM python image object or a numpy array)
		FFTsize		size of the FFTs to be computed (normally set to be the user parameter: FFTsize)
		spacing		spacing of the FFTs to be computed (normally set to be the user parameter: spacing)
		scale		number >=1 specifying the scaling factor to use
						should be same scale factor as used for the UpScaleRGB function
	Returns:		a 2 element tuple specifying the (x,y) size of the RGB image that will be produced by this module
	"""
	if isinstance(imo, np.ndarray): data = imo
	else: data = imo.GetNumArray()
	if(len(data.shape) != 2): 
		DM.OkDialog('Image is not 2D')
		sys.exit()
	if ((scale == 'match') and (pad_border == True)):
		(w0,h0) = data.shape
		print('MatchedScale')
		(nw,nh) = (w0,h0)
	else: 
		data = strided_binning2D(data, binning=(binning,binning))
		(w0,h0) = data.shape
		if scale=='match':
			scale = spacing*binning
		#Create 4D Diffractogram Datacube (Like 4D STEM datacube)
		nw = (w0-FFTsize)//spacing+1
		nh = (h0-FFTsize)//spacing+1
		if pad_border: 
			nw = nw+FFTsize//spacing
			nh = nh+FFTsize//spacing
		nw=nw*scale
		nh=nh*scale	
	del imo
	return(nw,nh)

def STEMx_Crop_to_Center_Square(datacube, center):
	"""
	Function to crop a 4D cube of diffraction patterns so that the center of the patterns 
	is in the center of the image/array and the image/array/pattern is square
	This does not find the pattern center. It also does not account for different patterns having different center positions
	this assumes the patterns have already been aligned, so that every pattern in the dataset has the same center. 
	This alignment can be performed using the built-in tool found in GMS under the SI menu (Align by Peak)
	Accepts:
		datacube	4D numpy array (x,y,u,v) representing an array of diffraction patterns
		center		2 element tuple specifying the center (in pixels, not calibrated units) of the diffraction patterns
	Returns:		a cropped 4D numpy array (x,y,u,v) representing an array of diffraction patterns
	"""
	if(len(datacube.shape) != 4): 
		DM.OkDialog('Data is not 4D... script aborted')
		sys.exit()
	min_dist = min(abs(datacube.shape[2]-center[1]),center[1],abs(datacube.shape[3]-center[0]),center[0])
	datacube_cropped = datacube[:,:,center[1]-min_dist:center[1]+min_dist,center[0]-min_dist:center[0]+min_dist]
	return datacube_cropped

def STEMx_Array_Analysis(datacube,maskP=10,maskC_width=0,ShowCube=False,median=True,Mask_Gen=False):
	"""
	Function (similar to FFT_Array_Analysis) to process 4D STEM datacube (assumes datacube patterns are centered on direct beam and are square)
		First use STEMx_Crop_to_Center_Square to center the patterns before analyzing with this function
	Accepts:
		datacube		4D numpy array (x,y,u,v) representing an array of diffraction patterns (should be square and centered)
		maskP			number between 0 and 100 specifying the central circlular mask diameter as a percentage of the diffractogram/diffraction-pattern size 
		maskC_width		integer number specifying the number of pixels to mask (both vertically and horizontally) on either side of the pattern center 
		ShowCube		boolean specifying whether to display the masked,filtered datacube in GMS 
		median			boolean specifying whether to process the data with a (3x3 pixel) median filter (to eliminate x-rays, and some camera artifacts) prior to processing
							this is recommended, but does make the processing significantly slower
	Returns:		
		r_max			2D numpy array where each pixel is the distance from the diffraction pattern center of the maximum pixel from each diffraction pattern
		t_max			2D numpy array where each pixel is the angle from the horizontal of the maximum pixel from each diffraction pattern
		i_max			2D numpy array where each pixel is the intensity of the maximum pixel from each diffraction pattern
		diff_max		2D numpy array giving a single diffraction pattern, where every pixel is the maximum value of that pixel across all diffraction patterns in the datacube
	"""
	if(len(datacube.shape) != 4): 
		DM.OkDialog('Data is not 4D... script aborted')
		sys.exit()
	if median: datacube = scipy.ndimage.median_filter(datacube, size=(1,1,3,3))
	datacube = mask_FFT_center(datacube,maskP,maskC_width)
	diff_size = datacube.shape[-1]
	x_max = (np.argmax(np.max(datacube, axis=2),axis=2)-diff_size//2).astype('int')
	y_max = -(np.argmax(np.max(datacube, axis=3),axis=2)-diff_size//2).astype('int')
	r_max = np.hypot(x_max, y_max)/diff_size
	t_max = np.arctan2(y_max, x_max)/np.pi*180
	t_max[t_max<0] += 180
	i_max = np.max(datacube, axis=(2,3))
	#Also calculate a maximum diffractogram
	diff_max = np.max(datacube, axis=(0,1))
	if ShowCube:
		cube_im = DM.CreateImage(np.copy(datacube))
		cube_im.SetName("4D Dataset Used for Analysis")
		cube_im.GetTagGroup().SetTagAsBoolean('Meta Data:Data Order Swapped', True)
		cube_im.GetTagGroup().SetTagAsString('Meta Data:Format', 'Diffraction image')
		cube_im.GetTagGroup().SetTagAsString('Meta Data:Acquisition Mode', 'FFTs of TEM Image')
		cube_im.ShowImage()
		del cube_im
	if Mask_Gen: 
		print("Masking Datacube...")
		I,J = np.meshgrid(np.arange(datacube.shape[1]),np.arange(datacube.shape[0]))
		mask = np.zeros(datacube.shape,dtype=np.int8)
		mask[J,I,-y_max+diff_size//2,x_max+diff_size//2] = 1
		cubemask = morph.dilation(mask, selem=create_4D_circular_dilation_element(min_spot_dist)).astype('bool')
		masked_cube = datacube 
		masked_cube[cubemask] = 0
		masked_im = DM.CreateImage(np.copy(masked_cube))
		masked_im.SetName("Max Spot Masked 4D Dataset")
		masked_im.GetTagGroup().SetTagAsBoolean('Meta Data:Data Order Swapped', True)
		masked_im.GetTagGroup().SetTagAsString('Meta Data:Format', 'Diffraction image')
		masked_im.GetTagGroup().SetTagAsString('Meta Data:Acquisition Mode', 'FFTs of TEM Image')
		masked_im.ShowImage()
		del masked_im
	return (r_max,t_max,i_max,diff_max,x_max,y_max)
	
def STEMx_Process_Cube(image4D,map_var, show_cube = False, im_data = None,RGB_scale_max=None,Mask_Gen=False):
	"""
	Function to process a STEMx dataset (assumes datacube patterns are centered on direct beam and are square)
		If this is not true, First use STEMx_Crop_to_Center_Square to center the patterns before analyzing with this function, 
		Pass both the original DM image and the numpy array produced by STEMx_Crop_to_Center_Square as the im_data parameter
	Accepts:
		image4D 		4D DM image with an array of diffraction patterns
		map_var			string specifying what parameter will be output as the resulting colormap's hue
		show_cube		Boolean specifying whether to output a datacube to GMS (see function STEMx_Array_Analysis)
		im_data			4D numpy array (x,y,u,v) representing an array of pre-processed diffraction patterns (this could be the output of STEMx_Crop_to_Center_Square)
		RGB_scale_max	optional number specifying a fixed maximum quantitative value for the colomap's brightness 
							(this is important when processing a series of maps, where all maps should have the same upper limit)
							if no value is given the map will be scaled automatically by the maximum from the data
	Returns:			
		RGB_im				3D numpy array representing a 2D image with red green and blue channels [x,y,color] 
								(suitable for use with the functions ShowRGB,UpdateRGB,UpScaleRGB,CreateDM_RGB)
		spacing_image		2D numpy array where each pixel is the distance from the diffraction pattern center of the maximum pixel from each diffraction pattern
		direction_image		2D numpy array where each pixel is the angle from the horizontal of the maximum pixel from each diffraction pattern
		intensity_image		2D numpy array where each pixel is the intensity of the maximum pixel from each diffraction pattern
		diffractogram_max	2D numpy array giving a single diffraction pattern, where every pixel is the maximum value of that pixel across all diffraction patterns in the datacube
	"""
	stime=time.perf_counter()
	if im_data is None: data = image4D.GetNumArray()
	else: data = im_data
	print("Processing %s diffraction patterns with %s total pixels" %(data.shape[0]*data.shape[1],np.product(data.shape)))
	(spacing_image,direction_image,intensity_image,diffractogram_max,x_max,y_max)=STEMx_Array_Analysis(data,maskP=maskP,maskC_width=maskC_width, ShowCube = show_cube, median=pre_filter,Mask_Gen=Mask_Gen)
	if map_var == "theta":
		clims=(0,180)
		RGB_im = hue_brightness_RGB(direction_image, intensity_image,clims,"gist_rainbow", original_im_data=None,scale_max=RGB_scale_max)
	elif map_var == "radius":
		clims=(np.percentile(spacing_image,5),np.percentile(spacing_image,95))
		RGB_im = hue_brightness_RGB(spacing_image, intensity_image,clims,"jet", original_im_data=None,scale_max=RGB_scale_max)
	del image4D
	print("Datacube Processing Time= %s seconds" %(time.perf_counter()-stime))
	return (RGB_im,direction_image,intensity_image,spacing_image,diffractogram_max)

def FFT_Array_Analysis(imo,FFTsize,spacing,maskP=10,maskC_width=0,show_cube=False, data=None, smooth=True):
	"""
	Function (similar to STEMx_Array_Analysis) to process a 2D image by first splitting into many patches and computing FFTs,
		transforming it into a 4D data cube resembling a 4D STEM dataset
	Accepts:
		imo				2D DM image variable (not a numpy array)
		FFTsize			integer (preferably 2^n) specifying the pixel size of the FFTs to be computed  FFT.shape = (FFTsize,FFTsize)
		spacing			integer specifying the spacing between windows of data from which FFTs are computed. If FFTsize = spacing, then no overlap occurs. 
		maskP			number between 0 and 100 specifying the central circlular mask diameter as a percentage of the diffractogram/diffraction-pattern size 
		maskC_width		integer number specifying the number of pixels to mask (both vertically and horizontally) on either side of the pattern center 
		ShowCube		boolean specifying whether to display a masked,filtered FFT datacube in GMS 
		data			optional 2D numpy array that overrides the data in the required DM image variable (used to pass in data that has been processed rather than raw data)
		smooth			boolean specifying whether to process the data with a gaussian filter (to reduce spurious noise) prior to processing. this is recommended
	Returns:		
		r_max			2D numpy array where each pixel is the distance-from-center of the maximum pixel in each diffractogram
		t_max			2D numpy array where each pixel is the angle from the horizontal of the maximum pixel from each diffractogram
		i_max			2D numpy array where each pixel is the intensity of the maximum pixel from each diffractogram
		diff_max		2D numpy array giving a single diffractogram, where every pixel is the maximum value of that pixel across all diffractograms in the datacube
	"""
	#stime=time.perf_counter()
	time_it = 0
	if data is None: data = imo.GetNumArray()
	
	if(len(data.shape) != 2): 
		DM.OkDialog('Image is not 2D... aborting script')
		sys.exit()
	data = strided_binning2D(data, binning=(binning,binning))
	#Create 4D Diffractogram Datacube (Like 4D STEM datacube)
	(w0,h0) = data.shape
	nw = (w0-FFTsize)//spacing+1
	nh = (h0-FFTsize)//spacing+1

	#Create (Virtual) 4D Datacube of Image Regions 
	shape = (FFTsize,FFTsize,nw,nh)
	strides = (data.strides[0],data.strides[1],data.strides[0]*spacing,data.strides[1]*spacing)
	image_datacube = np.transpose(as_strided(data,shape=shape,strides=strides),(2,3,0,1))
	#Create Hanning Window
	hanningf = np.hanning(FFTsize)
	hanningWindow2d = np.sqrt(np.outer(hanningf, hanningf)).astype('float32')
	#Compute FFTs
	print("Computing %s FFTs..." %(nw*nh))
	start_timef=time.perf_counter()
	datacube = np.log(np.fft.fftshift(np.abs(np.fft.fft2(hanningWindow2d*image_datacube))**2, axes=(2,3))).astype('float32')
	print("FFT Computation Time: %s s" %(time.perf_counter()-start_timef))
	#if smooth: datacube = scipy.ndimage.median_filter(datacube, size=(1,1,3,3))
	if smooth: datacube = scipy.ndimage.gaussian_filter(datacube,sigma=(0,0,1,1),truncate=2)
	datacube = mask_FFT_center(datacube,maskP,maskC_width)
	
	if show_cube: 
		origin, x_scale, scale_unit =  imo.GetDimensionCalibration(1, 0)
		name = imo.GetName()
		def front_image_create_diff_picker_dm(t,l,b,r):
			fipdm = ('image Picker_Im = PickerCreate( GetFrontImage(), '+str(t)+','+str(l)+','+str(b)+','+str(r)+')')
			DM.ExecuteScriptString(fipdm)
		dc_im = DM.CreateImage(np.copy(datacube.astype('float32')))
		dc_im.SetDimensionCalibration(0,-1/(2*(x_scale*binning)),1/(x_scale*binning)/FFTsize,scale_unit+"-1",0)
		dc_im.SetDimensionCalibration(1,-1/(2*(x_scale*binning)),1/(x_scale*binning)/FFTsize,scale_unit+"-1",0)
		dc_im.SetDimensionCalibration(2,0,(x_scale*binning)*spacing,scale_unit,0)
		dc_im.SetDimensionCalibration(3,0,(x_scale*binning)*spacing,scale_unit,0)
		dc_im.SetName("4D_STEM Diffractogram of "+name)
		dc_im.GetTagGroup().SetTagAsBoolean('Meta Data:Data Order Swapped', True)
		dc_im.GetTagGroup().SetTagAsString('Meta Data:Format', 'Diffraction image')
		dc_im.GetTagGroup().SetTagAsString('Meta Data:Acquisition Mode', 'FFTs of TEM Image')
		dc_im.ShowImage()
		DM.ExecuteScriptString("GetFrontImage().setzoom("+str(3)+")\nImageDocumentOptimizeWindow(GetFrontImageDocument())")
		t=datacube.shape[0]//2-max(datacube.shape[0]//10,1)
		b=datacube.shape[0]//2+max(datacube.shape[0]//10,1)
		l=datacube.shape[1]//2-max(datacube.shape[1]//10,1)
		r=datacube.shape[1]//2+max(datacube.shape[1]//10,1)
		try: front_image_create_diff_picker_dm(t,l,b,r)
		except: print("Ignoring DM Error") 
		disp = dc_im.GetImageDisplay(0)
		del dc_im
	del imo
	#Find the maximum pixel of each FFT
	x_max = (np.argmax(np.max(datacube[:,:,0:FFTsize//2,:], axis=2),axis=2)-FFTsize//2).astype('int')
	y_max = -(np.argmax(np.max(datacube[:,:,0:FFTsize//2,:], axis=3),axis=2)-FFTsize//2).astype('int')
	r_max = np.hypot(x_max, y_max)/FFTsize
	#r_max = np.hypot(x_max, y_max)/(x_scale*binning)/FFTsize
	t_max = np.arctan2(y_max, x_max)/np.pi*180
	t_max[t_max<0] += 180
	i_max = np.max(datacube, axis=(2,3))
	#Also calculate a maximum diffractogram
	diff_max = np.max(datacube, axis=(0,1))
	if pad_border:
		padx = FFTsize//spacing//2
		pady = FFTsize//spacing//2
		r_max = np.pad(r_max,((padx, padx), (pady, pady)),mode=pad_mode, constant_values = np.min(r_max))
		t_max = np.pad(t_max,((padx, padx), (pady, pady)),mode=pad_mode, constant_values = np.min(t_max))
		i_max = np.pad(i_max,((padx, padx), (pady, pady)),mode=pad_mode, constant_values = np.min(i_max))
	
	return(r_max,t_max,i_max,diff_max)

def BrowseforFileList():
	"""
	Function to prompt the user to browse for a folder, from which all DM4 files are found and listed. 
		This recursively finds all DM4 files in all sub-directories of the selected folder
	Accepts:
		nothing
	Returns:		
		listOfFiles		list of full file paths for all DM4 files
		dirname			the base directory chosen by the user
		newdir			a new directory name (likely not existing on the disk) that adds the prefix "DMScript Edited Datasets/" after the drive letter of the original name
	"""
	# Let User Select the IS Dataset Directory
	sys.argv.extend(['-a', ' '])
	root = tk.Tk()
	root.withdraw() #use to hide tkinter window
	currdir = os.getcwd()
	dirname = tkfd.askdirectory(parent=root, initialdir=currdir, title='Please select the IS Dataset Root Directory')
	if len(dirname) > 0:
		print("\nOriginal IS DataSet Directory: %s" % dirname)
		newdir=dirname[:3] + 'DMScript Edited Datasets/' + dirname[3:]
		os.chdir(dirname)
	else:
		root.destroy()
		print("User Canceled File Dialog")
		exit()
	# Get the list of all files in directory tree at given path
	listOfFiles = list()
	for (dirpath, dirnames, filenames) in os.walk(dirname):
		listOfFiles += [os.path.join(dirpath, file) for file in filenames if file.endswith('.dm4')]
	listOfFiles.sort()
	root.destroy()
	return (listOfFiles,dirname,newdir)

def processframe(image,map_var,show_cube, scale=1,overlay = True, im_data = None,RGB_scale_max=None): 
	"""
	Function to Process the Image Data in Each Image
	Accepts:
		image			2D DM image to be processed
		map_var			string specifying what parameter will be output as the resulting colormap's hue
		show_cube		Boolean specifying whether to output a datacube to GMS (see function FFT_Array_Analysis)
		scale			number (or string 'match') specifying an upscaling factor to be applied to the final map
						if scale = 'match' then the map will be upscaled to match the dimensions of the original data
		overlay			Boolean specifying whether to overlay the map with the original data... only applied if scale = 'match'
		im_data			optional 2D numpy array with a pre-processed image 
		RGB_scale_max	optional number specifying a fixed maximum quantitative value for the colomap's brightness 
							(this is important when processing a series of maps, where all maps should have the same upper limit)
							if no value is given the map will be scaled automatically by the maximum from the data
	Returns:			
		RGB_im				3D numpy array map result with red green and blue channels [x,y,color] 
								(suitable for use with the functions ShowRGB,UpdateRGB,UpScaleRGB,CreateDM_RGB)
		spacing_image		2D numpy array where each pixel is the distance from the diffraction pattern center of the maximum pixel from each diffraction pattern
		direction_image		2D numpy array where each pixel is the angle from the horizontal of the maximum pixel from each diffraction pattern
		intensity_image		2D numpy array where each pixel is the intensity of the maximum pixel from each diffraction pattern
		diffractogram_max	2D numpy array giving a single diffraction pattern, where every pixel is the maximum value of that pixel across all diffraction patterns in the datacube
	"""
	stime=time.perf_counter()
	if im_data is None: data = image.GetNumArray()
	else: data = im_data
	(spacing_image,direction_image,intensity_image,diffractogram_max) = FFT_Array_Analysis(image,FFTsize,spacing,maskP=maskP,maskC_width=maskC_width,show_cube=show_cube,data = im_data,smooth=pre_filter)
	original_im_data=None
	if scale == 'match':
		if pad_border == True:
			scale = spacing*binning
			spacing_image = sND.zoom(spacing_image,[scale,scale])
			direction_image = sND.zoom(direction_image,[scale,scale])
			intensity_image = sND.zoom(intensity_image,[scale,scale])
			original_size = data.shape
			processed_size = spacing_image.shape
			padx = original_size[0]-processed_size[0]
			pady = original_size[1]-processed_size[1]
			if padx>0:
				spacing_image = np.pad(spacing_image((padx//2, padx-padx//2), (0, 0)),mode=pad_mode, constant_values = np.min(spacing_image))
				direction_image = np.pad(direction_image((padx//2, padx-padx//2), (0, 0)),mode=pad_mode, constant_values = np.min(direction_image))
				intensity_image = np.pad(intensity_image((padx//2, padx-padx//2), (0, 0)),mode=pad_mode, constant_values = np.min(intensity_image))
			if pady>0:
				spacing_image = np.pad(spacing_image((0,0), (pady//2, pady-pady//2)),mode=pad_mode, constant_values = np.min(spacing_image))
				direction_image = np.pad(direction_image((0,0), (pady//2, pady-pady//2)),mode=pad_mode, constant_values = np.min(direction_image))
				intensity_image = np.pad(intensity_image((0,0), (pady//2, pady-pady//2)),mode=pad_mode, constant_values = np.min(intensity_image))
			if padx<0:
				spacing_image = spacing_image[-padx//2:padx-padx//2,:]
				direction_image = direction_image[-padx//2:padx-padx//2,:]
				intensity_image = intensity_image[-padx//2:padx-padx//2,:]
			if pady<0:
				spacing_image = spacing_image[:,-pady//2:pady-pady//2]
				direction_image = direction_image[:,-pady//2:pady-pady//2]
				intensity_image = intensity_image[:,-pady//2:pady-pady//2]
			if overlay:
				original_im_data = data
				#intensity_image = intensity_image**2*image.GetNumArray()
		else: 
			scale = spacing*binning
			spacing_image = sND.zoom(spacing_image,[scale,scale])
			direction_image = sND.zoom(direction_image,[scale,scale])
			intensity_image = sND.zoom(intensity_image,[scale,scale])
	else:
		spacing_image = sND.zoom(spacing_image,[scale,scale])
		direction_image = sND.zoom(direction_image,[scale,scale])
		intensity_image = sND.zoom(intensity_image,[scale,scale])
	if map_var == "theta":
		clims=(0,180)
		RGB_im = hue_brightness_RGB(direction_image, intensity_image,clims,"gist_rainbow",original_im_data=original_im_data,scale_max=RGB_scale_max)
	elif map_var == "radius":
		clims=(np.percentile(spacing_image,5),np.percentile(spacing_image,95))
		print(clims)
		RGB_im = hue_brightness_RGB(spacing_image, intensity_image,clims,"jet",original_im_data=original_im_data,scale_max=RGB_scale_max)
	del image
	print("Frame Processing Time= %s seconds" %(time.perf_counter()-stime))
	return (RGB_im,direction_image,intensity_image,spacing_image,diffractogram_max)

def Process_Dataset(listOfFiles,newdir,map_var, IS_Dataset=True, Stack=False):
	"""
	Function to process every file in a list of files, ideally a Gatan in-situ camera dataset 
	Accepts:
		listOfFiles		list of file paths for each frame in the dataset (can be generated using BrowseforFileList function)
		newdir			base directory in which to save the resulting maps (can be generated using BrowseforFileList function)
		map_var			string specifying what parameter will be output as the resulting colormaps' hue
		IS_Dataset		Boolean specifying whether the input data is an in-situ camera dataset
		Stack			Boolean specifying whether the input data is a DM stack 
			(only one of either IS_Dataset or Stack should be True)... stack support may be removed soon
		
	Returns:			
		isbasename		the directory name to which data is saved
	"""
	#Main loop over all image files
	i=0
	digits = int(np.ceil(np.log10(len(listOfFiles))))
	fmt="{:"+str(digits)+"n}"
	if not os.path.exists(newdir): os.makedirs(newdir)
	for file in tqdm(listOfFiles):
		i=i+1
		newdirnameIS=''
		image = DM.OpenImage(file)
		if(i==1): 
			origin, x_scale, scale_unit =  image.GetDimensionCalibration(1, 0)
			im_shape = image.GetNumArray().shape
			if len(im_shape) == 3:
				num_dims = 3
				(w0,h0,n0) = im_shape
			elif len(im_shape) == 2:
				num_dims = 2
				(w0,h0) = im_shape
			else:
				print("1st file image has wrong number of dimensions")
				exit()
			nw = (w0-FFTsize)//spacing+1
			nh = (h0-FFTsize)//spacing+1
			mem_est = 39.98*(nh*nw*FFTsize**2)/(1024**3)
			print("Estimated %.1f GB of memory required" %mem_est)
			if mem_est>mem_warn_limit: 
				if not DM.OkCancelDialog("Estimated %.1f GB of memory required. Continue?" %mem_est): 
					print("User Canceled")
					exit()
		if(i == showdatacube_frame): show_cube = True
		else: show_cube = False
		if num_dims == 2:
			(processedframe,direction_image,intensity_image,spacing_image,diffractogram_max) = processframe(image,map_var,show_cube,RGB_scale_max=RGB_scale_max)
			if IS_Dataset: 
				#IS Dataset 
				newfilenameIS = file[:3] + 'DMScript Edited Datasets/' + file[3:]
				newdirnameIS = os.path.dirname(newfilenameIS)
				if not os.path.exists(newdirnameIS): os.makedirs(newdirnameIS)
				DM_RGB = CreateDM_RGB(processedframe)
				DM_RGB.SetDimensionCalibration(1,0,(x_scale*binning)*spacing,scale_unit,0)
				DM_RGB.SetDimensionCalibration(0,0,(x_scale*binning)*spacing,scale_unit,0)
				DM_RGB.SaveAsGatan(newfilenameIS)
				del DM_RGB
		if ((num_dims == 3) and (IS_Dataset is True)):
			frame_stack_data = image.GetNumArray()
			digits = int(np.ceil(np.log10(n0)))
			fmt2="{:"+str(digits)+"n}"
			for frameN in range(n0):
				framedata = frame_stack_data[:,:,frameN]
				(processedframe,direction_image,intensity_image,spacing_image,diffractogram_max) = processframe(image,map_var,show_cube,im_data = framedata,RGB_scale_max=RGB_scale_max)
				#IS Dataset 
				newfilenameIS = file[:3] + 'DMScript Edited Datasets/' + file[3:-5]+fmt.format(frameN)+".dm4"
				newdirnameIS = os.path.dirname(newfilenameIS)
				if not os.path.exists(newdirnameIS): os.makedirs(newdirnameIS)
				DM_RGB = CreateDM_RGB(processedframe)
				DM_RGB.SetDimensionCalibration(1,0,(x_scale*binning)*spacing,scale_unit,0)
				DM_RGB.SetDimensionCalibration(0,0,(x_scale*binning)*spacing,scale_unit,0)
				DM_RGB.SaveAsGatan(newfilenameIS)
				del DM_RGB
		
		if Stack: 
			#Stacks
			filename=newdir+"\\png\\"+os.path.basename(newdir)+" "+fmt.format(i)+".png"
			if(i==1):
				print(filename)
				if not os.path.exists(os.path.dirname(filename)): os.makedirs(os.path.dirname(filename))
				shape = direction_image.shape
				direction_stack = np.zeros((len(listOfFiles),shape[0],shape[1]))
				intensity_stack = np.zeros((len(listOfFiles),shape[0],shape[1]))
				spacing_stack = np.zeros((len(listOfFiles),shape[0],shape[1]))
				direction_stack[0,:,:]=direction_image
				intensity_stack[0,:,:]=intensity_image
				spacing_stack[0,:,:]=spacing_image
			else:
				direction_stack[i-1,:,:]=direction_image
				intensity_stack[i-1,:,:]=intensity_image
				spacing_stack[i-1,:,:]=spacing_image
			imsave(filename,processedframe)
		if(i%10==1 or len(listOfFiles)<20): print("Saved Image %s of %s" %(i,len(listOfFiles)))
		#if(i>1): break
	if Stack: 
		dirstackim = DM.CreateImage(direction_stack)
		dirstackim.SetDimensionCalibration(1,0,(x_scale*binning)*spacing,scale_unit,0)
		dirstackim.SetDimensionCalibration(0,0,(x_scale*binning)*spacing,scale_unit,0)
		dirstackim.SetName("FFT Spot Direction of "+os.path.basename(newdir))
		dirstackim.ShowImage()
		del dirstackim
		intstackim = DM.CreateImage(intensity_stack)
		intstackim.SetDimensionCalibration(1,0,(x_scale*binning)*spacing,scale_unit,0)
		intstackim.SetDimensionCalibration(0,0,(x_scale*binning)*spacing,scale_unit,0)
		intstackim.SetName("FFT Spot Intensity of "+os.path.basename(newdir))
		intstackim.ShowImage()
		del intstackim
		spacestackim = DM.CreateImage(spacing_stack/(x_scale*binning))
		spacestackim.SetDimensionCalibration(1,0,(x_scale*binning)*spacing,scale_unit,0)
		spacestackim.SetDimensionCalibration(0,0,(x_scale*binning)*spacing,scale_unit,0)
		spacestackim.SetName("FFT Spot Spacing of "+os.path.basename(newdir))
		spacestackim.ShowImage()
		del spacestackim
	isbasename=os.path.dirname(os.path.dirname(os.path.dirname(newdirnameIS)))
	if GUI_Progress_Bar: plt.close('all')
	return isbasename
