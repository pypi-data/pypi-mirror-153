import tkinter as tk
import tkinter.filedialog as tkfd
import os
import sys
	
def BrowseforFullFileList():
	"""
	Function to Get List of All Files in In-Situ Dataset (or any other directory tree)

	Returns:
		listOfFiles		(list of strings) list of files in the dataset
		dirname			(string) dataset location
		newdir			(string) directory location (likely not yet existing) where an edited dataset can be saved
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

def GetSelectedFiles():
	"""
	Function to Get List of File Locations for Files Selected with a File Dialog

	Returns:
		listOfFiles		(list of strings) list of files selected by user
    """
	sys.argv.extend(['-a', ' '])
	root = tk.Tk()
	root.withdraw() #use to hide tkinter window
	currdir = os.getcwd()
	listOfFiles = tkfd.askopenfilenames(parent=root,title='Choose Files')
	if len(listOfFiles)>0:
		os.chdir(os.path.dirname(listOfFiles[0]))
	root.destroy()
	return listOfFiles