# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import datetime
from odoo.addons.website_helpdesk_form.controller.main import WebsiteForm
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class WebsiteForm(WebsiteForm):

    @http.route('''/helpdesk/<model("helpdesk.team", "[('use_website_helpdesk_form','=',True)]"):team>/submit''',
                type='http', auth="user", website=True)
    def website_helpdesk_form(self, team, **kwargs):
        if not team.active or not team.website_published:
            return request.render("website_helpdesk.not_published_any_team")
        default_values = {}
        complaint_type = request.env['complaint.type'].search([])
        complaint_against = []
        partners = request.env['res.partner'].search([])
        employees = partners.filtered(lambda x: x.custom_type == 'staff')
        students = partners.filtered(lambda x: x.custom_type == 'student')
        colleges = partners.filtered(lambda x: x.custom_type == 'college')
        related_services = [('career', 'Career Service'),
                            ('registrar', 'Registrar Service'),
                            ('engagement', 'Engagement Service'),
                            ('sport', 'Sport Service'),
                            ('hawiyati', 'Hawiyati Cards Service'),
                            ('it', 'Information Technology'),
                            ('service', 'Service'),
                            ('lib', 'Library'),
                            ('food', 'Food Services'),
                            ('medical', 'Medical Services'),
                            ]
        others = [('chss', 'Dean of CHSS'),
                  ('chls', 'Dean of CHlS'),
                  ('cse', 'Dean of CSE'),
                  ('cis', 'Dean of CIS'),
                  ('cl', 'Dean of CL'),
                  ('cpp', 'Dean of CPP'),
                  ('other', 'I am not sure'),
                  ]
        if request.env.user.partner_id != request.env.ref('base.public_partner'):
            default_values['name'] = request.env.user.partner_id.name
            default_values['email'] = request.env.user.partner_id.email
        return request.render("website_helpdesk_form.ticket_submit",
                              {'employees': employees,
                               'complaint_against': complaint_against,
                               'students': students,
                               'colleges': colleges,
                               'services': related_services,
                               'others': others,
                               'complaint_type': complaint_type, 'team': team,
                               'default_values': default_values})

    @http.route('/website_form/<string:model_name>', type='http', auth="user", methods=['POST'], website=True)
    def website_form(self, model_name, **kwargs):
        if request.params.get('partner_email'):
            Partner = request.env['res.partner'].sudo().search([('email', '=', kwargs.get('partner_email'))], limit=1)
            if Partner:
                request.params['partner_id'] = Partner.id
        if request.params.get('date_incident'):
            lang = request.env['ir.qweb.field'].user_lang()
            request.params['date_incident'] = datetime.datetime.strptime(request.params.get('date_incident'),
                                                                         "%Y-%m-%d").strftime(
                lang.date_format)
        return super(WebsiteForm, self).website_form(model_name, **kwargs)

    @http.route(['/website/portal/get_complaints_data'], type='json', auth="user", methods=['POST'],
                website=True)
    def get_complains_info(self, against, office_building, **kwargs):
        if against:
            againsts = request.env['complaint.against'].sudo().search([('related_type', '=', int(against))])
            builds = []
            for build in againsts:
                builds.append({'id': build.id, 'name': build.name, 'against': build.against})
            return {'againsts': builds}
        if office_building:
            floors = request.env['office.floor'].sudo().search([('related_base', '=', int(office_building))])
            builds = []
            for build in floors:
                builds.append({'id': build.id, 'name': build.name})
            return {'floors': builds}
