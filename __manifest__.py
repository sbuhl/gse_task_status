# -*- coding: utf-8 -*-

{
    'name': 'Tasks Stages and Status',
    'version': '0.2',
    'category': 'Hidden',
    'license': 'LGPL-3',
    'summary': 'Sales Orders',
    'description': """
        Display the status of a task. 
        Open | Closed
    """,
    'depends': ['sale_project'],
    'data': [
        'security/security.xml',
        'views/gse_sale_order_view.xml',
    ],
    'installable': True,

}
