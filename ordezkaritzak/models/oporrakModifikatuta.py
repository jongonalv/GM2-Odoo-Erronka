from odoo.exceptions import ValidationError
from odoo import models, fields, api

class Oporrak(models.Model):
    _inherit = 'hr.leave'

    @api.constrains('request_date_from', 'request_date_to', 'employee_id', 'holiday_status_id')
    def _konprobatu_oporra_egunak(self):
        for leave in self:
            if leave.holiday_status_id.display_name.lower() != 'oporrak':
                continue

            # 14 baino gehiagoko oporrak ezin dira
            if leave.request_date_from and leave.request_date_to:
                iraupena_oporrak = (leave.request_date_to - leave.request_date_from).days + 1
                if iraupena_oporrak > 14: 
                    raise ValidationError("Ezin dira eskatu 2 aste baino gehiagoko oporrak.")

            # Departamentua lortu
            department = leave.employee_id.department_id
            if not department:
                continue

            # Konprobatu ea oporrak solapatzen diren
            overlapping_leaves = self.search([
                ('id', '!=', leave.id),
                ('employee_id.department_id', '=', department.id),
                ('request_date_from', '<=', leave.request_date_to),
                ('request_date_to', '>=', leave.request_date_from),
                ('state', 'in', ['confirm', 'validate']),
            ])

            if overlapping_leaves:
                raise ValidationError("Beste langile bat dago departamento berean oporretan egun horietan.")
