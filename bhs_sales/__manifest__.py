# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom for Sales',
    'author': 'Bac Ha Software',
    'website': 'https://bachasoftware.com',
    'maintainer': 'Bac Ha Software',
    'version': '1.0',
    'category': 'Sales',
    'sequence': 75,
    'summary': 'Manage your BHS sale',
    'description': "Create and manage your sale",
    'depends': ['sale'],
    'data': [
        'views/sale_order_view.xml',
        'views/sale_report_view.xml'
    ],
    'demo': [],
    "external_dependencies": {},
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3'
}
