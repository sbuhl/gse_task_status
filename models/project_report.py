from odoo import api, fields, models, tools

class ReportProjectTaskUser(models.Model):
    _inherit = "report.project.task.user"

    mo_value_technician = fields.Many2one('project.task', 'MO Value Technician', readonly=True, auto_join=True, index=True)

    @api.model
    def _select(self):
        return super()._select() + ", t. mo_value_technician AS  mo_value_technician"

    @api.model
    def _group_by(self):
        return super()._group_by() + ", t. mo_value_technician"

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
    CREATE view %s as
         SELECT %s
           FROM %s
          WHERE %s
       GROUP BY %s
        """ % (self._table, self._select(), self._from(), self._where(), self._group_by()))



    