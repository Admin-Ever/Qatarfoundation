# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ComplaintType(models.Model):
    _name = 'complaint.type'

    name = fields.Char('Name')


class ComplaintAgainst(models.Model):
    _name = 'complaint.against'

    name = fields.Char('Name')
    related_type = fields.Many2many('complaint.type',
                                    string='Complaint Type')
    against = fields.Selection(
        [('student', 'Students'), ('college', 'Colleges'), ('staff', 'Staffs'), ('service', 'Services'),
         ('other', 'Others')],
        'Against Data')


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    complaint_type = fields.Many2one('complaint.type',
                                     'Complaint Type')

    complaint_against = fields.Many2one('complaint.against',
                                        'Complaint Against')
    related_against = fields.Selection(related='complaint_against.against')
    related_student = fields.Many2one('res.partner', 'Student',domain="[('custom_type','=','student')]")
    related_college = fields.Many2one('res.partner', 'College',domain="[('custom_type','=','college')]")
    related_employee = fields.Many2one('res.partner', 'Staff',domain="[('custom_type','=','staff')]")
    related_services = fields.Selection([('career', 'Career Service'),
                                         ('registrar', 'Registrar Service'),
                                         ('engagement', 'Engagement Service'),
                                         ('sport', 'Sport Service'),
                                         ('hawiyati', 'Hawiyati Cards Service'),
                                         ('it', 'Information Technology'),
                                         ('service', 'Service'),
                                         ('lib', 'Library'),
                                         ('food', 'Food Services'),
                                         ('medical', 'Medical Services'),
                                         ], 'Services')
    other_complaints = fields.Selection([('chss', 'Dean of CHSS'),
                                         ('chls', 'Dean of CHlS'),
                                         ('cse', 'Dean of CSE'),
                                         ('cis', 'Dean of CIS'),
                                         ('cl', 'Dean of CL'),
                                         ('cpp', 'Dean of CPP'),
                                         ('other', 'I am not sure'),
                                         ], 'Direct Complaint')

    date_incident = fields.Date('Date of Incident')

    location_incident = fields.Char('Location of Incident')

    terms_and_conditions = fields.Boolean('Terms and Conditions')


class Partner(models.Model):
    _inherit = "res.partner"

    custom_type = fields.Selection([('student', 'Student'), ('staff', 'Staff'), ('college', 'College')], 'Contact Type')
