#!/usr/bin/python3
"""This is an experimentation project with Deep Learning
goal: Make a frontend to choose a dataset, explore, tunning the model
and make some predictions

Author: Jose P. Leitao
Release: 0.0.1
Date: 2025-01-11
"""

"""Main Application"""

#TODO Define the imports
#TODO Criar a GUI
#DONE Obtain list of datasets
#TODO Create the interface
#DONE list them, so the user can choose the dataset
#DONE list the version, on second colum, in case a dataset has more than one version
#TODO load the choosed dataset and version
#TODO Display description of Dataset
#TODO Clean the Dataset
#TODO Choose the model
#TODO Training the model
#TODO Make some prediction




import os
import sys
from app_gui import App

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

if os.getenv('DISPLAY') is None:
    os.environ['DISPLAY'] = ":0.0"

if __name__ == "__main__":
    app = App()
    app.mainloop()
