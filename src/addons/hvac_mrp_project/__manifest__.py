# -*- coding: utf-8 -*-
{
    'name': "Manufactuting Projects",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp','sale','purchase','web_kanban_gauge'],

    # always loaded
    'data': [
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/sale_order_mrp_projects.xml',
        'views/product_template_view.xml',
        'views/sale_order_task.xml',
        'wizards/add_product_wizard_view.xml',
        'wizards/recalculate_project_wizard_views.xml',
        'wizards/revise_project_views.xml',
        'views/hvac_mrp_task_views.xml',
        'views/hvac_mrp_project_views.xml',
        'report/mrp_report_bom_structure.xml'
    ],
    # only loaded in demonstration mode
    'qweb': ['static/src/xml/mrp.xml'],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}
