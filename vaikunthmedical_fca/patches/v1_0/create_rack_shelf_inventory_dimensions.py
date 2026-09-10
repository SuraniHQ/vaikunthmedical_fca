import frappe


def execute():
	"""Register Rack and Shelf as Inventory Dimensions so they appear as fields
	on stock transactions (Purchase Receipt, Stock Entry, Delivery Note, etc.)
	and get tracked on the Stock Ledger Entry / Bin.
	"""
	for dimension_name, reference_document in (("Rack", "Rack"), ("Shelf", "Shelf")):
		if frappe.db.exists("Inventory Dimension", dimension_name):
			continue

		frappe.get_doc(
			{
				"doctype": "Inventory Dimension",
				"dimension_name": dimension_name,
				"reference_document": reference_document,
				"apply_to_all_doctypes": 1,
				"reqd": 0,
				"validate_negative_stock": 0,
			}
		).insert(ignore_permissions=True)
