# -*- coding: utf-8 -*-

{
    'name': 'Appointment Management System Base',
    'summary': 'Appointment Management System Base for further flows',
    'description': """
        
    """,
    'version': '1.0.12',
    'category': 'sales',
    'author': 'Almighty Consulting Solutions Pvt. Ltd.',
    'support': '',
    'website': '',
    'license': 'OPL-1',
    'depends': ['account', 'stock', 'hr'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'report/paper_format.xml',
        'report/report_layout.xml',
        'report/report_invoice.xml',

        'data/sequence.xml',
        'data/mail_template.xml',
        'data/company_data.xml',

        'views/assets_view.xml',
        'views/hms_base_views.xml',
        'views/patient_view.xml',
        'views/physician_view.xml',
        'views/product_view.xml',
        'views/drug_view.xml',
        'views/account_view.xml',
        'views/res_config_settings.xml',
        'views/menu_item.xml',
    ],
    'pre_init_hook': 'pre_init_hook',
    'images': [

    ],
    'installable': True,
    'application': True,
    'sequence': 1,
    'price': 36,
    'currency': 'USD',
}
