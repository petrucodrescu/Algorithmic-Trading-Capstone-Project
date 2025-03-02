"""Set of functions to get ticker name, company name, and other identifying
features from NYSE, NASDAQ, S&P500 Individual and ETFS.
Also, share class relationships are established.

NYSE and NASDAQ code is  based on two original scripts by Joe Hand
and datahub.io that grab stock listing data from the Nasdaq FTP.
https://github.com/datasets/nyse-other-listings/blob/main/README.md
https://github.com/datasets/nasdaq-listings/blob/main/README.md

ETFS scraped from https://etfdb.com/, using the etfpy library:
https://github.com/JakubPluta/pyetf.

Original code licensed for data processing under PDDL.
Refer to NASDAQ data copyright: © 2010, The NASDAQ OMX Group, Inc.

Modifications by Erin Xu, 2025.

    - Downloads data from FTP
    - Does some basic cleaning
    - Creates 4 CSV files:
        1. nyse-listed.csv for NYSE equities
        2. nasdaq-listed.csv
        3.
        4.
    - Creates datapackage.json file w/ schema

    Data Source: ftp://ftp.nasdaqtrader.com/symboldirectory/
    Data Documentation: http://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs"""

import pandas as pd
import json
import os
import requests
from etfpy import ETF, load_etf, get_available_etfs_list

PACKAGE_NAME = 'nyse-listings'
PACKAGE_TITLE = 'NYSE Listings'

NYSE_URL = 'ftp://ftp.nasdaqtrader.com/symboldirectory/otherlisted.txt'
NASDAQ_URL = 'https://www.nasdaqtrader.com/dynamic/symdir/nasdaqlisted.txt'
SNP_INDIVIDUAL_URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks'
SNP_SECTOR_URL = 'https://www.spglobal.com/spdji/en/index-family/equity/us-equity/sp-sectors/#indices'

def process_nasdaq():
    try:
        resp = requests.get(NASDAQ_URL)

        data = resp.text.split('\n')
        data = [row.split('|') for row in data]
        df = pd.DataFrame(data[1:], columns=data[0])

        # Transform data
        df.columns = df.columns.str.replace('\r', '', regex=False)
        df = df.map(lambda x: x.replace('\r', '') if isinstance(x, str) else x)

        # Create nasdaq_listed.csv
        nasdaq_listed = df[['Symbol', 'Security Name']]
        nasdaq_listed.to_csv('data/nasdaq-listed.csv', index=False)
        nasdaq_listed_symbol = df
        nasdaq_listed_symbol['Company Name'] = nasdaq_listed_symbol['Security Name'].str.split(' - ').str[0].str.replace("",'').str.strip()
        print('nasdaq-listed.csv saved.')

    except Exception as e:
        print(f"Error fetching/saving NASDAQ data: {e}")

def process_nyse():
    try:
        # Load the data from the provided FTP link
        other = pd.read_csv(NYSE_URL, sep='|')

        # Clean the data and filter for NYSE only
        other = _clean_data(other)
        nyse = other[other['Exchange'] == 'N'][['ACT Symbol', 'Company Name']]  # NYSE Only

        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)

        # Save the NYSE listings dataset
        nyse.to_csv('data/nyse-listed.csv', index=False)

        print('nyse_listed.csv saved.')
        # Create datapackage.json
        with open("data/datapackage.json", "w") as outfile:
            json.dump(_create_datapackage([(nyse, 'nyse-listed')]), outfile, indent=4, sort_keys=True)

    except Exception as e:
        print(f"Error fetching/saving NYSE data: {e}")


def _clean_data(df):
    df = df.copy()

    # Remove test listings
    df = df[df['Test Issue'] == 'N']

    # Create New Column with Just Company Name
    df['Company Name'] = df['Security Name'].apply(lambda x: x.split('-')[0])

    # Move 'Company Name' to 2nd Column
    cols = list(df.columns)
    cols.insert(1, cols.pop(-1))

    # Replacing df.ix with df.loc
    df = df.loc[:, cols]  # Using loc for label-based indexing

    return df


