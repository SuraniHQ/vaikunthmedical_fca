from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	create_custom_fields(
		{
			"Purchase Receipt Item": [
				{
					"fieldname": "custom_scm_amount",
					"label": "SCM (₹)",
					"fieldtype": "Currency",
					"insert_after": "discount_percentage",
					"in_list_view": 1,
					"description": "Flat scheme discount for this line, on top of Discount %. Reduces Rate (and Amount) further; applied before tax.",
				},
			],
			"Purchase Invoice Item": [
				{
					"fieldname": "custom_scm_amount",
					"label": "SCM (₹)",
					"fieldtype": "Currency",
					"insert_after": "discount_percentage",
					"in_list_view": 1,
					"description": "Flat scheme discount for this line, on top of Discount %. Reduces Rate (and Amount) further; applied before tax.",
				},
			],
			"Purchase Receipt": [
				{
					"fieldname": "custom_total_scm_amount",
					"label": "Total SCM (₹)",
					"fieldtype": "Currency",
					"read_only": 1,
					"insert_after": "discount_amount",
					"description": "Sum of SCM across all item rows.",
				},
			],
			"Purchase Invoice": [
				{
					"fieldname": "custom_total_scm_amount",
					"label": "Total SCM (₹)",
					"fieldtype": "Currency",
					"read_only": 1,
					"insert_after": "discount_amount",
					"description": "Sum of SCM across all item rows.",
				},
			],
		}
	)
