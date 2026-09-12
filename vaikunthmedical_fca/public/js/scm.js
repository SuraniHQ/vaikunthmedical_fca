function vmfca_apply_scm(frm, cdt, cdn) {
	const row = locals[cdt][cdn];
	const qty = flt(row.qty) || 1;
	const price_list_rate = flt(row.price_list_rate) || flt(row.rate);
	const rate_after_discount = price_list_rate * (1 - flt(row.discount_percentage) / 100.0);

	frappe.model.set_value(cdt, cdn, "rate", rate_after_discount - flt(row.custom_scm_amount) / qty);
}

["Purchase Receipt", "Purchase Invoice"].forEach((parent_doctype) => {
	frappe.ui.form.on(`${parent_doctype} Item`, {
		custom_scm_amount: vmfca_apply_scm,
	});
});