def _create_file_schema(df, filename):
    fields = []
    for name, dtype in zip(df.columns, df.dtypes):
        if str(dtype) == 'object' or str(dtype) == 'bool':  # Updated 'boolean' type check
            dtype = 'string'
        else:
            dtype = 'number'

        fields.append({'name': name, 'description': '', 'type': dtype})

    return {
        'name': filename,
        'path': f'data/{filename}.csv',
        'format': 'csv',
        'mediatype': 'text/csv',
        'schema': {'fields': fields}
    }


def _create_datapackage(datasets):
    resources = []
    for df, filename in datasets:
        resources.append(_create_file_schema(df, filename))

    return {
        'name': PACKAGE_NAME,
        'title': PACKAGE_TITLE,
        'license': '',
        'resources': resources,
    }

def process_snp500_individual():
    try:
        df = pd.read_html(SNP_INDIVIDUAL_URL, header=0)[0]
        columns_to_remove = ["GICS Sub-Industry", "Headquarters Location", "Date added", "CIK", "Founded"]  # Replace with the column names you want to drop
        df = df.drop(columns=columns_to_remove)

        df.to_csv('data/snp_individual.csv')
        print('snp_individual.csv saved.')
        return df
    except Exception as e:
        print(f"Error fetching/saving S&P 500 individual indexes: {e}")
        return None

def process_etfs():
    etfs_list = get_available_etfs_list()
    df = pd.DataFrame(etfs_list, columns=["Symbol"])
    df.to_csv("data/etfs.csv", index=False)

    print("etfs.csv saved.")

def find_share_classes():
    """
    for  stocks, indexes and etfs
    store in "share_classes_[equity type].csv"
    """
    df_nasdaq = pd.read_csv("data/nasdaq-listed.csv")
    df_nasdaq['Security Name'] = df_nasdaq['Security Name'].astype(str).str.strip('"').str.strip()
    df_nasdaq.to_csv("data/nasdaq-listed.csv", index=False)
    matches_nasdaq = []
    for i in range(len(df_nasdaq) - 1):
        current_name = df_nasdaq.loc[i, 'Security Name']
        previous_name = df_nasdaq.loc[i + 1, 'Security Name']

        current_first_word = current_name.split()[0]
        previous_first_word = previous_name.split()[0]

        if current_first_word == previous_first_word:
            matches_nasdaq.append(df_nasdaq.loc[i, ['Symbol', 'Security Name']])
            matches_nasdaq.append(df_nasdaq.loc[i + 1, ['Symbol', 'Security Name']])

    matches_df_nasdaq = pd.DataFrame(matches_nasdaq)
    matches_df_nasdaq.to_csv("data/share_classes_nasdaq.csv", index=False)
    print(f"Matches saved to share_classes_nasdaq.csv")

    # #for nyse
    df_nyse = pd.read_csv("data/nyse-listed.csv")
    matches_nyse = []
    for i in range(len(df_nyse) - 1):
        current_name = df_nyse.loc[i, 'Company Name']
        previous_name = df_nyse.loc[i + 1, 'Company Name']

        current_first_word = current_name.split()[0]
        previous_first_word = previous_name.split()[0]

        if current_first_word == previous_first_word:
            matches_nyse.append(df_nyse.loc[i, ['ACT Symbol', 'Company Name']])
            matches_nyse.append(df_nyse.loc[i + 1, ['ACT Symbol', 'Company Name']])

    matches_df_nyse= pd.DataFrame(matches_nyse)
    matches_df_nyse.to_csv("data/share_classes_nyse.csv", index=False)
    print(f"Matches saved to share_classes_nyse.csv.csv")

    #for s&p individual
    df = pd.read_csv("data/snp_individual.csv")
    matches = []
    for i in range(len(df) - 1):
        current_name = df.loc[i, 'Security']
        previous_name = df.loc[i + 1, 'Security']

        current_first_word = current_name.split()[0]
        previous_first_word = previous_name.split()[0]

        if current_first_word == previous_first_word:
            matches.append(df.loc[i, ['Symbol', 'Security']])
            matches.append(df.loc[i + 1, ['Symbol', 'Security']])

    matches_df = pd.DataFrame(matches)
    matches_df.to_csv("data/share_classes_snp_individual.csv", index=False)
    print(f"Matches saved to share_classes_snp_individual.csv")



if __name__ == '__main__':
    process_nyse()
    process_nasdaq()
    process_snp500_individual()
    process_etfs()
    find_share_classes()
