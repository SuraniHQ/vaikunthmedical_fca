function vmfca_init_scm_tracking(frm) {
	(frm.doc.items || []).forEach((row) => {
		if (row._previous_scm === undefined) {
			row._previous_scm = flt(row.custom_scm_amount);
		}
	});
}

function vmfca_apply_scm(frm, cdt, cdn) {
	const row = locals[cdt][cdn];
	const previous = row._previous_scm || 0;
	const delta = flt(row.custom_scm_amount) - previous;

	if (delta) {
		const qty = flt(row.qty) || 1;
		frappe.model.set_value(cdt, cdn, "rate", flt(row.rate) - delta / qty);
	}

	row._previous_scm = flt(row.custom_scm_amount);
}

["Purchase Receipt", "Purchase Invoice"].forEach((parent_doctype) => {
	frappe.ui.form.on(parent_doctype, {
		refresh: vmfca_init_scm_tracking,
	});

	frappe.ui.form.on(`${parent_doctype} Item`, {
		items_add(frm, cdt, cdn) {
			locals[cdt][cdn]._previous_scm = 0;
		},
		custom_scm_amount: vmfca_apply_scm,
	});
});
