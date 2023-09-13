# -*- coding: utf-8 -*-
#║                                                                      ║
#╚══════════════════════════════════════════════════════════════════════╝
{
    'name': 'Reservation Management System',
    'summary': 'reservation Management System',
    'description': """
        
    """,
    'version': '1.2.34',
    'category': 'Sales',
    'author': 'Almighty Consulting Solutions Pvt. Ltd.',
    'support': '',
    'website': '',
    'license': 'OPL-1',
    'depends': ['acs_hms_base', 'web_timer_widget', 'website'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/patient_cardreport.xml',
        'report/report_prescription.xml',
        'report/appointment_report.xml',
        'report/evaluation_report.xml',

        'data/sequence.xml',
        'data/mail_template.xml',
        'data/hms_data.xml',
        
        'wizard/cancel_reason_view.xml',

        'views/hms_base_views.xml',
        'views/patient_view.xml',
        'views/physician_view.xml',
        'views/evaluation_view.xml',
        'views/appointment_view.xml',
        'views/diseases_view.xml',
        'views/medicament_view.xml',
        'views/prescription_view.xml',
        'views/medication_view.xml',
        'views/treatment_view.xml',
        'views/resource_cal.xml',
        'views/medical_alert.xml',
        'views/account_view.xml',
        'views/template.xml',
        'views/res_config_settings_views.xml',
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
