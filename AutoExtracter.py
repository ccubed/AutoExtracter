# AutoExtracter.py
#
# I download a lot of compressed files and want a quicker way to unpack them all. I use 7zip just because it does everything.
# 7Zip needs to be in the directory of the script. From there, just pass it the folder of the compressed files and it'll sort
# everything out.
#
# Using 7zip command line interface exe. I do not own this program and do not distribute it. Just download it on their website.
#
# Extracts to a folder named Extracted and then separates into folders based on name of archive.
# Example: This.rar ends up in Extracted/This/
#
# Author: Cooper AKA Gizmo
import os,sys,os.path,subprocess

if len(sys.argv) < 2:
	print("No Folder specified for compressed files.\nUsage: python autoextracter.py <folder>")
	sys.exit()
elif sys.argv[1] == "" or sys.argv[1] is None:
	print("No Folder specified for compressed files.\nUsage: python autoextracter.py <folder>")
	sys.exit()
elif not os.path.isdir(sys.argv[1]) or not os.path.exists(sys.argv[1]):
	print("Path ",sys.argv[1]," does not exist or is not a directory.")
	sys.exit()
else:
	BASE_PATH = sys.argv[1]
	#Error Checking, so we don't accidentally overwrite existing files. Better safe than sorry. 
	#Also reminds me to do something with them.
	if not os.path.exists("Extracted"):
		try:
			os.mkdir("Extracted")
		except:
			print("Error occured when making directory Extracted.\nError: ",sys.exc_info()[0])
			sys.exit()
	else:
		if os.listdir("Extracted"):
			print("Stopping Execution. Extracted exists and has files inside. Please clear the files or rename the directory.")
			sys.exit()
		else:
			#Error Checking done. Extracted now exists and has no files. Begin Extraction
			Filelist = os.listdir(BASE_PATH)
			Item = 0
			Partfiles = [] #part files
			Files = [] #straight files
			Directories = [] #directories
			FinalFiles = [] #Actual files we need to extract
			#First, find part files and separate them. Also separate out directories
			for fname in Filelist:
				if os.path.isdir(os.path.join(BASE_PATH,fname)):
					Directories.append(fname)
				elif "part" in fname:
					Partfiles.append(fname)
				else:
					Files.append(fname)
			#Get files out of directories (and more directories out of these directories)
			for DirName in Directories:
				Filelist = os.listdir(os.path.join(BASE_PATH,DirName))
				for fname in Filelist:
					if os.path.isdir(os.path.join(BASE_PATH,DirName,fname)):
						Directories.append(os.path.join(BASE_PATH,DirName,fname))
					elif "part" in fname:
						Partfiles.append(os.path.join(BASE_PATH,DirName,fname))
					else:
						Files.append(os.path.join(BASE_PATH,DirName,fname))
			#At this point, we should have a list of every file in every directory in the path
			print("Overview of files found.\n\nDirectories:",Directories,"\n\nPartfiles:",Partfiles,"\n\nFiles:",Files)