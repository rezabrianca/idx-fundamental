import requests
import gspread
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

today = pd.to_datetime('today').strftime('%Y-%m-%d')
company = pd.read_csv('./data/company_code_{0}.csv'.format(today))

base_url = 'https://www.reuters.com/companies/{0}.JK/key-metrics'
gc = gspread.oauth()

column_list = [
    'company_code',
    'Price closing or last bid',
    '52 Week High',
    '52 Week Low',
    '10 Day Average Trading Volume',
    'Market Capitalization',
    '3 Month Average Trading Volume',
    'Beta',
    '1 Day Price Change',
    '13 Week Price Return (Daily)',
    '26 Week Price Return (Daily)',
    '5 Day Price Return (Daily)',
    '52 Week Price Return (Daily)',
    'Year To Date Price Return (Daily)',
    'Month to Date Price Return (Daily)',
    'Price Relative to S&P500 (4 Week)',
    'Price Relative to S&P500 (13 Week)',
    'Price Relative to S&P500 (26 Week)',
    'Price Relative to S&P500 (52 Week)',
    'Price Relative to S&P500 (YTD)',
    'EPS excl. Extra Items (Annual)',
    'EPS excl. Extra Items (TTM)',
    'EPS Normalized (Annual)',
    'Revenue per Share (Annual)',
    'Revenue per Share (TTM)',
    'Book Value (Per Share Annual)',
    'Book Value (Per Share Quarterly)',
    'Tangible Book Value (Per Share Annual)',
    'Tangible Book Value (Per Share Quarterly)',
    'Cash Per Share (Per Share Annual)',
    'Cash Per Share (Per Share Quarterly)',
    'Cash Flow (Per Share Annual)',
    'Cash Flow (Per Share TTM)',
    'Dividend (Per Share Annual)',
    'Dividends (Per Share TTM)',
    'EBITD (Per Share TTM)',
    'EPS Basic excl. Extra Items (Annual)',
    'EPS Basic excl. Extra Items (TTM)',
    'EPS incl. Extra Items (Annual)',
    'EPS incl. Extra Items (TTM)',
    'Free Cash Flow (Per Share TTM)',
    'Dividend (Per Share 5Y)',
    'P/E excl. Extra Items (Annual)',
    'P/E excl. Extra Items (TTM)',
    'P/E Normalized (Annual)',
    'Price to sales (Annual)',
    'Price to sales (TTM)',
    'Price to Tangible Book (Annual)',
    'Price to Tangible Book (Quarterly)',
    'Price to Free Cash Flow (Per Share Annual)',
    'Price to Cash Flow (Per Share TTM)',
    'Price to Free Cash Flow (Per Share TTM)',
    'Price to Book (Annual)',
    'Price to Book (Quarterly)',
    'P/E Basic excl. Extra Items (TTM)',
    'P/E excl. Extra Items High (TTM)',
    'P/E excl. Extra Items Low (TTM)',
    'P/E incl. Extra Items (TTM)',
    'Net Debt (Interim)',
    'Net Debt (Annual)',
    'Dividend Yield (5Y)',
    'Dividend Yield',
    'Current Dividend Yield (TTM)',
    'Free Cash Flow (Annual)',
    'Current Ratio (Annual)',
    'Net Interest coverage (Annual)',
    'Long Term Debt/Equity (Annual)',
    'Payout Ratio (Annual)',
    'Quick Ratio (Annual)',
    'Total Debt/Total Equity (Annual)',
    'Current EV/Free Cash Flow (Annual)',
    'Current EV/Free Cash Flow (TTM)',
    'Current Ratio (Quarterly)',
    'Long Term Debt/Equity (Quarterly)',
    'Quick Ratio (Quarterly)',
    'Total Debt/Total Equity (Quarterly)',
    'Free Cash Flow (TTM)',
    'Net Interest Coverage (TTM)',
    'Payout Ratio (TTM)',
    'Gross Margin (Annual)',
    'Gross Margin (TTM)',
    'Net Profit Margin % (Annual)',
    'Net Profit Margin (TTM)',
    'Operating Margin (Annual)',
    'Operating Margin (TTM)',
    'Pretax Margin (TTM)',
    'Pretax Margin (Annual)',
    'Operating Margin (5Y)',
    'Pretax Margin (5Y)',
    'Free Operating Cash Flow/Revenue (5Y)',
    'Free Operating Cash Flow/Revenue (TTM)',
    'Gross Margin (5Y)',
    'Net Profit Margin (5Y)',
    'Return on Assets (Annual)',
    'Return on Equity (TTM)',
    'Return on Average Equity (Annual)',
    'Return on Average equity (TTM)',
    'Return on Investment (Annual)',
    'Return on Investment (TTM)',
    'Return on Average Assets (5Y)',
    'Return on Average Equity (5Y)',
    'Return on Investment (5Y)',
    'Asset Turnover (Annual)',
    'Asset Turnover (TTM)',
    'Inventory Turnover (Annual)',
    'Inventory Turnover (TTM)',
    'Net Income/Employee (Annual)',
    'Net Income/Employee (TTM)',
    'Receivables Turnover (Annual)',
    'Receivables Turnover (TTM)',
    'Revenue/Employee (Annual)',
    'Revenue/Employee (TTM)',
    'Revenue Growth (Quarterly YoY)',
    'Revenue Growth Rate (5Y)',
    'EPS Growth (Quarterly YoY)',
    'EPS Growth (TTM YoY)',
    'EPS Growth Rate (5Y)',
    'Dividend Growth Rate (3Y)',
    'Revenue Growth (TTM YoY)',
    'Revenue Growth (Per Share 5Y)',
    'Revenue Growth Rate (3Y)',
    'EPS Growth Rate (3Y)',
    'Book Value Growth Rate (Per Share 5Y)',
    'Tangible Book Value Total Equity CAGR (5Y)',
    'Capital Spending growth rate 5 year',
    'EBITDA CAGR (5Y)',
    'EBITDA Interim CAGR (5Y)',
    'Free Operating Cash Flow CAGR (5Y)',
    'Total Debt CAGR (5Y)',
    'Net Profit Margin Growth Rate (5Y)',
    'Revenue (Annual)',
    'Revenue (TTM)',
    'EBITD (Annual)',
    'EBITD (TTM)',
    'Earnings Before Taxes (Annual)',
    'Earnings Before Taxes (TTM)',
    'Net Income to Common (Annual)',
    'Net Income to Common (TTM)',
    'Earnings Before Taxes Normalized (Annual)',
    'Net Income Available to Common Normalized (Annual)',
    'Diluted Normalized EPS excl. Extra Items (TTM)'
]

