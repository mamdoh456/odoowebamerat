from odoo import models, fields, api,_


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_send_birthday_email(self):
        for rec in self:
            template_id = self.env.ref('res_partner_email_birthday.birthday_email_template')
            # Send the email using the template
            self.env['mail.template'].browse(template_id.id).send_mail(rec.id)


    def action_send_gift_card(self):
        action = self.env['ir.actions.act_window']._for_xml_id(
            'res_partner_email_birthday.action_birthday_gift_card_wizard_form')
        action['context'] = {'res_partner_id': self.id,}
        return action

