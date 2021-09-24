from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import InvalidArgumentException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# Setting display limit for printing
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)


class DataDownloader:

    URL_PREFIX = "http://financials.morningstar.com/ratios/r.html?t="

    def __init__(self, ticker):
        self.ticker = ticker
        self.options = None
        self.driver = None
        self.data = None
        self.has_ttm = None
        self.growth_df = pd.DataFrame()
        self.growth_df_ttm = pd.DataFrame()

    def init_selenium_options(self):
        self.options = Options()
        self.options.headless = True

    def start_selenium(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)

    def selenium_soup(self, parser='html.parser'):
        try:
            self.driver.get(self.URL_PREFIX + self.ticker.upper())
        except InvalidArgumentException as e:
            raise Exception('Invalid argument: {}'.format(e)) from None
        return BeautifulSoup(self.driver.page_source, parser)

    def stop_selenium(self):
        self.driver.quit()

    def download(self):
        """
        This runs the initialization of selenium, downloads the team url, downloads the team page, extracts all tables,
        :return: Boolean True
        """
        self.init_selenium_options()
        self.start_selenium()

        soup = self.selenium_soup()

        if len(soup.find_all('table')) == 0:
            print('Ticker can not be found - try another')
            self.stop_selenium()
            return None

        df = pd.read_html(str(soup))[0]
        self.stop_selenium()

        df = df[df.index % 2 != 0].\
            rename(columns={'Unnamed: 0': ''}).\
            set_index('', drop=True).\
            transpose()

        df.columns = df.columns.\
            str.replace('USD Mil', '').\
            str.replace('%', '').\
            str.replace('*', '').\
            str.replace('USD', '').\
            str.strip().\
            str.lower().\
            str.replace(' ', '_').\
            str.replace('\xa0', '_')  # To catch a funny weird space in shares mil

        self.data = df.replace('—', '0').astype('float')

    def calculate_growth(self, col_name, years=None):

        col_name_to_replace = self.data.columns[self.data.columns.str.contains(col_name)][0]
        self.data = self.data.rename({col_name_to_replace: col_name}, axis=1)

        if years is None:
            years = [1, 3, 5, 7]

        tail_length = 2 if self.has_ttm else 1

        growth_dict = {}
        for year in years:
            growth_dict[str(year)+'_year_average'] = \
                ((self.data[col_name] / self.data[col_name].shift(year)) ** (1 / year)).tail(tail_length)

        df = pd.DataFrame(growth_dict).transpose()

        growth_df = df[[df.columns[0]]]
        growth_df.columns = [col_name]

        if self.has_ttm:
            growth_df_ttm = df[[df.columns[1]]]
            growth_df_ttm.columns = [col_name]
        else:
            growth_df_ttm = pd.DataFrame()

        self.growth_df = pd.concat([self.growth_df, growth_df], axis=1)
        self.growth_df_ttm = pd.concat([self.growth_df_ttm, growth_df_ttm], axis=1)

    def sticker_price(self):

        self.data['earnings_per_share']

    def process(self):

        self.download()

        self.has_ttm = True if any(downloader.data.index.str.contains('TTM')) else False

        # Equity/ Book value
        self.calculate_growth(col_name='book_value_per_share')
        self.calculate_growth(col_name='earnings_per_share')
        self.calculate_growth(col_name='revenue')
        self.calculate_growth(col_name='free_cash_flow')
        self.calculate_growth(col_name='operating_cash_flow')

        # Sticker price
        self.sticker_price()

downloader = DataDownloader(ticker='NVDA')
# downloader.download()
downloader.process()
downloader.growth_df
downloader.growth_df_ttm





if __name__ == '__main__':
    DataDownloader()
