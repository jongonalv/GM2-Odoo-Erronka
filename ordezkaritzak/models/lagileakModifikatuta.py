

from odoo import models, fields, api



class Langilea(models.Model):
    _inherit = 'hr.employee'

    ordezkaritza = fields.Many2one('ordezkaritzak.ordezkaritza', string="Ordezkaritza")
