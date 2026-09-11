import frappe


def execute():
	"""Default GRN item rows to the plain Batch No field instead of the
	"Add Serial / Batch No" popup, so a supplier's batch number can just be
	typed straight into the row.
	"""
	if not frappe.db.exists(
		"Property Setter",
		{"doc_type": "Purchase Receipt Item", "field_name": "use_serial_batch_fields", "property": "default"},
	):
		frappe.make_property_setter(
			{
				"doctype": "Purchase Receipt Item",
				"fieldname": "use_serial_batch_fields",
				"property": "default",
				"value": "1",
				"property_type": "Check",
			}
		)
