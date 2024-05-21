# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.tools import date_utils
import datetime


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    bhs_project_id = fields.Many2one('project.project', string="BHS Project")

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_price_unit(self):
        for line in self:
            # check if there is already invoiced amount. if so, the price shouldn't change as it might have been
            # manually edited
            if line.qty_invoiced > 0:
                continue
            # check if option change_line_by_pricelist not checked
            # manually edited
            if not line.order_id.change_line_by_pricelist:
                continue
            if not line.product_uom or not line.product_id:
                line.price_unit = 0.0
            else:
                price = line.with_company(line.company_id)._get_display_price()
                line.price_unit = line.product_id._get_tax_included_unit_price(
                    line.company_id or line.env.company,
                    line.order_id.currency_id,
                    line.order_id.date_order,
                    'sale',
                    fiscal_position=line.order_id.fiscal_position_id,
                    product_price_unit=price,
                    product_currency=line.currency_id
                )

class SaleOrder(models.Model):
    _inherit = "sale.order"

    change_line_by_pricelist = fields.Boolean(string='Change line by Pricelist?', default=True)

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
