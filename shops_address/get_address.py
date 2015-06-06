import requests

def get_url_content(url):
	r = requests.get(url)
	if r.status_code != requests.codes.ok:
		raise ValueError("can not connect to target url")
	return r.content

def get_shops_address(url):
	global shop_list
	global branch_name_list
	global address_list
	html = get_url_content(url)
	html = html.split()
	for string in html:
		if string.find('class="name"') != -1:
			first_b = string.find('<b>')
			first_br = string.find('<br>')
			first_dashb = string.find('</b>')
			store_name = string[first_b+3:first_br]
			branch_name = string[first_br+4:first_dashb]
			store_name_list.append(store_name)
			branch_name_list.append(branch_name)

		if string.find('class="add"') != -1:
			first_b = string.find('<b>')
			first_dashb = string.find('</b>')
			address = string[first_b+3:first_dashb]
			address_list.append(address)


if __name__ == '__main__':
	store_name_list = []
	branch_name_list = []
	address_list = []

	get_shops_address("http://twcoupon.com/brandshop-7_11-%E9%9B%BB%E8%A9%B1-%E5%9C%B0%E5%9D%80.html")
	get_shops_address("http://twcoupon.com/brandshop-%E8%90%8A%E7%88%BE%E5%AF%8C%E4%BE%BF%E5%88%A9%E5%95%86%E5%BA%97-%E9%9B%BB%E8%A9%B1-%E5%9C%B0%E5%9D%80.html")
	get_shops_address("http://twcoupon.com/brandshop-OK%E4%BE%BF%E5%88%A9%E5%95%86%E5%BA%97-%E9%9B%BB%E8%A9%B1-%E5%9C%B0%E5%9D%80.html")
	get_shops_address("http://twcoupon.com/brandshop-%E5%85%A8%E5%AE%B6%E4%BE%BF%E5%88%A9%E5%95%86%E5%BA%97-%E9%9B%BB%E8%A9%B1-%E5%9C%B0%E5%9D%80.html")
	get_shops_address("http://twcoupon.com/brandshop-%E5%85%A8%E8%81%AF%E7%A6%8F%E5%88%A9%E4%B8%AD%E5%BF%83-%E9%9B%BB%E8%A9%B1-%E5%9C%B0%E5%9D%80.html")
	get_shops_address("http://twcoupon.com/brandshop-Costco-%E9%9B%BB%E8%A9%B1-%E5%9C%B0%E5%9D%80.html")
	get_shops_address("http://twcoupon.com/brandshop-%E5%BA%B7%E6%98%AF%E7%BE%8E-%E9%9B%BB%E8%A9%B1-%E5%9C%B0%E5%9D%80.html")
	get_shops_address("http://twcoupon.com/brandshop-%E5%B1%88%E8%87%A3%E6%B0%8F-%E9%9B%BB%E8%A9%B1-%E5%9C%B0%E5%9D%80.html")

	f = open("shops_address", "w")
	for store_name, branch_name, address, in zip(store_name_list, branch_name_list, address_list):
		f.write("{0} {1} {2}\n".format( store_name, branch_name, address) )
	f.close()