price_volume = [
    'company_code',
    'Price closing or last bid',
    '52 Week High',
    '52 Week Low',
    '10 Day Average Trading Volume',
    'Market Capitalization',
    '3 Month Average Trading Volume',
    '1 Day Price Change',
    '13 Week Price Return (Daily)',
    '26 Week Price Return (Daily)',
    '5 Day Price Return (Daily)',
    '52 Week Price Return (Daily)',
    'Year To Date Price Return (Daily)',
    'Month to Date Price Return (Daily)',
    'Price Relative to S&P500 (4 Week)',
    'Price Relative to S&P500 (13 Week)',
    'Price Relative to S&P500 (26 Week)',
    'Price Relative to S&P500 (52 Week)',
    'Price Relative to S&P500 (YTD)'
]

per_share_idr = [
    'company_code',
    'EPS excl. Extra Items (Annual)',
    'EPS excl. Extra Items (TTM)',
    'EPS Normalized (Annual)',
    'Revenue per Share (Annual)',
    'Revenue per Share (TTM)',
    'Book Value (Per Share Annual)',
    'Book Value (Per Share Quarterly)',
    'Tangible Book Value (Per Share Annual)',
    'Tangible Book Value (Per Share Quarterly)',
    'Cash Per Share (Per Share Annual)',
    'Cash Per Share (Per Share Quarterly)',
    'Cash Flow (Per Share Annual)',
    'Cash Flow (Per Share TTM)',
    'Dividend (Per Share Annual)',
    'Dividends (Per Share TTM)',
    'EBITD (Per Share TTM)',
    'EPS Basic excl. Extra Items (Annual)',
    'EPS Basic excl. Extra Items (TTM)',
    'EPS incl. Extra Items (Annual)',
    'EPS incl. Extra Items (TTM)',
    'Free Cash Flow (Per Share TTM)',
    'Dividend (Per Share 5Y)'
]

