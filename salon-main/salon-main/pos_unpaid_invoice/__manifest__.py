# -*- coding: utf-8 -*-
{
    "name": "POS Inpaid Invoice",
    "version": "14.0",
    "category": "Point Of Sale",
    "author": "Ady",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        'point_of_sale',
    ],
    "data": [
        # Data
        "data/data.xml",
        # Views
        "views/pos_config_views.xml",
        # Pos Assets
        "views/pos_assets.xml",


    ],
    "summary": "The tool for pos inpaid invoice management",
}
