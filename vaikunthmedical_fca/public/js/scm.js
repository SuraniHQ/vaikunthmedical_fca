function vmfca_apply_scm(frm, cdt, cdn) {
	const row = locals[cdt][cdn];
	const qty = flt(row.qty) || 1;
	const price_list_rate = flt(row.price_list_rate) || flt(row.rate);

	frappe.model.set_value(cdt, cdn, "rate", price_list_rate - flt(row.custom_scm_amount) / qty);
}

["Purchase Receipt", "Purchase Invoice"].forEach((parent_doctype) => {
	frappe.ui.form.on(`${parent_doctype} Item`, {
		custom_scm_amount: vmfca_apply_scm,
	});
});
