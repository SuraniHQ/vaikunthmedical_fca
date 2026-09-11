import frappe
from frappe.utils import flt


def sync_batch_expiry_and_selling_price(doc, method=None):
	"""On GRN submission: push each row's Expiry Date onto the batch(es) it
	received, and roll the row's MRP (entered per Purchase UOM) into the
	default Selling Price List, converted to Stock UOM.
	"""
	for row in doc.items:
		if row.custom_expiry_date:
			for batch_no in _get_row_batch_nos(row):
				_set_batch_expiry(batch_no, row.custom_expiry_date)

		if row.custom_mrp:
			_update_selling_price(row)


def _get_row_batch_nos(row):
	if row.batch_no:
		return [row.batch_no]

	if row.serial_and_batch_bundle:
		return frappe.get_all(
			"Serial and Batch Entry",
			filters={"parent": row.serial_and_batch_bundle},
			pluck="batch_no",
			distinct=True,
		)

	return []


def _set_batch_expiry(batch_no, expiry_date):
	if batch_no and frappe.db.exists("Batch", batch_no):
		frappe.db.set_value("Batch", batch_no, "expiry_date", expiry_date)


def _update_selling_price(row):
	price_list = frappe.db.get_single_value("Selling Settings", "selling_price_list")
	if not price_list:
		return

	rate_in_stock_uom = flt(row.custom_mrp) / flt(row.conversion_factor or 1)

	existing = frappe.db.get_value(
		"Item Price",
		{
			"item_code": row.item_code,
			"price_list": price_list,
			"uom": row.stock_uom,
			"selling": 1,
		},
		"name",
	)

	if existing:
		frappe.db.set_value("Item Price", existing, "price_list_rate", rate_in_stock_uom)
	else:
		frappe.get_doc(
			{
				"doctype": "Item Price",
				"item_code": row.item_code,
				"price_list": price_list,
				"uom": row.stock_uom,
				"selling": 1,
				"price_list_rate": rate_in_stock_uom,
			}
		).insert(ignore_permissions=True)
