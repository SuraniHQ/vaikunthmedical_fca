frappe.ui.form.on("Purchase Receipt Item", {
	custom_scm(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "amount", flt(row.qty) * flt(row.rate) - flt(row.custom_scm));
	},
});
