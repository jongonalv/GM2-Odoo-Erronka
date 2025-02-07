# -*- coding: utf-8 -*-
{
    'name': "Ordezkaritzak",

    'summary': "Ordezkaritzak administratzeko moduloa",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'account'],

    # always loaded
    'data': [
        'views/ordezkaritza_views.xml',
        'views/ordezkaritza_historikoa_views.xml',
        'views/ordezkaritza_datuak_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}

