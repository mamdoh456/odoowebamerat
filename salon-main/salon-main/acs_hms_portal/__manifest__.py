# -*- coding: utf-8 -*-

{
    'name' : 'salon Patient Portal Management',
    'summary' : 'This Module Adds salon Portal facility for Patients to allow access to their appointments and prescriptions',
    'description' : """
    This Module Adds salon Portal facility for Patients to allow access to their appointments and prescriptions
    HMS Website Portal acs hms salon management system medical
    """,
    'version': '1.0.7',
    'category': 'Medical',
    'author': 'Almighty Consulting Solutions Pvt. Ltd.',
    'website': '',
    'license': 'OPL-1',
    'depends' : ['portal','acs_hms','website_form'],
    'data' : [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/email_template.xml',
        'data/data.xml',
        'views/patient_view.xml',
        'views/template.xml',
        'views/res_config_settings_views.xml',
    ],
    'images': [

    ],
    'installable': True,
    'application': True,
    'sequence': 1,
    'price': 30,
    'currency': 'USD',
}
