# -*- coding: utf-8 -*-

from odoo import models


class ProjectTask(models.Model):
    _inherit = "project.task"

    def write(self, vals):
        res = super().write(vals)
        if 'user_ids' in vals:
            # If you need to clear a specific cache, replace this with the correct method
            pass  # No clear_caches method used
        return res
    