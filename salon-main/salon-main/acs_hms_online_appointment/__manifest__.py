# -*- coding: utf-8 -*-

#║                                                                      ║
#╚══════════════════════════════════════════════════════════════════════╝
{
    'name' : 'Online Appointment',
    'summary' : 'Allow Customers to Book an Appointment on-line from portal',
    'description' : """Website Portal to Book an Appointment online.""",
    'version': '14.0.1',
    'category': 'Sale',
    'author': 'Almighty Consulting Solutions Pvt. Ltd.',
    'website': '',
    'license': 'OPL-1',
    'depends' : ['acs_hms_portal','website_payment','account_payment'],
    'data' : [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/website_page.xml',
        'views/hms_base_view.xml',
        'views/schedule_views.xml',
        'views/template.xml',
        'views/res_config_settings_views.xml',
        'wizard/appointment_scheduler_wizard.xml',
        'views/menu_item.xml',
    ],
    'images': [

    ],
    'installable': True,
    'application': True,
    'sequence': 1,
    'price': 70,
    'currency': 'USD',
}