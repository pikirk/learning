import sys
import pytest

def calculateCoverageSLO(attempted_rows: int, processed_rows: int, nines: float) -> str:
    ### Calculates the proportion of data processed and available as output for a given reliabiltiy threshold
    ###
    ### Return: Consumed error budget (percent)
    if (attempted_rows <= 0):
        raise ValueError("Attempt to calculate SLO with zero or negative attempted_rows")

    if (nines <=0):
        raise ValueError("Attempt to calculate SLO using zero or negative nines")

    if (attempted_rows == processed_rows):
        return "0.0"

    # calculate the max error budget
    threshold = 1 - (nines/100)
    error_budget = attempted_rows * threshold

    # calculate used error budget
    result =  100 * ( (attempted_rows - processed_rows) / error_budget )
    return "{:.2f}".format(result)

def testAwesomeReliability():
    #arrange
    rows = 1000
    processed = 1000
    threshold = 99.999

    #act
    result = calculateCoverageSLO(rows, processed, threshold)

    #assert
    assert result == "0.0" # unicorn - nothing's perfect


def testOneNine():
    #arrange
    rows = 100
    processed = 95
    threshold = 90.0

    #act
    result = calculateCoverageSLO(rows, processed, threshold)

    #assert
    assert result == "50.00"

def testOneAndAHalfNines():
    #arrange
    rows = 1000
    processed = 997
    threshold = 90.5

    #act
    result = calculateCoverageSLO(rows, processed, threshold)

    #assert
    assert result == "3.16"

def testOneAndAHalfNinesWarning():
    #arrange
    rows = 1000
    processed = 934
    threshold = 90.5

    #act
    result = calculateCoverageSLO(rows, processed, threshold)

    #assert
    assert result == "69.47" # error budget burn >50%

def testTwoNinesFailing():
    #arrange
    rows = 1000
    processed = 990
    threshold = 99

    #act
    result = calculateCoverageSLO(rows, processed, threshold)

    #assert
    assert result == "100.00" # error budget burn >= 100%