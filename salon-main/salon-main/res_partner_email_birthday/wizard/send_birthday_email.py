from odoo import models, fields
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class BirthdayGiftCardWizard(models.TransientModel):
    _name = 'birthday.gift.card.wizard'

    product = fields.Many2one('product.product', string='Product',domain="[('mimetype', 'not in', ('application/javascript','text/css'))]")

    def _prepare_gift_card_vals(self,product_id,partner_id):
        expiry_checked = False
        exp_dat_show = False
        coupon_obj = self.env['web.gift.coupon']
        d = datetime.now()
        issue_date = datetime.combine(d, datetime.min.time())
        if product_id.validity_type == 'month':
            value = product_id.card_validity
            expiry_checked = issue_date + relativedelta(months=int(value))
        elif product_id.validity_type == 'year':
            value = product_id.card_validity
            expiry_checked = issue_date + relativedelta(years=int(value))
        else:
            expiry_checked = False

        if expiry_checked:
            exp_dat_show = True
        return {
            'name': product_id.name + ' ' + str(datetime.now()),
            'coupon_apply_times': 1,
            'product_id': product_id.id,
            'issue_date': issue_date,
            'amount': product_id.list_price,
            'amount_type': 'fix',
            'exp_dat_show': exp_dat_show,
            'expiry_date': expiry_checked,
            'partner_id': partner_id,
            'partner_true': True,
            'max_amount': product_id.list_price,
            'active': True,
            'user_id': self.env.user.id,
        }
    def action_send_gift_card(self):
        partner_id = self._context.get('res_partner_id',False)
        coupon_obj = self.env['web.gift.coupon']
        product_id = self.product
        gift_card_vals = self._prepare_gift_card_vals(self.product,partner_id)
        template = None
        if product_id.template_id:
            template = product_id.template_id.id

        if product_id.gift_card_type == 'ecard':
            coupon_id = coupon_obj.sudo().with_context(giftcard=True, template=template).create(gift_card_vals)
            auther = coupon_id.partner_id
            if template:
                template_id = self.env['mail.template'].browse(int(template))
                template_id.sudo().with_context(auther=auther).send_mail(coupon_id.id, force_send=True)
            else:
                template_id = self.env.ref('bi_website_gift_cards.email_template_edi_giftcard')
                template_id.sudo().with_context(auther=auther).send_mail(coupon_id.id, force_send=True)
        return {'type': 'ir.actions.act_window_close'}
