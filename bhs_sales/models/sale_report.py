# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
import datetime

class SaleReport(models.Model):
    _inherit = "sale.report"

    validity_date = fields.Date('Expiration', readonly=True)
    eom_accumulation = fields.Date(string="EOM accumulation", help="End of Month Accumulation.", readonly=True)

    bhs_project_id = fields.Many2one(
        comodel_name='project.project', string="BHS Project", readonly=True)

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['validity_date'] = "s.validity_date"
        res['eom_accumulation'] = "s.eom_accumulation"
        res['bhs_project_id'] = "l.bhs_project_id"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,
            s.validity_date, s.eom_accumulation, l.bhs_project_id"""
        return res

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        for g in groupby:
            if 'eom_accumulation' in g and self.env.context.get('order_by_eom_accumulation'):
                orderby = g + ' desc'
                break
        res = super(SaleReport, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                     orderby=orderby, lazy=lazy)
        return res

