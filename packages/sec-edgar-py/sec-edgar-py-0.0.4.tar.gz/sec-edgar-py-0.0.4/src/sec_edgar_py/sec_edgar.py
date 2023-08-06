import requests
from faker import Faker
from datetime import datetime


class EdgarWrapper:
	def __init__(self):
		self.fake = Faker()
		resp = requests.get('https://www.sec.gov/files/company_tickers.json', headers={'User-Agent': self.generate_random_user_agent()})
		data: dict = resp.json()
		self.ticker_cik = {}
		for d in data.values():
			if str(d['ticker']) not in self.ticker_cik.keys():
				self.ticker_cik[d['ticker']] = str(d['cik_str'])


	def generate_random_user_agent(self):
		return f"{self.fake.first_name()} {self.fake.last_name()} {self.fake.email()}"

	def parse_ticker_cik(self, ticker_or_cik):
		ticker_or_cik = str(ticker_or_cik)
		if len(ticker_or_cik) > 10:
			raise ValueError("CIK numbers should be at most 10 digits long")
		try:
			int(ticker_or_cik)
		except ValueError:
			if ticker_or_cik.upper() not in self.ticker_cik.keys():
				raise ValueError("Invalid ticker")
			else:
				ticker_or_cik = self.ticker_cik[ticker_or_cik.upper()]

		if ticker_or_cik[0] != '0' and ticker_or_cik not in self.ticker_cik.values():
			raise ValueError("Invalid CIK")

		while len(ticker_or_cik) < 10:  # ensure the CIK is filled to 10 digits with leading zeroes
			ticker_or_cik = '0' + ticker_or_cik
		return ticker_or_cik

	def get_company_filings(self, ticker_or_cik, form_types=None, amount=0):
		if form_types is None:
			form_types = []

		cik = self.parse_ticker_cik(ticker_or_cik)

		req_url = f'https://data.sec.gov/submissions/CIK{cik}.json'
		co_filings_resp = requests.get(req_url, headers={'User-Agent': self.generate_random_user_agent()})
		co_filings_data = co_filings_resp.json()
		co_filings = co_filings_data['filings']['recent']

		while cik[0] == '0':
			cik = cik[1:]

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
				"URL": f"https://www.sec.gov/Archives/edgar/data/{cik}/{co_filings['accessionNumber'][n].replace('-', '')}/{co_filings['primaryDocument'][n]}"
			}
			filings_list.append(add_filing)
			idx += 1

		filings = {
			'response': 200,
			'filings': filings_list
		}

		return filings

	def get_company_facts(self, ticker_or_cik):
		cik = self.parse_ticker_cik(ticker_or_cik)
		req_url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
		resp = requests.get(req_url, headers={'User-Agent': self.generate_random_user_agent()})
		if resp.status_code == 404:
			return {'response': 404}
		facts = resp.json()['facts']
		facts['response'] = 200
		facts['taxonomy'] = 'us-gaap' if 'us-gaap' in facts.keys() else 'ifrs-full'
		return facts

	def get_company_concept(self, ticker_or_cik, taxonomy, tag):
		cik = self.parse_ticker_cik(ticker_or_cik)
		req_url = f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/{taxonomy}/{tag}.json'
		resp = requests.get(req_url, headers={'User-Agent': self.generate_random_user_agent()})
		if resp.status_code == 404:
			return {'response': 404}
		concept = resp.json()
		concept['response'] = 200
		return concept

	def get_frames(self, taxonomy, tag, currency, year=None, quarter=None, instantaneous=True):
		if year and year > datetime.utcnow().year:
			raise ValueError("Year cannot be in the future")
		if quarter and int(quarter) not in range(1, 5):
			raise ValueError("Quarter must be either 1, 2, 3 or 4")
		base_url = 'https://data.sec.gov/api/xbrl/frames'
		year = year if year else datetime.utcnow().year
		quarter = 'Q' + str(quarter) if quarter else ''
		instantaneous = 'I' if instantaneous else ''
		req_url = f'{base_url}/{taxonomy}/{tag}/{currency}/CY{str(year)}{quarter}{instantaneous}.json'
		resp = requests.get(req_url, headers={'User-Agent': self.generate_random_user_agent()})
		if resp.status_code == 404:
			return {'response': 404}
		frames = resp.json()
		frames['response'] = 200
		return frames
