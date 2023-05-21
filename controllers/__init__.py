import os
import glob

try:
    __all__=[os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py" )]
except:
    print("Such file not in directory")