valuation_idr = [
    'company_code',
    'P/E excl. Extra Items (Annual)',
    'P/E excl. Extra Items (TTM)',
    'P/E Normalized (Annual)',
    'Price to sales (Annual)',
    'Price to sales (TTM)',
    'Price to Tangible Book (Annual)',
    'Price to Tangible Book (Quarterly)',
    'Price to Free Cash Flow (Per Share Annual)',
    'Price to Cash Flow (Per Share TTM)',
    'Price to Free Cash Flow (Per Share TTM)',
    'Price to Book (Annual)',
    'Price to Book (Quarterly)',
    'P/E Basic excl. Extra Items (TTM)',
    'P/E excl. Extra Items High (TTM)',
    'P/E excl. Extra Items Low (TTM)',
    'P/E incl. Extra Items (TTM)',
    'Net Debt (Interim)',
    'Net Debt (Annual)',
    'Dividend Yield (5Y)',
    'Dividend Yield',
    'Current Dividend Yield (TTM)'
]

financial_strength_idr = [
    'company_code',
    'Free Cash Flow (Annual)',
    'Current Ratio (Annual)',
    'Net Interest coverage (Annual)',
    'Long Term Debt/Equity (Annual)',
    'Payout Ratio (Annual)',
    'Quick Ratio (Annual)',
    'Total Debt/Total Equity (Annual)',
    'Current EV/Free Cash Flow (Annual)',
    'Current EV/Free Cash Flow (TTM)',
    'Current Ratio (Quarterly)',
    'Long Term Debt/Equity (Quarterly)',
    'Quick Ratio (Quarterly)',
    'Total Debt/Total Equity (Quarterly)',
    'Free Cash Flow (TTM)',
    'Net Interest Coverage (TTM)',
    'Payout Ratio (TTM)'
]

margins_pct = [
    'company_code',
    'Gross Margin (Annual)',
    'Gross Margin (TTM)',
    'Net Profit Margin % (Annual)',
    'Net Profit Margin (TTM)',
    'Operating Margin (Annual)',
    'Operating Margin (TTM)',
    'Pretax Margin (TTM)',
    'Pretax Margin (Annual)',
    'Operating Margin (5Y)',
    'Pretax Margin (5Y)',
    'Free Operating Cash Flow/Revenue (5Y)',
    'Free Operating Cash Flow/Revenue (TTM)',
    'Gross Margin (5Y)',
    'Net Profit Margin (5Y)'
]

management_effectiveness_idr = [
    'company_code',
    'Return on Assets (Annual)',
    'Return on Equity (TTM)',
    'Return on Average Equity (Annual)',
    'Return on Average equity (TTM)',
    'Return on Investment (Annual)',
    'Return on Investment (TTM)',
    'Return on Average Assets (5Y)',
    'Return on Average Equity (5Y)',
    'Return on Investment (5Y)',
    'Asset Turnover (Annual)',
    'Asset Turnover (TTM)',
    'Inventory Turnover (Annual)',
    'Inventory Turnover (TTM)',
    'Net Income/Employee (Annual)',
    'Net Income/Employee (TTM)',
    'Receivables Turnover (Annual)',
    'Receivables Turnover (TTM)',
    'Revenue/Employee (Annual)',
    'Revenue/Employee (TTM)'
]

growth_pct = [
    'company_code',
    'Revenue Growth (Quarterly YoY)',
    'Revenue Growth Rate (5Y)',
    'EPS Growth (Quarterly YoY)',
    'EPS Growth (TTM YoY)',
    'EPS Growth Rate (5Y)',
    'Dividend Growth Rate (3Y)',
    'Revenue Growth (TTM YoY)',
    'Revenue Growth (Per Share 5Y)',
    'Revenue Growth Rate (3Y)',
    'EPS Growth Rate (3Y)',
    'Book Value Growth Rate (Per Share 5Y)',
    'Tangible Book Value Total Equity CAGR (5Y)',
    'Capital Spending growth rate 5 year',
    'EBITDA CAGR (5Y)',
    'EBITDA Interim CAGR (5Y)',
    'Free Operating Cash Flow CAGR (5Y)',
    'Total Debt CAGR (5Y)',
    'Net Profit Margin Growth Rate (5Y)'
]

income_statement_mil_idr = [
    'company_code',
    'Revenue (Annual)',
    'Revenue (TTM)',
    'EBITD (Annual)',
    'EBITD (TTM)',
    'Earnings Before Taxes (Annual)',
    'Earnings Before Taxes (TTM)',
    'Net Income to Common (Annual)',
    'Net Income to Common (TTM)',
    'Earnings Before Taxes Normalized (Annual)',
    'Net Income Available to Common Normalized (Annual)',
    'Diluted Normalized EPS excl. Extra Items (TTM)'
]

