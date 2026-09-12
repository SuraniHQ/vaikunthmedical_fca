function vmfca_recompute_amount(frm, cdt, cdn) {
	const row = locals[cdt][cdn];
	const base_amount = flt(row.qty) * flt(row.rate);
	const discount_value = (base_amount * flt(row.discount_percentage)) / 100.0;

	frappe.model.set_value(cdt, cdn, "amount", base_amount - discount_value - flt(row.custom_scm_amount));
}

["Purchase Receipt", "Purchase Invoice"].forEach((parent_doctype) => {
	frappe.ui.form.on(`${parent_doctype} Item`, {
		custom_scm_amount: vmfca_recompute_amount,
		discount_percentage: vmfca_recompute_amount,
	});
});
