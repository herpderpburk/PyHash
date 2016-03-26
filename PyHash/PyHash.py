import os, hashlib

path = 'josephburkey/PythonHash/'
path = 'josephburkey/PythonHash/Movies'
path = 'josephburkey/PythonHash/TV'

subdires = [] #retrieves list of subdirectories
files = [] #retrieves list of files within subdirectories

for root, dirs, filenames, in os.walk(path):
    for subdir in dirs:
        subdirs.append(os.path.relpath(os.path.join(root,subdir),path))

        for name in filenames:
            files.append(os.path.relpath(os.path.join(root,name),path))
                       

