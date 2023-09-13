from odoo import fields, models, api, _, tools


class web_gift_coupon(models.Model):
    _inherit = 'web.gift.coupon'


    order_ids = fields.One2many('pos.order', 'coupon_id')