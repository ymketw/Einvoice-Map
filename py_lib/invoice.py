
class Invoice(object):
	def __init__(self, details):
		self.inv_num = details["invNum"]
		self.card_type = details["cardType"]
		self.card_no = details["cardNo"]
		self.seller_name = details["sellerName"]
		self.amount = details["amount"]
		self.inv_date = InvDate(details["invDate"])
		self.inv_period = details["invPeriod"]
		self.inv_status = details["invStatus"]
		self.inv_donatable = details["invDonatable"]
		self.donate_mark = details["donateMark"]
		self.item = []

	def add_item(self, _item):
		self.item.append(Item(_item))

	def _print(self):
		print("invoice number:", self.inv_num, end=" ")
		self.inv_date._print()
		print("amount: {:>5d}".format(self.amount), end=" ")
		print("seller name:", self.seller_name)
		for i in self.item:
			i._print()

class InvDate(object):
	def __init__(self, inv_date):
		self.year = inv_date["year"]
		self.month = inv_date["month"]
		self.day = inv_date["date"]
		self.week_day = inv_date["day"]
		self.hours = inv_date["hours"]
		self.minutes = inv_date["minutes"]
		self.seconds = inv_date["seconds"]
		self.time = inv_date["time"]
		self.timezoneOffset = inv_date["timezoneOffset"]

	def _print(self):
		print("invoice date:", "{0}/{1:0=2d}/{2:0=2d}".format(self.year, self.month, self.day), end=" ")
		
class Item(object):
	def __init__(self, item):
		self.number = item["rowNum"]
		self.description = item["description"]
		self.quantity = item["quantity"]
		self.unitPrice = item["unitPrice"]
		self.amount = item["amount"]

	def _print(self):
		print("item #" + str(self.number), self.description, self.quantity, self.unitPrice, self.amount)
		