
import einvoice
from trips.invoice import Invoice


class User(object):
	def __init__(self, api_key, app_id, card_type, card_no, card_encrypt):
		self.api_key = api_key
		self.app_id = app_id
		self.card_type = card_type
		self.card_no = card_no
		self.card_encrypt = card_encrypt
		self.invoice_list = einvoice.get_einvoice(api_key, app_id, card_type, card_no, card_encrypt)

		#key is the ID of store
		self.visit_freqency = {}
		self.top_item = {}
		self.consumption = {}

#if __name__ == '__main__':
def login(account, password):
	#TEST
	api_key = "QWQ4dU9WMzRXa2xoYUdsZA=="
	app_id = "EINV0201505042102"
	card_type = "3J0002"
	card_no = account
	card_encrypt = password
	user = User(api_key, app_id, card_type, card_no, card_encrypt)
	#for inv in user.invoice_list:
	#	inv._print()
	#	print()