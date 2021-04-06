import sys
import pytest

def calculateThrougputSLO(actual_duration_mins: int, target_duration_mins: int, nines: float) -> str:
    if (actual_duration_mins <= 0 or target_duration_mins <=0):
        raise ValueError("Attempt to calculate SLO with zero or negative durations")

    if (nines <=0):
        raise ValueError("Attempt to calculate SLO using zero or negative nines")

    if (actual_duration_mins == target_duration_mins):
        return "0.0"

    # calculate the max error budget
    threshold = 1 - (nines/100)
    error_budget = actual_duration_mins * threshold

    # calculate the residual time - the amount of time greater than target_duration mins
    extra_time = (target_duration_mins - actual_duration_mins) if (target_duration_mins - actual_duration_mins) > 0 else abs(target_duration_mins - actual_duration_mins)

    # calculate used error budget
    result =  100 * ( extra_time / error_budget )
    return "{:.2f}".format(result)

def testPassingLSLOWhenTargetExceeded():
    #arrange
    duration = 100
    target = 105
    nines = 90.0

    #act
    result = calculateThrougputSLO(duration, target, nines)

    #assert
    assert result == "50.00" # half of the error budget spent 

def testFailingSLOWhenTargetExceeded():
    #arrange
    duration = 100
    target = 120
    nines = 90.0

    #act
    result = calculateThrougputSLO(duration, target, nines)

    #assert
    assert result == "200.00" # failing SLO

def testAwesomeReliability():
    #arrange
    duration = 100
    target = 100
    nines = 99.999

    #act
    result = calculateThrougputSLO(duration, target, nines)

    #assert
    assert result == "0.0" # unicorn - nothing's perfect


def testOneNine():
    #arrange
    duration = 100
    target = 95
    nines = 90.0

    #act
    result = calculateThrougputSLO(duration, target, nines)

    #assert
    assert result == "50.00"

def testOneAndAHalfNines():
    #arrange
    duration = 1000
    target = 997
    nines = 90.5

    #act
    result = calculateThrougputSLO(duration, target, nines)

    #assert
    assert result == "3.16"

def testOneAndAHalfNinesWarning():
    #arrange
    duration = 1000
    target = 934
    nines = 90.5

    #act
    result = calculateThrougputSLO(duration, target, nines)

    #assert
    assert result == "69.47" # error budget burn >50%

def testTwoNinesFailing():
    #arrange
    duration = 1000
    target = 990
    nines = 99

    #act
    result = calculateThrougputSLO(duration, target, nines)

    #assert
    assert result == "100.00" # error budget burn >= 100%