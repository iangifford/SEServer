import os
import glob
print(os.getcwd())
contents = glob.glob(str(os.getcwd())+"/src/petsittingco/databases/*")
for file in contents:
    print(file)
    os.remove(file)