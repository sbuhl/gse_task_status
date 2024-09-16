
from odoo import fields, models



class ReportProjectTaskUser(models.Model):
    _inherit = 'report.project.task.user.fsm'


    mo_value_technician = fields.Many2one('project.task', 'MO Value Technician', readonly=True, auto_join=True, index=True)
    
