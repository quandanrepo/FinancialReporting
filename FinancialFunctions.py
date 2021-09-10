# Functions to calculate financial statistics


def calculate_average_annual_growth(start, end, num_years):
    """

    Calculates the average annual (compounded) growth rate 

    :param start: numeric
    :param end: numeric
    :param num_years: numeric
    :return: numeric, annual interest rate
    """

    # Using the formula: end = start *((1+y)^num_years)
    return (end/start)**(1/float(num_years))

def calculate_growth_df():
    """

    :return:
    """




start = 0.26
end = 1.89
num_years = 9

calculate_average_annual_growth(start, end, num_years)