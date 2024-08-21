from odoo import api, fields, models

class SchoolSubjects(models.Model):
    _name = "school.subjects"
    _description = "school subjects"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'subject_name'

    students = fields.Many2one('school.students')
    subject_name = fields.Char(string='Subject Name', required=True)
    color = fields.Integer(string='Color')
    stage = fields.Many2one('school.stages', string='Stage')
    subjects_term = fields.Many2one('school.terms', string='Term')
    grade = fields.Many2one('school.grades', string='Grade')
    active = fields.Boolean(string='Active', default=True)

    # sponsor_image_512 = fields.Image(string='Sponsor Logo', related='sponsor_id.image_512')

    @api.onchange('stage')
    def onchange_stage(self):
        for rec in self:
            return {
                'domain': {'grade': [('grade_stage', '=', rec.stage.stage_name)]}
            }

class SchoolTerms(models.Model):
    _name = "school.terms"
    _description = "school terms"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'term_name'

    term_name = fields.Char(string='Term')
