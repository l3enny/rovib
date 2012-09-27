""" Subpackage containing rotational constants for various gas molecules.
The use is primarily internal for the pyrov program which automatically
detects the available molecular states. New transitions can be added in
the following manner:

1. Create a folder for the gas in question.
2. Within that folder create a python file for each state containing
   the rotational constants Y, D and B in a dictionary format where
   the keys are integers representing the vibrational state, v
3. Create __init__.py for the folder, and define __all__ for the new
   states.
4. Modify __all__ in this file to reflect any new molecules.
"""

__all__ = ['N2']
