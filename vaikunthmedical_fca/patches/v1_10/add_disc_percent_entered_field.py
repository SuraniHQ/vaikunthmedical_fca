from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	fields = {
		"Purchase Receipt Item": [
			{
				"fieldname": "custom_disc_percent_entered",
				"label": "Disc % (Entered)",
				"fieldtype": "Percent",
				"insert_after": "custom_scm_amount",
				"read_only": 1,
				"description": (
					"What you typed into Discount %. ERPNext resets the native Discount % "
					"field to 0 once SCM is also used on this row (the reduction still applies "
					"correctly to Rate/Amount) - this field keeps the entered value visible."
				),
			},
		],
		"Purchase Invoice Item": [
			{
				"fieldname": "custom_disc_percent_entered",
				"label": "Disc % (Entered)",
				"fieldtype": "Percent",
				"insert_after": "custom_scm_amount",
				"read_only": 1,
				"description": (
					"What you typed into Discount %. ERPNext resets the native Discount % "
					"field to 0 once SCM is also used on this row (the reduction still applies "
					"correctly to Rate/Amount) - this field keeps the entered value visible."
				),
			},
		],
	}
	create_custom_fields(fields)
