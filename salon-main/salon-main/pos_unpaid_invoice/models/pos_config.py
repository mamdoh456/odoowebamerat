from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    def _get_unpaid_invoice_product_id(self):
        return self.env.ref("pos_unpaid_invoice.product_product_unpaid_invoice", raise_if_not_found=False)

    unpaid_invoice_product_id = fields.Many2one('product.product', string='Inpaid Invoice Product',default=_get_unpaid_invoice_product_id)