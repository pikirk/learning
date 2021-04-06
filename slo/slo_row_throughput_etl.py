import sys
import pytest

def calculateRowThrougputSLO(actual_duration_mins: int, processed_rows: int, target_rows_per_sec: float, nines: float) -> str:
    if (actual_duration_mins <= 0 or target_rows_per_sec <=0 or processed_rows < 0):
        raise ValueError("Attempt to calculate SLO with zero or negative param values")

    if (nines <=0):
        raise ValueError("Attempt to calculate SLO using zero or negative nines")

    # calculate the max error budget
    actual_duration_secs = actual_duration_mins * 60
    actual_rows_sec = (processed_rows / actual_duration_secs)
    threshold = 1 - (nines/100)
    error_budget = ( processed_rows / actual_duration_secs ) * threshold

    print ("Stats:")
    print ("Error Budget: {}".format(error_budget))
    print ("Actual rows/sec: {}".format(actual_rows_sec))
    print ("Target rows/sec:{}".format(target_rows_per_sec))

    # throughtput target exceeded - early return
    if (actual_rows_sec >= target_rows_per_sec):
        return "0.00"

    # calculate the residual throughput difference
    throughput_diff = (target_rows_per_sec - actual_rows_sec) if (target_rows_per_sec - actual_rows_sec) > 0 else abs(target_rows_per_sec - actual_rows_sec)
    print ("Througput diff: {}".format(throughput_diff))

    # calculate used error budget
    result =  100 * ( throughput_diff / error_budget )
    return "{:.2f}".format(result)

def testSLOTargetExceeded():
    #arrange
    duration = 5
    rows = 10000
    target = 10
    nines = 90.0

    #act
    result = calculateRowThrougputSLO(duration, rows, target, nines)

    #assert
    assert result == "0.00" 

def testPassingSLOWhenTargetExceeded():
    #arrange
    duration = 10
    rows = 10000
    target = 17
    nines = 90.0

    #act
    result = calculateRowThrougputSLO(duration, rows, target, nines)

    #assert
    assert result == "20.00" 

def testWarningSLOWhenTargetExceeded():
    #arrange
    duration = 10
    rows = 10000
    target = 17.6
    nines = 90.0

    #act
    result = calculateRowThrougputSLO(duration, rows, target, nines)

    #assert
    assert result == "56.00" # budget burn > 50%

def testErrorSLOWhenTargetExceeded():
    #arrange
    duration = 10
    rows = 10000
    target = 17.93
    nines = 90.0

    #act
    result = calculateRowThrougputSLO(duration, rows, target, nines)

    #assert
    assert result == "75.80" # budget burn > 75%


