# FinancialReporting
Code implementation of Rule 1


## Things to have

Docker compose file with the following services:
- Database (to store ticker name, and associated data): Need to set up tables for type of data we might need (download data, annual, quarterly, processed data)
- Downloader: Pulls (for now) financial information for one ticker and writes to the tables
- Processor: Compute all aggregations needed and write to DB
- Output/Dashboard: Surface all data downloaded and processed 

