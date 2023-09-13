# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductCategory(models.Model):
    _name = "product.category"
    _inherit = 'product.category'

    image = fields.Binary("Image")


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    home_booking = fields.Boolean('Home booking', default=False)
    local_reservation = fields.Boolean('Local reservation', default=False)
    time = fields.Float(string='Time')
    appointment_id = fields.Many2one('hms.appointment')


