from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	create_custom_fields(
		{
			"Purchase Receipt Item": [
				{
					"fieldname": "custom_expiry_month_year",
					"label": "Expiry (MM-YY)",
					"fieldtype": "Data",
					"insert_after": "batch_no",
					"description": "Enter as MM-YY, e.g. 12-26 for December 2026 - the last day of that month is used as the Expiry Date below.",
				},
				{
					"fieldname": "custom_expiry_date",
					"label": "Expiry Date",
					"fieldtype": "Date",
					"insert_after": "custom_expiry_month_year",
				},
			]
		}
	)
