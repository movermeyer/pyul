import sys

if sys.version_info < (2, 7):
    from path import Path
else: #Pathlib seems to only support python 2.7 and up
    from pathlib import Path


del sys