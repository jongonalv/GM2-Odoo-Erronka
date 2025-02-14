from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    """
        Produktuak modeloa
        Hemen produktuen modeloa redefinitzen da kampo batzuk derrigorerzkoak izateko eta balidazioak gehitzen dira.
    """
    _inherit = 'product.template'

    description = fields.Text(string="Description", required=True)
    categ_id = fields.Many2one('product.category', string="Category", required=True)
    list_price = fields.Float(string="Sales Price", required=True)

    @api.constrains('list_price')
    def _check_positive_price(self):
        for record in self:
            if record.list_price <= 0:
                raise ValidationError("Salmenta prezioa positiboa izan behar da.")

    @api.constrains('name')
    def _check_unique_product_name(self):
        for record in self:
            existing_records = self.search([
                ('name', '=', record.name),
                ('id', '!=', record.id)
            ])
            if existing_records:
                raise ValidationError("Ezinezkoa da izen bereko produkturik egotea.")