"""
Global variables.
"""
import os
from pathlib import Path


MNI_DATAPATH = Path(os.environ['MNI_DATAPATH'])
"""
Location of data such as starting ellipsoids for surface extraction.
"""