df = pd.DataFrame(columns=column_list)

# exclude missing company info
# may need to maintain this

code = company.Kode[~company.Kode.isin(['GGST', 'GRHA', 'INSA', 'SPOT', 'SUDI', 'ZADI'])]

i = 0
for k in code:
    try:
        print(k)
        req = requests.get(base_url.format(k))
        soup = BeautifulSoup(req.content, 'html.parser')
        status = soup.find('h2', class_='TextLabel__text-label___3oCVw TextLabel__black___2FN-Z TextLabel__medium___t9PWg ErrorPage-status-2Tfzh')
        # print(status)
        if status is not None and status.text == '404':
            print('{0} not found'.format(k))
            pass
        else:
            data = soup.find_all('span', class_='TextLabel__text-label___3oCVw TextLabel__black___2FN-Z TextLabel__regular___2X0ym digits MarketsTable-value-FP5ul')
            value = [d.get_text() for d in data]
            df.loc[i] = [k] + value
            i += 1
    except Exception as e:
        print(e)
        pass

df.to_csv('./data/company_info_{0}.csv'.format(today), index=False)
converted = pd.DataFrame()
converted[df.columns[0]] = df[df.columns[0]]

for i in range(1,len(df.columns)):
    if i != 4:
        converted[df.columns[i]] = [j.replace(',','') for j in df[df.columns[i]]]
        converted[df.columns[i]] = [j.replace('--','') for j in converted[df.columns[i]]]
        converted[df.columns[i]] = [np.round(np.float32(j),2) if j != '' else np.nan for j in converted[df.columns[i]]]
    elif i == 4:
        converted[df.columns[i]] = [np.round(j,2) for j in df[df.columns[i]]]

converted.fillna('', inplace=True)

converted.to_csv('./data/company_convert_{0}.csv'.format(today), index=False)

price_volume_df = converted[price_volume].copy()
per_share_df = converted[per_share_idr].copy()
valuation_df = converted[valuation_idr].copy()
fin_str_df = converted[financial_strength_idr].copy()
margins_df = converted[margins_pct].copy()
mgmt_df = converted[management_effectiveness_idr].copy()
growth_df = converted[growth_pct].copy()
income_df = converted[income_statement_mil_idr].copy()

# update with Google Sheets Key
# sh = gc.open_by_key("GOOGLE_SHEETS_KEY")
worksheet = sh.worksheet("Company Info")
price_vol_ws = sh.worksheet('Price and Volume')
per_share_ws = sh.worksheet('Per Share Data')
valuation_ws = sh.worksheet('Valuation')
fin_str_ws = sh.worksheet('Financial Strength')
margin_ws = sh.worksheet('Margins')
mgmt_ws = sh.worksheet('Management Effectiveness')
growth_ws = sh.worksheet('Growth')
income_ws = sh.worksheet('Income Statement')

print('Uploading to Company Info ...')
worksheet.update([converted.columns.values.tolist()] + converted.values.tolist())
print('Upload Success')

print('Uploading to Price and Volume ...')
price_vol_ws.update([price_volume_df.columns.values.tolist()] + price_volume_df.values.tolist())
print('Upload Success')

print('Uploading to Per Share Data ...')
per_share_ws.update([per_share_df.columns.values.tolist()] + per_share_df.values.tolist())
print('Upload Success')

print('Uploading to Valuation ...')
valuation_df.update([valuation_df.columns.values.tolist()] + valuation_df.values.tolist())
print('Upload Success')

print('Uploading to Financial Strength ...')
fin_str_df.update([fin_str_df.columns.values.tolist()] + fin_str_df.values.tolist())
print('Upload Success')

print('Uploading to Margins ...')
margins_df.update([margins_df.columns.values.tolist()] + margins_df.values.tolist())
print('Upload Success')

print('Uploading to Management Effectiveness ...')
mgmt_df.update([mgmt_df.columns.values.tolist()] + mgmt_df.values.tolist())
print('Upload Success')

print('Uploading to Growth ...')
growth_df.update([growth_df.columns.values.tolist()] + growth_df.values.tolist())
print('Upload Success')

print('Uploading to Income Statement ...')
income_df.update([income_df.columns.values.tolist()] + income_df.values.tolist())
print('Upload Success')
