# The main class for financial data


class FinancialData:

    """
    Main class for financial data
    Steps: Put ticker in, download data from a source (can be several),
            Generate the growth report, which will calculate all the growth statistics
            and produce the 10, 5, 3 and 1 year growths
            for Equity, EPS, Sales/Gross Profit, and ROIC

    """

    def __init__(self, ticker):

        self.ticker = ticker

    def download_ticker_financials(self):
        pass

    def calculate_growth_statistics(self):
        pass

    def generate_growth_report(self):
        pass

