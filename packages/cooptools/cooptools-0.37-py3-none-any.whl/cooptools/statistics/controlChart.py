from typing import Dict, List, Union, Any
import numpy as np
from cooptools.statistics.trends import *

def control(data: List[Union[int, float]],
            set_baseline_periods: int = None,
            trailing_window: int = None) -> List[Dict[str, Any]]:
    """ Takes a set of data and determines if it statistically in control

    :param: data: List of integers or floats that represents the data set to evaluate
    :param: set_baseline_periods: The number of periods that must pass before evaluating the statistics
    :param: trailing_window: The amount of past periods to evaluate for control (should be at least 15 since control includes
     checks of at least past 15 periods
    :return: List Dict of values by period
    """

    # init optional params
    if set_baseline_periods is None:
        set_baseline_periods = 10

    if trailing_window is None:
        trailing_window = 20

    if trailing_window <= 0:
        raise ValueError(f"The trailing window must be greater than zero. Ideally, this value is at least 20")

    # init the tracking dicts
    deltas = {}
    stdevs = {}
    means = {}
    lcls = {}
    ucls = {}
    out_of_limit_high = {}
    out_of_limit_low = {}
    two_of_three_high_2stdev = {}
    two_of_three_low_2stdev = {}
    four_of_five_high_1stdev = {}
    four_of_five_low_1stdev = {}
    seven_high = {}
    seven_low = {}
    seven_trend_high = {}
    seven_trend_low = {}
    eight_out_of_1stdev = {}
    fifteen_within_1stdev = {}
    fourteen_alternate = {}
    out_of_control = {}

    # iterate the data
    for ii in range(0, len(data)):
        # track deltas
        deltas[ii] = data[ii] - data[ii-1] if ii > 0 else None

        # track means and stdevs
        start_period = max(0, ii - trailing_window)
        means[ii] = round(np.mean(data[start_period: ii]), 3) if ii > set_baseline_periods else None
        stdevs[ii] = round(np.std(data[start_period:ii]), 3) if ii > set_baseline_periods else None

        # track LCL and UCL
        lcls[ii] = (means[ii] - 3 * stdevs[ii]) if ii > set_baseline_periods else None
        ucls[ii] = means[ii] + 3 * stdevs[ii] if ii > set_baseline_periods else None

        # Track control rules
        out_of_limit_high[ii] = len([x for x in data[start_period:ii] if x > ucls[ii]]) > 0 if ii > set_baseline_periods else None
        out_of_limit_low[ii] = len([x for x in data[start_period:ii] if x < lcls[ii]]) > 0 if ii > set_baseline_periods else None
        two_of_three_high_2stdev[ii] = len([x for x in data[max(ii-3, start_period):ii] if x > (means[ii] + 2 * stdevs[ii])]) >= 2 if ii > set_baseline_periods else None
        two_of_three_low_2stdev[ii] = len([x for x in data[max(ii-3, start_period):ii] if x < (means[ii] - 2 * stdevs[ii])]) >= 2 if ii > set_baseline_periods else None
        four_of_five_high_1stdev[ii] = len([x for x in data[max(ii-5, start_period):ii] if x > (means[ii] + stdevs[ii])]) >= 4 if ii > set_baseline_periods else None
        four_of_five_low_1stdev[ii] = len([x for x in data[max(ii-5, start_period):ii] if x < (means[ii] - stdevs[ii])]) >= 4 if ii > set_baseline_periods else None
        seven_high[ii] = len([x for x in data[max(ii-7, start_period):ii] if x > means[ii]]) == 7 if ii > set_baseline_periods else None
        seven_low[ii] = len([x for x in data[max(ii-7, start_period):ii] if x < means[ii]]) == 7 if ii > set_baseline_periods else None
        seven_trend_high[ii] = strictly_increasing(data[max(ii-7, start_period):ii]) if ii > set_baseline_periods else None
        seven_trend_low[ii] = strictly_decreasing(data[max(ii-7, start_period):ii]) if ii > set_baseline_periods else None
        eight_out_of_1stdev[ii] = len([x for x in data[max(ii-8, start_period):ii] if x < means[ii] - stdevs[ii] or x > means[ii] + stdevs[ii]]) == 8 if ii > set_baseline_periods else None
        fifteen_within_1stdev[ii] = len([x for x in data[max(ii-15, start_period):ii] if x < means[ii] + stdevs[ii] and x > means[ii] - stdevs[ii]]) == 15 if ii > set_baseline_periods else None
        fourteen_alternate[ii] = alternating([x for x in list(deltas.values())[max(ii-14, start_period):ii] if x]) if ii > set_baseline_periods else None
        out_of_control[ii] = out_of_limit_high[ii] or \
                             out_of_limit_low[ii] or \
                             two_of_three_high_2stdev[ii] or \
                             two_of_three_low_2stdev[ii] or \
                             four_of_five_high_1stdev[ii] or \
                             four_of_five_low_1stdev[ii] or \
                             seven_high[ii] or \
                             seven_low[ii] or \
                             seven_trend_high[ii] or \
                             seven_trend_low[ii] or \
                             eight_out_of_1stdev[ii] or \
                             fifteen_within_1stdev[ii] or \
                             fourteen_alternate[ii] if ii > set_baseline_periods else None


    # format and return
    data = [{'index': x,
             'data_point': data[x],
             'delta': deltas[x],
             'mean': means[x],
             'stdev': stdevs[x],
             'lcl': lcls[x],
             'ucl': ucls[x],
             'out_of_limit_high': out_of_limit_high[x],
             'out_of_limit_low': out_of_limit_low[x],
             'two_of_three_high_2stdev': two_of_three_high_2stdev[x],
             'two_of_three_low_2stdev': two_of_three_low_2stdev[x],
             'four_of_five_high_1stdev': four_of_five_high_1stdev[x],
             'four_of_five_low_1stdev': four_of_five_low_1stdev[x],
             'seven_high': seven_high[x],
             'seven_low': seven_low[x],
             'seven_trend_high': seven_trend_high[x],
             'seven_trend_low': seven_trend_low[x],
             'eight_out_of_1stdev': eight_out_of_1stdev[x],
             'fifteen_within_1stdev': fifteen_within_1stdev[x],
             'fourteen_alternate': fourteen_alternate[x],
             'out_of_control': out_of_control[x]} for x in range(len(data))]
    return data

