# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools.translate import _


class product_template(models.Model):
    _inherit = "product.template"

    form_id = fields.Many2one('drug.form', ondelete='cascade', string='Drug Form', tracking=True)
    active_component_ids = fields.Many2many('active.comp', 'product_active_comp_rel', 'product_id','comp_id','Active Component')
    drug_company_id = fields.Many2one('drug.company', ondelete='cascade', string='Drug Company', help='Company producing this drug')
    salon_product_type = fields.Selection([
        ('medicament','Medicament'),
        ('fdrinks', 'Food & Drinks'),
        ('os', 'Other Service'),
        ('not_medical', 'Not Medical'),], string="salon Product Type", default='medicament')
    indications = fields.Text(string='Indication', help='Indications') 
    therapeutic_action = fields.Char(size=256, string='Therapeutic Effect', help='Therapeutic action')
    pregnancy_warning = fields.Boolean(string='Pregnancy Warning',
        help='The drug represents risk to pregnancy')
    lactation_warning = fields.Boolean('Lactation Warning',
        help='The drug represents risk in lactation period')
    pregnancy = fields.Text(string='Pregnancy and Lactancy',
        help='Warnings for Pregnant Women')

    notes = fields.Text(string='Extra Info')
    storage = fields.Char(string='Storage')
    adverse_reaction = fields.Char(string='Adverse Reactions')
    dosage = fields.Float(string='Dosage', help='Dosage')
    
    route_id = fields.Many2one('drug.route', ondelete='cascade', 
        string='Route', help='')
    form_id = fields.Many2one('drug.form', ondelete='cascade', 
        string='Form',help='Drug form, such as tablet or gel')
    need_partial_payment = fields.Boolean('Need Partial Payment',
        help='Need partial payment on the reservation')
    need_full_payment = fields.Boolean('Need Full Payment',
        help='Need Full payment on the reservation')
    advance_payment_amount = fields.Float(string='Amount of the reservation', help='Advance amount by the reservation')
