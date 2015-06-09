import csv

class Seller(object):
	def __init__(self, _id, store_name, address, longitude, latitude):
		self.id = int(_id)
		self.store_name = store_name if store_name.find("-") == -1 else store_name[:store_name.find("-")]
		self.branch_name = "" if store_name.find("-") == -1 else store_name[store_name.find("-")+1:]
		self.address = address
		self.longitude = longitude
		self.latitude = latitude

		#for user
		self.visit_frequency = 0
		self.consumption = 0.0
		self.top_item = ''

	def set_branch_name(self, n):
		self.branch_name = n

	def set_visit_frequency(self, f):
		self.visit_frequency = f

	def set_consumption(self, c):
		self.consumption = c
		
	def set_top_item(self, i):
		self.top_item = i

	def _print(self):
		print(self.id, self.store_name, self.branch_name, self.address, self.longitude, self.latitude, self.visit_frequency, self.consumption, self.top_item)

def list_sellers(csv_file):
	#key is the ID
	sellers = {}
	with open(csv_file, 'r', errors='ignore') as f:
		for row in csv.reader(f):
			row = [s.replace("\n", "") for s in row]
			sellers[int(row[0])] = Seller(*row)
	return sellers
		
if __name__ == '__main__':
	#TEST
	all_sellers1 = list_sellers("../Taipei_shops_with_einvoice.csv")
	#all_sellers2 = list_sellers("../Taipei_shops_with_einvoice.csv")
	#for key in sellers:
	for i in range(1, 2000):
		sellers[i]._print()