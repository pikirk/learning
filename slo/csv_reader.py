import pytest
import math
import pandas as pd


def testReadFile():
    #arrange
    data = pd.read_csv("./data.csv")
    
    #act
    # print columns
    print (data.columns)

    # remap column names based on names from above
    # does not work
    data.rename(columns={' AvailableRows': 'AvailableRows'})

    # remove spaces between delimeters on header and rows
    rows = data.AvailableRows
    print (data.columns)
    print (rows)



