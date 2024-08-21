from odoo import api, fields, models
from datetime import date

class SchoolStudents(models.Model):
    _name = "school.students"
    _description = "school students"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _log_access = True

    name = fields.Char(string='Student Name', required=True, tracking=True)
    # birthdate = fields.Date(string='Birthdate', required=True, tracking=True)
    phone = fields.Char(string='Phone Number', tracking=True)
    address = fields.Char(string='Address', tracking=True)
    detailed_age = fields.Char(string='Age', compute="_compute_detailed_age")
    # age = fields.Char(string='Age', compute="_compute_age")
    show_age = fields.Boolean(string='Show Age Details')
    parent = fields.Many2one('res.partner')
    active = fields.Boolean(string='Active', default=True)
    subjects = fields.Many2many('school.subjects', string='Subjects')

    image = fields.Image(string='Image')

    stage = fields.Many2one('school.stages', string='Stage')

    grade = fields.Many2one('school.grades', string='Grade')
    term = fields.Many2one('school.terms', string='Term')
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirmed'),
                              ('cancel', 'Canceled')], string='State', default='draft', required=True)

    # @api.depends('birthdate')
    # def _compute_detailed_age(self):
    #     for rec in self:
    #         today = date.today()
    #         if rec.birthdate:
    #
    #             all_days = today - rec.birthdate
    #             str_days = str(all_days)
    #             int_days = int(str_days[0: str_days.index(' ')])
    #
    #             years = int_days // 365
    #             months = (int_days % 365) // 30
    #             rest_days = (int_days % 365) % 30
    #
    #             rec.detailed_age = f"{years} Years, {months} Months, {rest_days} Days"
    #         else:
    #             rec.detailed_age = 0

    # @api.depends('birthdate')
    # def _compute_age(self):
    #     today = date.today()
    #     for rec in self:
    #         if rec.birthdate:
    #             rec.age = today.year - rec.birthdate.year
    #         else:
    #             rec.age = 0

    def object_confirm(self):
        for rec in self:
            rec.state = 'confirm'

        return {
            'effect': {
                'message': 'The New Student Has Been Registered Successfully',
                'type': 'rainbow_man',
                'fadeout': 'slow'
            }
        }

    def object_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.onchange('stage')
    def onchange_stage(self):
        for rec in self:
            return {
                'domain': {'grade': [('grade_stage', '=', rec.stage.stage_name)]}
            }

    @api.onchange('term')
    def onchange_term(self):
        for rec in self:
            return{
                'domain': {'subjects': [('stage', '=', rec.stage.stage_name),
                                        ('grade', '=', rec.grade.grade_name),
                                        # ('subjects_term', '=', rec.term.term_name)
                                        ]}
            }

class SchoolStages(models.Model):
    _name = "school.stages"
    _description = "school stages"
    _rec_name = 'stage_name'

    stage_name = fields.Char(string='Stage')
    stage_number = fields.Integer(string='Stage Number')


class SchoolGrades(models.Model):
    _name = "school.grades"
    _description = "school grades"
    _rec_name = 'grade_name'

    grade_name = fields.Char(string='Grade')
    grade_stage = fields.Many2many('school.stages')
