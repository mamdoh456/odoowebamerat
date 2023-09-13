# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Custom For Labalma',
    'category': 'Website/Website',
    'sequence': 20,
    'summary': 'website builder',
    'version': '1.0',
    'description': "",
    'depends': [
        'website', 'website_sale', 'acs_hms_online_appointment','acs_hms_base'
    ],

    'data': [
        'security/ir.model.access.csv',
        "data/product_category.xml",
        "views/assets.xml",
        "views/pages/template.xml",
        "views/pages/home.xml",
        "views/pages/categories_services.xml",
        "views/pages/invoice.xml",
        "views/pages/booking.xml",
        "views/pages/staff.xml",
        "views/pages/time.xml",
        "views/pages/personaldata.xml",
        "views/product_view.xml",
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'sequence': 5,
}
