""" Nipraxis utilities

Nipraxis contains a series of utilities for the Nipraxis course at
https://nipraxis.org

The key function is ``fetch_file``; this fetches data from the nipraxis data
repository, caching in a known location to avoid repeat downloads.

Additional modules are:

* `stimuli``: functions to operate on FMRI run stimulus files.
* `rotations``: functions to work with roations in 3D.
"""

__version__ = '0.3.5'

from ._fetcher import fetch_file
from . import stimuli
from . import rotations
