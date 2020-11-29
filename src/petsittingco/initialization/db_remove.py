import os
import glob

contents = glob.glob(str(os.getcwd())+"/src/petsittingco/databases/*")
for file in contents:
    print("Removing",file)
    os.remove(file)