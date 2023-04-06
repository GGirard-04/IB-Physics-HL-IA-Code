# Gavin Girard - April 2023

def get_stat_mean(data_set):
    if len(data_set) == 0:
        return None
    final_sum = 0
    for item in data_set:
        final_sum += item
    return final_sum / len(data_set)

def get_stat_min(data_set, selector=None):
    lowest_item = None
    compared_val = None
    for item in data_set:
        selected = selector(item) if selector else item
        if not compared_val or selected < compared_val:
            lowest_item = item
            compared_val = selected
    return lowest_item

def get_stat_max(data_set, selector=None):
    highest_item = None
    compared_val = None
    for item in data_set:
        selected = selector(item) if selector else item
        if not compared_val or selected > compared_val:
            highest_item = item
            compared_val = selected
    return highest_item

def get_stat_error(accepted_value: float, experimental_value: float) -> float:
    return 100 * abs(experimental_value - accepted_value) / accepted_value