from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        partner_id = vals.get('partner_id')
        order_lines = vals.get('order_line', [])

        # Eskaerak ez badu produktu-lerro bakar bat ere, ez da bikoiztasuna egiaztatzen
        if not order_lines:
            return super(SaleOrder, self).create(vals)

        # Bezero berak egindako egungo eguneko eskaerak bilatu
        existing_orders = self.search([
            ('partner_id', '=', partner_id),
            ('date_order', '>=', fields.Date.to_string(fields.Date.today())),  # Egun berean
            ('state', '!=', 'cancel')  # Bertan behera utzitako eskaerak baztertu
        ])

        for order in existing_orders:
            # Eskaera zaharreko produktu eta kantitateen multzoa sortu
            existing_lines = {(line.product_id.id, line.product_uom_qty) for line in order.order_line}
            # Sortzen ari den eskaerako produktu eta kantitateen multzoa sortu
            new_lines = {(line[2]['product_id'], line[2]['product_uom_qty']) for line in order_lines if line[2]}

            # Bi eskaerak berdinak badira, errorea bota
            if existing_lines == new_lines:
                raise ValidationError("Bezero honek jada eskaera berdina egin du gaur.")

        return super(SaleOrder, self).create(vals)

    @api.constrains('partner_id', 'date_order', 'order_line')
    def _check_duplicate_order(self):
        for order in self:
            # Bezero berak egun berean egindako eskaerak bilatu
            existing_orders = self.search([
                ('partner_id', '=', order.partner_id.id),
                ('date_order', '>=', fields.Date.to_string(fields.Date.today())),
                ('id', '!=', order.id),  # Bere burua ez konparatzeko
                ('state', '!=', 'cancel')
            ])

            for existing_order in existing_orders:
                # Eskaera zaharreko produktu eta kantitateen multzoa sortu
                existing_lines = {(line.product_id.id, line.product_uom_qty) for line in existing_order.order_line}
                # Uneko eskaerako produktu eta kantitateen multzoa sortu
                new_lines = {(line.product_id.id, line.product_uom_qty) for line in order.order_line}

                # Bi eskaerak berdinak badira, errorea bota
                if existing_lines == new_lines:
                    raise ValidationError("Bezero honek jada eskaera berdina egin du gaur.")
