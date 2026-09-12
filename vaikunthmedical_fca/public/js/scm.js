function vmfca_apply_scm(frm, cdt, cdn) {
	const row = locals[cdt][cdn];
	const base_amount = flt(row.qty) * flt(row.rate);
	frappe.model.set_value(cdt, cdn, "amount", base_amount - flt(row.custom_scm_amount));
}

["Purchase Receipt", "Purchase Invoice"].forEach((parent_doctype) => {
	frappe.ui.form.on(`${parent_doctype} Item`, {
		custom_scm_amount: vmfca_apply_scm,
	});
});
