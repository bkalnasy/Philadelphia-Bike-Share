# Define a function which returns the hours of daylight
# given the day of the year, from 0 to 365
import pandas as pd
import numpy as np
from datetime import datetime

def hours_of_daylight(date, axis=23.44, latitude=39.87):
    """Compute the hours of daylight for the given date"""
    #date = datetime.strptime(start_time, "%Y-%m-%d")
    
    diff = date - pd.datetime(2000, 12, 21)
    day = diff.total_seconds() / 24. / 3600
    day %= 365.25
    m = 1. - np.tan(np.radians(latitude)) * np.tan(np.radians(axis) * np.cos(day * np.pi / 182.625))
    m = max(0, min(m, 2))
    return 24. * np.degrees(np.arccos(1 - m)) / 180.
