from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ContractTemplate(models.Model):
    _inherit = 'hr.contract'

    # Langile berdinak ezin ditu bi kontratu aldi berean izan
    @api.constrains('date_start', 'date_end', 'employee_id')
    def _konprobatu_kontratu_gainjartzea(self):
        for contract in self:
            contract_end = contract.date_end if contract.date_end else fields.Date.today()

            overlapping_contracts = self.env['hr.contract'].search([
                ('id', '!=', contract.id),
                ('employee_id', '=', contract.employee_id.id),
                '|',
                '&', ('date_start', '<=', contract_end), 
                     ('date_end', '>=', contract.date_start),
                '&', ('date_start', '<=', contract.date_start), 
                     ('date_end', '=', False) 
            ])

            if overlapping_contracts:
                raise ValidationError("Ezin da kontratu bat baino gehiago izan aldi berean.")
