from odoo.exceptions import ValidationError
from odoo import models, fields, api

# Ausenzen modulua editatzen dugu ("hr.leave") oporren kudeaketa egiteko
class Oporrak(models.Model):
    _inherit = 'hr.leave'

    # Oporren baldintzak egiaztatzen ditu
    @api.constrains('request_date_from', 'request_date_to', 'employee_id', 'holiday_status_id')
    def _konprobatu_oporra_egunak(self):
        for leave in self:
            if leave.holiday_status_id.display_name.lower() != 'oporrak':
                continue

            self._konprobatu_oporren_iraupena(leave)
            self._departamentuen_gainjartzea(leave)

    # Oporrek gehienez 14 egun jarraian eta 30 egun urtean izan ditzakete
    def _konprobatu_oporren_iraupena(self, leave):
        if leave.number_of_days_display > 14:
            raise ValidationError("Ezin dira eskatu 2 aste baino gehiagoko oporrak.")

        urte_hasiera = fields.Date.to_date(f"{leave.request_date_from.year}-01-01")
        urte_bukaera = fields.Date.to_date(f"{leave.request_date_from.year}-12-31")

        zenbat_egun_oporrak = sum(self.search([
            ('id', '!=', leave.id),
            ('employee_id', '=', leave.employee_id.id),
            ('holiday_status_id.name', '=', 'oporrak'),
            ('request_date_from', '>=', urte_hasiera),
            ('request_date_to', '<=', urte_bukaera),
            ('state', 'in', ['confirm', 'validate']),
        ]).mapped('number_of_days_display')) + leave.number_of_days_display

        if zenbat_egun_oporrak > 30:
            raise ValidationError("30 egun baino gehiagoko oporrak ezin dira hartu.")

    # Departamentuko beste langile batekin opor-egunak gainjartzen direla egiaztatzen du
    def _departamentuen_gainjartzea(self, leave):
        department = leave.employee_id.department_id
        if not department:
            return

        overlapping_leaves = self.search([
            ('id', '!=', leave.id),
            ('employee_id.department_id', '=', department.id),
            ('holiday_status_id.name', '=', 'oporrak'),
            ('request_date_from', '<=', leave.request_date_to),
            ('request_date_to', '>=', leave.request_date_from),
            ('state', 'in', ['confirm', 'validate']),
        ])

        if overlapping_leaves:
            raise ValidationError("Beste langile bat dago departamento berean oporretan egun horietan.")
