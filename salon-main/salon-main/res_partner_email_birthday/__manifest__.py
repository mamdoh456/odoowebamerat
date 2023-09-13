# -*- coding: utf-8 -*-
{
    "name": "Send Birthday Email and Gift Card",
    "version": "14.0",
    "category": "Tools",
    "author": "Ady",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        'bi_website_gift_cards',
    ],
    "data": [
        # Security
        "security/ir.model.access.csv",
        # Data
        "data/mail_templates.xml",
        # Views
        "views/res_partner_filter.xml",
        "views/send_email_action.xml",
        # Wizard
        "wizard/send_birthday_email.xml",

    ],
    "summary": "The tool for send email and gift card to customers",
}
