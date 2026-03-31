# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.tools import date_utils
import datetime


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    bhs_project_id = fields.Many2one('project.project', string="BHS Project")

class SaleOrder(models.Model):
    _inherit = "sale.order"

    amount_total_main = fields.Monetary(
        string='Total in main currency',
        compute='_compute_amount_total_main', store=True, readonly=True,
        currency_field='company_currency_id'
    )

    company_currency_id = fields.Many2one(
        string='Company Currency',
        related='company_id.currency_id', readonly=True,
    )

    def _get_default_date(self):
        today = fields.Date.today()
        if today.day < 5:
            month = fields.Date.today().month
            month = month - 1 if month != 1 else 12
            return today.replace(month=month, day=15)
        else:
            return fields.Date.today()

    eom_accumulation = fields.Date(
        string="EOM accumulation",
        help="End of Month Accumulation.", default=lambda self: self._get_default_date())

    @api.depends('currency_id', 'currency_rate', 'amount_total')
    def _compute_amount_total_main(self):
        for so in self:
            so.amount_total_main = (so.amount_total/so.currency_rate)
