import sys
import einvoice
from seller import list_sellers

try:
	from trips.invoice import Invoice
except:
	from invoice import Invoice 
	import pickle

if sys.version_info >= (2, 7, 9):
	import ssl
	ssl._create_default_https_context = ssl._create_unverified_context

class User(object):
	def __init__(self, api_key, app_id, card_type, card_no, card_encrypt):
		self.api_key = api_key
		self.app_id = app_id
		self.card_type = card_type
		self.card_no = card_no
		self.card_encrypt = card_encrypt
		if not TEST:
			self.invoice_list = einvoice.get_einvoice(api_key, app_id, card_type, card_no, card_encrypt)
		else:
			with open('invoice_list_tmp.pkl', 'rb') as f:
				self.invoice_list = pickle.load(f)

		#key is the ID of store
		self.visit_freqency = {}
		self.top_item = {}
		self.consumption = {}

	def 

#if __name__ == '__main__':
def login(account, password):
	#TEST
	api_key = "QWQ4dU9WMzRXa2xoYUdsZA=="
	app_id = "EINV0201505042102"
	card_type = "3J0002"
	card_no = account
	card_encrypt = password
	user = User(api_key, app_id, card_type, card_no, card_encrypt)
	all_sellers1 = list_sellers("../Taipei_shops_with_einvoice.csv")

if __name__ == '__main__':
	TEST = True
	api_key = "QWQ4dU9WMzRXa2xoYUdsZA=="
	app_id = "EINV0201505042102"
	card_type = "3J0002"
	card_no = '/SMV1EFQ'
	card_encrypt = '1212'
	user = User(api_key, app_id, card_type, card_no, card_encrypt)
	all_sellers1 = list_sellers("../Taipei_shops_with_einvoice.csv")	

	for inv in user.invoice_list:
		inv._print()