"""
The script contains utility function to print error traceback.
"""

#imports
from sys import exc_info
from traceback import print_tb

def generate_traceback():
    """
    The function will generate traceback when error occured.
    :param: None
    :return: None
    """
    error_name, error_value, error_traceback = exc_info()
    print(error_name, error_value)
    print_tb(error_traceback)