from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	create_custom_fields(
		{
			"Purchase Receipt Item": [
				{
					"fieldname": "custom_expiry_date",
					"label": "Expiry Date",
					"fieldtype": "Date",
					"insert_after": "batch_no",
				},
				{
					"fieldname": "custom_mrp",
					"label": "MRP (Purchase UOM)",
					"fieldtype": "Currency",
					"options": "currency",
					"insert_after": "custom_expiry_date",
					"description": (
						"MRP for one Purchase UOM. On submit this is converted to the Stock UOM "
						"rate and pushed to the default Selling Price List."
					),
				},
			]
		}
	)