def control_data_and_deltas(data: List[Union[int, float]],
                            set_baseline_periods: int = None,
                            trailing_window: int = None
                            ) -> List[Dict[str, Any]]:
    """
    Calculates the control of both raw data and the deltas of that data to check for overall control

    :param data: raw data to be analyzed
    :param: set_baseline_periods: The number of periods that must pass before evaluating the statistics
    :param: trailing_window: The amount of past periods to evaluate for control (should be at least 15 since control includes
     checks of at least past 15 periods
    :return: List Dict of values by period
    """
    # gather control of raw data
    controlled_data = control(data, set_baseline_periods, trailing_window)

    # gather control of deltas
    deltas = [x['delta'] for x in controlled_data][1:]
    controlled_deltas = control(deltas, set_baseline_periods, trailing_window)
    controlled_deltas.insert(0, {x: None for x in controlled_deltas[0].keys()})

    # merge and return
    ret = []
    for ii in range(len(controlled_data)):
        controlled_deltas[ii] = {f'delta_{key}': value for key, value in controlled_deltas[ii].items()}
        ret.append({**controlled_data[ii], **controlled_deltas[ii]})

    return ret



if __name__ == "__main__":
    import random as rnd
    import pandas as pd
    import cooptools.pandasHelpers as ph
    data = [rnd.randint(0, 100) for ii in range(50)]
    cc = pd.DataFrame(control_data_and_deltas(data))
    ph.pretty_print_dataframe(cc)




