# Writing scrapers to fetch data of different Oil stations and petrol stations from
# Different Websites Using python Cralwers.
# Using Mongo to store the data.

from crawlers import bharatpetroleum as bp
from crawlers import hpcl as hpcl

"""
bpObj = bp.BharatPetroleumHelper()
bpObj.fetch_details()
"""

hpclObj = hpcl.HPCL()
hpclObj.fetch_details()


