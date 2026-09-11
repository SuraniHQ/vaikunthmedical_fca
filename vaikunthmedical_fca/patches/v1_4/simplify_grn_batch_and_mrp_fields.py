import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	# Batch No as a plain text field instead of a Link search dropdown - the
	# supplier's batch number is just typed in, and our own validate hook
	# (ensure_batch_with_expiry) creates the Batch record from that text.
	for property, value, property_type in (
		("fieldtype", "Data", "Select"),
		("options", "", "Text"),
	):
		if not frappe.db.exists(
			"Property Setter",
			{"doc_type": "Purchase Receipt Item", "field_name": "batch_no", "property": property},
		):
			frappe.make_property_setter(
				{
					"doctype": "Purchase Receipt Item",
					"fieldname": "batch_no",
					"property": property,
					"value": value,
					"property_type": property_type,
				}
			)

	# Move MRP next to Rate instead of under Batch No / Expiry Date.
	create_custom_fields(
		{
			"Purchase Receipt Item": [
				{
					"fieldname": "custom_mrp",
					"label": "MRP (Purchase UOM)",
					"fieldtype": "Currency",
					"options": "currency",
					"insert_after": "rate",
					"description": (
						"MRP for one Purchase UOM. On submit this is converted to the Stock UOM "
						"rate and pushed to the default Selling Price List."
					),
				},
			]
		}
	)
