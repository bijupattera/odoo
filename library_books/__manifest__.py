# -*- coding: utf-8 -*-
{
    'name': "library_books",

    'summary': """
        Library Management""",

    'description': """
        Long description of module's purpose
    """,

    'author': "BijuPattera",
    'website': "http://www.pattera.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'decimal_precision'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/library_books.xml',
        'views/respartner.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

'application': True,
}