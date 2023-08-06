import requests


class EdgarWrapper:
	def __init__(self):
		self.headers = {'User-Agent': "sec-edgar.py robinweaver2001@gmail.com"}
		resp = requests.get('https://www.sec.gov/files/company_tickers.json', headers=self.headers)
		data: dict = resp.json()
		self.ticker_cik = {}
		for d in data.values():
			if str(d['ticker']) not in self.ticker_cik.keys():
				self.ticker_cik[d['ticker']] = str(d['cik_str'])

	def get_company_filings(self, ticker_or_cik, form_types=None, amount=0):
		if form_types is None:
			form_types = []
		ticker_or_cik = str(ticker_or_cik)
		try:
			int(ticker_or_cik)
			if len(ticker_or_cik) > 10:
				raise ValueError("CIK numbers should be at most 10 digits long")
		except ValueError:
			if ticker_or_cik.upper() not in self.ticker_cik.keys():
				raise ValueError("Invalid ticker")
			else:
				ticker_or_cik = self.ticker_cik[ticker_or_cik.upper()]

		while len(ticker_or_cik) < 10:  # ensure the CIK is padded to 10 digits with leading zeroes
			ticker_or_cik = '0' + ticker_or_cik
		req_url = f'https://data.sec.gov/submissions/CIK{ticker_or_cik}.json'
		co_filings_resp = requests.get(req_url, headers=self.headers)
		co_filings_data = co_filings_resp.json()
		co_filings = co_filings_data['filings']['recent']

		while ticker_or_cik[0] == '0':
			ticker_or_cik = ticker_or_cik[1:]

		filings_list = []
		amount = len(co_filings['form']) if amount == 0 else amount
		idx = 0
		for n in range(len(co_filings['form'])):
			if idx == amount:
				break
			if co_filings['form'][n] not in form_types and len(form_types) > 0:
				continue

			add_filing = {
				"form": co_filings['form'][n],
				"filingDate": co_filings['filingDate'][n],
				"URL": f"https://www.sec.gov/Archives/edgar/data/{ticker_or_cik}/{co_filings['accessionNumber'][n].replace('-', '')}/{co_filings['primaryDocument'][n]}"
			}
			filings_list.append(add_filing)
			idx += 1

		return filings_list
