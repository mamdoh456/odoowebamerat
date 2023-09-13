# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class coiffureSpecialty(models.Model):
    _name = 'coiffure.specialty'
    _description = "coiffure Specialty"

    code = fields.Char(string='Code')
    name = fields.Char(string='Specialty', required=True, translate=True)

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
    ]


class coiffureDegree(models.Model):
    _name = 'coiffure.degree'
    _description = "coiffure Degree"

    name = fields.Char(string='Degree')

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
    ]


class Coiffure(models.Model):
    _name = 'hms.coiffure'
    _description = "coiffure"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    user_id = fields.Many2one('res.users', string='Related User',
                              ondelete='cascade', help='User-related data of the coiffure')
    name = fields.Char(string='Name', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    mobile = fields.Char(string='Mobile', tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    code = fields.Char(string='coiffure Code', default='/', tracking=True)
    degree_ids = fields.Many2many('coiffure.degree', 'coiffure_rel_education', 'coiffure_ids', 'degree_ids',
                                  string='Degree')
    specialty_id = fields.Many2one('coiffure.specialty', ondelete='set null', string='Specialty',
                                   help='Specialty Code', tracking=True)
    medical_license = fields.Char(string='Medical License', tracking=True)
    product_services_ids = fields.Many2many('product.product',
                                            string='Services', domain=[('type', '=', 'service')])

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    image_1024 = fields.Image("Image 1024", )
    image_512 = fields.Image("Image 512", )
    image_256 = fields.Image("Image 256", )

    @api.model
    def create(self, values):
        if values.get('code', '/') == '/':
            values['code'] = self.env['ir.sequence'].next_by_code('hms.coiffure')
        if values.get('email'):
            values['login'] = values['email']
        return super(Coiffure, self).create(values)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
