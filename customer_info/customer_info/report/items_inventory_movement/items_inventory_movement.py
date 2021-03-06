# Copyright (c) 2013, indictrans and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import date_diff
from datetime import datetime, timedelta,date
from frappe.utils import flt, get_datetime, get_time, getdate

def execute(filters=None):
	columns, data = [], []
	columns = get_colums()
	data = get_data(filters)
	return columns, data

def get_data(filters):
	#now_date = datetime.now().date()
	result = frappe.db.sql("""select
			item.default_warehouse,
			item.default_supplier,
			item.invoice_number,
			item.product_category,item.brand,
			item.serial_number,item.imei_number,
			format(item.purchase_price_with_vat,2) as Basic_calculation_price,
			format(item.wholesale_price,2) as Purchase_price_with_VAT,
			format(item.wholesale_price/((item.vat_rate)/100+1),2) as Purchase_price_without_VAT,
			item.purchase_date,item.sold_date,
			case when agreement.merchandise_status = "Early buy" then
			concat(agreement.early_buy_discount_percentage,"% ",item.merchandise_status) else item.merchandise_status end as merchandise_status,
			agreement.name,
			agreement.customer,
			(select replace(replace(replace(content,"<p></p>",""),"<p>",""),"</p>","") as content from `tabCommunication` where reference_doctype = "Item" 
				 and reference_name = item.name order by creation desc limit 1) as Last_Comment
			FROM `tabItem` item left join `tabCustomer Agreement` agreement on 
			item.name = agreement.product
			WHERE 1=1
			{0}""" .format(get_condtion(filters.get("sold_from_date"),filters.get("sold_to_date"),filters.get("purchase_from_date"),filters.get("purchase_to_date"))),as_list=1)
	return result

def get_condtion(sold_from_date,sold_to_date,purchase_from_date,purchase_to_date):
	

	cond = ""
	if  sold_from_date and sold_to_date and purchase_from_date and purchase_to_date:
		cond = "and item.sold_date BETWEEN '{0}' AND '{1}' and item.purchase_date BETWEEN '{2}' AND '{3}' ".format(sold_from_date,sold_to_date,purchase_from_date,purchase_to_date)

	elif sold_from_date and sold_to_date:
		cond = "and item.sold_date BETWEEN '{0}' AND '{1}' ".format(sold_from_date,sold_to_date)

	elif purchase_from_date and purchase_to_date:
		cond = "and item.purchase_date BETWEEN '{0}' AND '{1}' ".format(purchase_from_date,purchase_to_date)
	
	elif sold_from_date:	
		cond = "and  item.sold_date >= '{0}' ".format(sold_from_date)
	
	elif purchase_from_date:	
		cond = "and  item.purchase_date >= '{0}' ".format(purchase_from_date)

	elif sold_to_date:
		cond = "and item.sold_date < '{0}' ".format(sold_to_date)

	elif purchase_to_date:
		cond = "and item.purchase_date < '{0}' ".format(purchase_to_date)	

	return cond	


def get_colums():
	columns = [
				("Warehouse") + ":Link/Warehouse:100",
				("Supplier") + ":Link/Supplier:100",
				("Invoice number") + "::170",
				("Product Category") + ":Link/Product Category:90",
				("Product Model") + ":Link/Brand:90",
				("Serial number") + "::90",
				("IMEI number") + "::90",
				("Basic calculation price") + "::120",
				("Purchase price with VAT") + ":Data:90",
				("Purchase price without VAT") + ":Data:90",
				("Purchase Date") + ":Date:100",
				("Merchandise transfer date") + ":Date:80",
				("Merchandise status") + "::90",
				("Customer Agreement") + ":Link/Customer Agreement:90",
				("Customer") + ":Link/Customer:90",
				("Last Comment") + ":Data:150"
			]	
	return columns