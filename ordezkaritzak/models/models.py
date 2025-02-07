# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

ordezkaritza_motak = [
        ('mota1', 'Lehen Mailaka'), 
        ('mota2', 'Bigarren Mailakoa')
    ]

class Ordezkaritza(models.Model):
    _name = 'ordezkaritzak.ordezkaritza'
    _description = 'Ordezkaritza'

    izena = fields.Char(string="Izena", required=True)
    helbidea = fields.Char(string="Helbidea", required=True)
    zuzendaria = fields.Many2one('hr.employee', string="Zuzendaria", required=True)
    nif = fields.Char(string="NIF", required=True)
    mota = fields.Selection(ordezkaritza_motak, string="Mota", required=True)
    probintzia = fields.Char(string="Probintzia", required=True)

    def write(self, vals):
        if 'zuzendaria' in vals:
            for record in self:
                if record.zuzendaria and record.zuzendaria.id != vals['zuzendaria']:
                    # Crear una entrada en OrdezkaritzaDatuak con el zuzendaria anterior

                    datuak = self.env['ordezkaritzak.datuak'].search([
                        ('ordezkaritza', '=', record.id),
                        ('zuzendaria', '=', record.zuzendaria.id)
                    ], limit=1)

                    if datuak:

                        facturas = self.env['account.move'].search([
                            ('ordezkaritza', '=', record.id),
                            ('invoice_date', '>=', datuak.hasieraData),
                            ('invoice_date', '<=', datetime.now())
                        ])

                        total_irabazitako = 0.0
                        for factura in facturas:
                            total_irabazitako += factura.amount_total

                        datuak.write({'irabaziak': total_irabazitako,
                                  'amieraData': datetime.now()})

                    self.env['ordezkaritzak.datuak'].create({
                        'ordezkaritza': record.id,
                        'zuzendaria': vals['zuzendaria'],
                        'hasieraData': datetime.now(),
                    })


        return super(Ordezkaritza, self).write(vals)

    def unlink(self):
        for record in self:
            # Crear una entrada en OrdezkaritzaHistorikoa antes de eliminar el registro
            historikoa =  self.env['ordezkaritzak.historikoa'].create({
                'ordezkaritza': record.id,
                'hasieraData': record.hasieraData,
                'amieraData': datetime.now(),
                'nif': record.nif,
                'mota': record.mota,
                'probintzia': record.probintzia,
                'hasieraData': record.hasieraData
            })

            datuak = self.env['ordezkaritzak.datuak'].search([
                        ('ordezkaritza', '=', record.id),
                        ('zuzendaria', '=', record.zuzendaria.id)
                    ], limit=1)
            
            datuak.write({'historikoa': historikoa.id})

        return super(Ordezkaritza, self).unlink()


class OrdezkaritzaHistorikoa(models.Model):
    _name = 'ordezkaritzak.historikoa'
    _description = 'Ordezkaritza Historikoa'

    ordezkaritza = fields.Many2one('ordezkaritzak.ordezkaritza', string="Ordezkaritza", required=True)
    hasieraData = fields.Date(string="Hasiera Data")
    amieraData = fields.Date(string="Amiera Data")
    nif = fields.Char(string="NIF", required=True)
    mota = fields.Selection(ordezkaritza_motak, string="Mota", required=True)
    probintzia = fields.Char(string="Probintzia", required=True)

class OrdezkaritzaDatuak(models.Model):
    _name = 'ordezkaritzak.datuak'
    _description = 'Ordezkaritza Datuak'

    ordezkaritza = fields.Many2one('ordezkaritzak.ordezkaritza', string="Ordezkaritza", required=True)
    zuzendaria = fields.Many2one('hr.employee', string="Zuzendaria", required=True)
    hasieraData = fields.Date(string="Hasiera Data")
    amieraData = fields.Date(string="Amiera Data")
    irabaziak = fields.Float(string="Irabaziak")
    historikoa = fields.Many2one('ordezkaritzak.historikoa', string="Historikoa")