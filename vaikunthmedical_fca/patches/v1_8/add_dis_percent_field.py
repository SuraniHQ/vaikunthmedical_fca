from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	create_custom_fields(
		{
			"Purchase Receipt Item": [
				{
					"fieldname": "custom_dis_percent",
					"label": "Dis %",
					"fieldtype": "Percent",
					"insert_after": "custom_scm",
					"description": "Percentage discount for this line. Works alongside Scm - both reduce Amount together; Rate is unaffected.",
				},
			]
		}
	)
