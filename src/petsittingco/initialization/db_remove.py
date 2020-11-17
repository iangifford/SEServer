import os
import glob
print(os.getcwd())
contents = glob.glob(str(os.getcwd())+"/databases/*")
for file in contents:
    os.remove(file)