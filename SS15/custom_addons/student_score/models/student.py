from odoo import models, fields


class Student(models.Model):
    _inherit = "student.student"

    score_math = fields.Float(string="Math Score")
    score_english = fields.Float(string="English Score")
    score_average = fields.Float(string="Average Score", compute="_compute_score_average", store=True)

    def action_calculate_average(self):
        for record in self:
            record.score_average = (record.score_math + record.score_english) / 2 if (record.score_math or record.score_english) else 0.0

    def _compute_score_average(self):
        for record in self:
            record.score_average = (record.score_math + record.score_english) / 2 if (record.score_math or record.score_english) else 0.0

