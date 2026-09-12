frappe.ui.form.on("Purchase Receipt", {
	refresh(frm) {
		(frm.doc.items || []).forEach((row) => {
			if (row._previous_scm === undefined) {
				row._previous_scm = flt(row.custom_scm);
			}
		});
	},
});

frappe.ui.form.on("Purchase Receipt Item", {
	items_add(frm, cdt, cdn) {
		locals[cdt][cdn]._previous_scm = 0;
	},
	custom_scm(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		const previous = row._previous_scm || 0;
		const delta = flt(row.custom_scm) - previous;

		if (delta) {
			const qty = flt(row.qty) || 1;
			frappe.model.set_value(cdt, cdn, "rate", flt(row.rate) - delta / qty);
		}

		row._previous_scm = flt(row.custom_scm);
	},
});
