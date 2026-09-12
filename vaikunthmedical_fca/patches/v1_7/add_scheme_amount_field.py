from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	create_custom_fields(
		{
			"Purchase Receipt Item": [
				{
					"fieldname": "custom_scm",
					"label": "Scm",
					"fieldtype": "Currency",
					"options": "currency",
					"insert_after": "rate",
					"description": "Scheme/promotional discount for this line. Amount comes out as (Qty x Rate) - Scm.",
				},
			]
		}
	)
