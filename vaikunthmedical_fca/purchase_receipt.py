import frappe
from frappe.utils import flt


def ensure_batch_with_expiry(doc, method=None):
	"""Create the Batch for a freshly typed supplier batch number ourselves,
	before core tries to auto-create it. Core's own auto-create only sets
	batch_id + item (no expiry), which hard-fails for items that don't have
	a Shelf Life set. Creating it here with the row's Expiry Date avoids that,
	and runs early enough (doc_events "validate") to land before core's own
	link validation touches the field.
	"""
	for row in doc.items:
		if row.batch_no and not frappe.db.exists("Batch", row.batch_no):
			batch = frappe.new_doc("Batch")
			batch.batch_id = row.batch_no
			batch.item = row.item_code
			if row.custom_expiry_date:
				batch.expiry_date = row.custom_expiry_date
			batch.insert(ignore_permissions=True)


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
