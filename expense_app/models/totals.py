from odoo import api, fields, models, tools
from odoo.tools.translate import _

class ExpenseTotals(models.Model):
    _name = 'expense.totals'
    _auto = False
    _rec_name = 'id'
    _description = 'Total of all tables'
    asset_total = fields.Float('Total Assets ₹', readonly=True)
    expense_total = fields.Float('Total Expense ₹', readonly=True)
    income_total = fields.Float('Total Income ₹', readonly=True)
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW expense_totals AS
            (
            SELECT * from (
            SELECT round(sum(value), 2)AS asset_total, min(id) as id FROM fd_invest WHERE active = 't') t1,(
            SELECT round(sum(total), 2)AS expense_total FROM home_daily WHERE date_part('year', date) = date_part('year', CURRENT_DATE)) t2, (
            SELECT round(sum(total), 2)AS income_total FROM varu_manam WHERE date_part('year', date) = date_part('year', CURRENT_DATE)) t3
            );
            """)
        
