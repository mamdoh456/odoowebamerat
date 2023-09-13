# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AppointmentProductLine(models.Model):
    _name = 'appointment.product.line'

    product_id = fields.Many2one('product.product', ondelete='restrict', string='Product', required=True)
    appointment_id = fields.Many2one('hms.appointment', ondelete="cascade", string='Appointment')
    
class AppointmentCustom(models.Model):
    _inherit = 'hms.appointment'

    product_services_line_ids = fields.One2many('appointment.product.line', 'appointment_id', 'Services')

    def create_invoice(self):
        # product_id = self.product_idF
        # if not product_id:
        #     raise UserError(_("Please Set Consultation Service first."))
        product_data = []
        for product in self.product_services_line_ids:
            product_data.append({
                'product_id': product.product_id,
                'quantity': 1,
            })
        inv_data = {
            'ref_coiffure_id': self.ref_coiffure_id and self.ref_coiffure_id.id or False,
            'coiffure_id': self.coiffure_id and self.coiffure_id.id or False,
            'appointment_id': self.id,
            'salon_invoice_type': 'appointment',
        }

        pricelist_context = {}
        if self.pricelist_id:
            pricelist_context = {'acs_pricelist_id': self.pricelist_id.id}
        invoice = self.with_context(pricelist_context).acs_create_invoice(partner=self.patient_id.partner_id, patient=self.patient_id, product_data=product_data, inv_data=inv_data)
        invoice.action_post()
        self.invoice_id = invoice.id
        if self.state == 'to_invoice':
            self.appointment_done()

        if self.state == 'draft' and not self._context.get('avoid_confirmation'):
            if self.invoice_id and not self.company_id.acs_check_appo_payment:
                self.appointment_confirm()