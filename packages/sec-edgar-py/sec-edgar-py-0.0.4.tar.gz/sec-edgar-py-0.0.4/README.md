# sec-edgar.py
A basic (unofficial) Python API wrapper for the SEC's EDGAR system

## Documentation

The aim of this project is to make the SEC's EDGAR system more accessible to python programmers, performing all of the "messy" work so the user can make simple requests and receive clean results.
Still very much a WIP.

### Getting Started

Start off by importing the base class from the main file and instantiating it.
```py
from sec_edgar_py import EdgarWrapper
client = EdgarWrapper()
```
Now you can call all of the methods from `client`.

### Filings
```py 
client.get_company_filings(ticker_or_cik, form_types=None, amount=0)
```

Where:
  * `ticker_or_cik` can be either the company ticker, or the CIK.
  * `form_types` if specified, must be a list of the types of filings you wish to retrieve.
  * `amount` is the amount of filings you wish to retrieve. If unspecified or 0, all available filings will be retrieved.

This method returns the requested filings, with the most recent filings first.
 
So:

`client.get_company_filings('abbv', form_types=['10-K', '10-Q'], amount=5)`

will return:
```py 
{'response': 200,
 'filings': [
  {'form': '10-Q',
   'filingDate': '2022-05-06',
   'URL': 'https://www.sec.gov/Archives/edgar/data/1551152/000155115222000017/abbv-20220331.htm'},
  {'form': '10-K',
   'filingDate': '2022-02-18',
   'URL': 'https://www.sec.gov/Archives/edgar/data/1551152/000155115222000007/abbv-20211231.htm'},
  {'form': '10-Q',
   'filingDate': '2021-11-02',
   'URL': 'https://www.sec.gov/Archives/edgar/data/1551152/000155115221000031/abbv-20210930.htm'},
  {'form': '10-Q',
   'filingDate': '2021-08-02',
   'URL': 'https://www.sec.gov/Archives/edgar/data/1551152/000155115221000025/abbv-20210630.htm'},
  {'form': '10-Q',
   'filingDate': '2021-05-07',
   'URL': 'https://www.sec.gov/Archives/edgar/data/1551152/000155115221000016/abbv-20210331.htm'}
 ]
}
```

### Company Facts
```py 
client.get_company_facts(ticker_or_cik)
```

Where `ticker_or_cik` is the ticker or CIK of the company you wish to retrieve facts for. This method returns a nested dictionary containing all current facts for the chosen company.
The facts themselves are stored under the key that corresponds to the taxonomy of the filing (`us-gaap`, `ifrs-full` etc.) so for this purpose, there is a key-value pair included in the response with the key `taxonomy`, allowing programmatic access to the facts themselves.

The output is too long to include an example here.

### Company Concepts
```py 
client.get_company_concept(self, ticker_or_cik, taxonomy, tag)
```
This returns all disclosures for a specific concept (taxonomy and tag) of a specified company.

So:

```py 
client.get_company_concept('tsla', 'us-gaap', 'Assets')
```

Will return:

```py 
{'cik': 1318605,
 'taxonomy': 'us-gaap',
 'tag': 'Assets',
 'label': 'Assets',
 'description': 'Sum of the carrying amounts as of the balance sheet date of all assets that are recognized. Assets are probable future economic benefits obtained or controlled by an entity as a result of past transactions or events.',
 'entityName': 'Tesla, Inc.',
 'units': {'USD': [{'end': '2010-12-31',
    'val': 386082000,
    'accn': '0001193125-11-221497',
    'fy': 2011,
    'fp': 'Q2',
    'form': '10-Q',
    'filed': '2011-08-12'},
   {'end': '2010-12-31',
    'val': 386082000,
    'accn': '0001193125-11-308489',
    'fy': 2011,
    'fp': 'Q3',
    'form': '10-Q',
    'filed': '2011-11-14'},
   {'end': '2010-12-31',
    'val': 386082000,
    'accn': '0001193125-12-081990',
    'fy': 2011,
    'fp': 'FY',
    'form': '10-K',
    'filed': '2012-02-27'},
    ...
    ...
   ]
  },
 'response': 200
}
```
### Frames
```py 
client.get_frames(self, taxonomy, tag, currency, year=None, quarter=None, instantaneous=True)
```

This returns one fact for each reporting entity that is last filed that most closely fits the calendar period requested. 

The output is too long to include an example here.
