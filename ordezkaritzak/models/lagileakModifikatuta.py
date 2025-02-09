

from odoo import models, fields, api



class Langilea(models.Model):
    _inherit = 'hr.employee'

    ordezkaritza = fields.Many2one('ordezkaritzak.ordezkaritza', string="Ordezkaritza")

class AccountMove(models.Model):
    _inherit = 'account.move'

    ordezkaritza = fields.Many2one('ordezkaritzak.ordezkaritza', string="Ordezkaritza")