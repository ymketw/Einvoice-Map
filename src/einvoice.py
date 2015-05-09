import string
import time, datetime, calendar
import random
import math
import itertools

import base64
import hmac
import hashlib
import urllib.request

import  json

from invoice import Invoice

def uniqid(prefix='', more_entropy=False):
	m = time.time()
	uniqid = '%8x%05x' %(math.floor(m),(m-math.floor(m))*1000000)
	if more_entropy:
		valid_chars = list(set(string.hexdigits.lower()))
		entropy_string = ''
		for i in range(0,10,1):
			entropy_string += random.choice(valid_chars)
		uniqid = uniqid + entropy_string
	uniqid = prefix + uniqid
	return uniqid

def dict_sort(d):
	return [(k,d[k]) for k in sorted(d.keys())]

def get_param_list(param_dict):
	param_list = ""
	for key, value in param_dict:
		param_list += key + "=" + value + "&"
	param_list = param_list[:len(param_list)-1]
	return param_list

def url_parameter(api_key, param_dict):
	param_dict = dict_sort(param_dict)
	param_list = get_param_list(param_dict)
	signature = hmac.new(api_key.encode('utf-8'), param_list.encode('utf-8'), hashlib.sha1).digest()
	signature = base64.b64encode(signature)
	return(param_list, signature)


def carrier_query(api_key, app_id, card_type, card_no, card_encrypt):
	data = {}
	while "code" not in data or data["code"] != 200:
		param_dict = {}
		param_dict["version"] = "1.0"
		param_dict["serial"] = "0000000001"
		param_dict["action"] = "qryCarrierAgg"
		param_dict["cardType"] = card_type
		param_dict["cardNo"] = card_no
		param_dict["cardEncrypt"] = card_encrypt
		param_dict["appID"] = app_id
		param_dict["timeStamp"] = str(int(time.time())+10)
		param_dict["uuid"] = uniqid()

		(param_list, signature) = url_parameter(api_key, param_dict)
		carrier_query_url = 'https://www.einvoice.nat.gov.tw/PB2CAPIVAN/Carrier/Aggregate?' + param_list + '&signature=' + signature.decode()
		#print(carrier_query_url)

		with urllib.request.urlopen(carrier_query_url) as url:
			data = json.loads(url.read().decode())

	for carrier_property in data["carriers"]:
		print(carrier_property)

	return data

def invoice_header_query(api_key, app_id, card_type, card_no, card_encrypt):
	invoice_list = []
	now = datetime.datetime.now()
	for year in range(now.year-5, now.year+1):
		for month in range(1, 13):
			if year >= now.year and month > now.month:
				break
			start_date = "{0:0=4d}".format(year) + "/" + "{0:0=2d}".format(month) + "/" + "01"
			end_date = "{0:0=4d}".format(year) + "/" + "{0:0=2d}".format(month) + "/" + "{0:0=2d}".format(calendar.monthrange(year, month)[1])
			
			data = {}
			while "code" not in data or data["code"] != 200:
				param_dict = {}
				param_dict["version"] = "0.2"
				param_dict["action"] = "carrierInvChk"
				param_dict["cardType"] = card_type
				param_dict["cardNo"] = card_no
				param_dict["cardEncrypt"] = card_encrypt
				param_dict["appID"] = app_id
				param_dict["timeStamp"] = str(int(time.time())+10)
				param_dict["expTimeStamp"] = str(int(time.time())+1000)
				param_dict["startDate"] = start_date
				param_dict["endDate"] =  end_date				
				param_dict["onlyWinningInv"] = "N"
				param_dict["uuid"] = uniqid()
				
				(param_list, signature) = url_parameter(api_key, param_dict)
				invoice_header_url = 'https://www.einvoice.nat.gov.tw/PB2CAPIVAN/invServ/InvServ?' + param_list + '&signature=' + signature.decode()
				with urllib.request.urlopen(invoice_header_url) as url:
					data = json.loads(url.read().decode())

				if data["code"] == 903:
					break

				for inv in data["details"]:
					if "sellerName" in inv:
						invoice_list.append(Invoice(inv))
	return invoice_list

def invoice_item_query(api_key, app_id, card_type, card_no, card_encrypt, invoice_list):
	for inv, i in zip(invoice_list, itertools.count()):
		data = {}
		while "code" not in data or data["code"] != 200:
			param_dict = {}
			param_dict["version"] = "0.1"
			param_dict["action"] = "carrierInvDetail"
			param_dict["cardType"] = card_type
			param_dict["cardNo"] = card_no
			param_dict["cardEncrypt"] = card_encrypt
			param_dict["appID"] = app_id
			param_dict["timeStamp"] = str(int(time.time())+10)
			param_dict["expTimeStamp"] = str(int(time.time())+1000)
			param_dict["uuid"] = uniqid()
			param_dict["invNum"] = inv.inv_num
			param_dict["invDate"] = "{0:0=4d}/{1:0=2d}/{2:0=2d}".format((inv.inv_date.year+1911), inv.inv_date.month, inv.inv_date.day)
			param_dict["sellerName"] = urllib.parse.quote(inv.seller_name)
			param_dict["amount"] = str(inv.amount)

			(param_list, signature) = url_parameter(api_key, param_dict)
			invoice_item_url = 'https://www.einvoice.nat.gov.tw/PB2CAPIVAN/invServ/InvServ?' + param_list + '&signature=' + signature.decode()
			with urllib.request.urlopen( invoice_item_url ) as url:
				data = json.loads(url.read().decode())

			for item in data["details"]:
				invoice_list[i].add_item(item) 
	return invoice_list

def get_einvoice(api_key, app_id, card_type, card_no, card_encrypt):
	invoice_list = invoice_header_query(api_key, app_id, card_type, card_no, card_encrypt)
	invoice_list = invoice_item_query(api_key, app_id, card_type, card_no, card_encrypt, invoice_list)

	return invoice_list

if __name__ == '__main__':

	#TEST
	api_key = "QWQ4dU9WMzRXa2xoYUdsZA=="
	app_id = "EINV0201505042102"
	card_type = "3J0002"
	card_no = "/SMV1EFQ"
	card_encrypt = "1212"

	invoice_list = get_einvoice(api_key, app_id, card_type, card_no, card_encrypt)
	for inv in invoice_list:
		inv._print()
		print()
