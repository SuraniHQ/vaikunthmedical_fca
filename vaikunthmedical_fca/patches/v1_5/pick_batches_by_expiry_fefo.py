import frappe


def execute():
	"""Sell the batch closest to expiring first (FEFO), not just the oldest-
	received one (FIFO) - pairs with the batch-wise Item Price so POS/Sales
	auto-picks a batch and its price together (see get_item_details.py).
	"""
	stock_settings = frappe.get_single("Stock Settings")
	stock_settings.auto_create_serial_and_batch_bundle_for_outward = 1
	stock_settings.pick_serial_and_batch_based_on = "Expiry"
	stock_settings.save(ignore_permissions=True)
