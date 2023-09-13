# -*- coding: utf-8 -*-

from odoo import api,fields,models,_


class AccountMove(models.Model):
    _inherit = 'account.move'

    patient_id = fields.Many2one('hms.patient',  string='Client', index=True, readonly=True, states={'draft': [('readonly', False)]})
    coiffure_id = fields.Many2one('hms.coiffure', string='coiffure', readonly=True, states={'draft': [('readonly', False)]}) 
    salon_invoice_type = fields.Selection([
        ('patient','Patient')], string="salon Invoice Type")

    @api.onchange('patient_id')
    def onchange_patient(self):
        if self.patient_id and not self.partner_id:
        	self.partner_id = self.patient_id.partner_id.id
