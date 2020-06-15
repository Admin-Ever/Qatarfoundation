# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api, _
from odoo.tools import email_split
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


def extract_email(email):
    """ extract the email address from a user-friendly email address """
    addresses = email_split(email)
    return addresses[0] if addresses else ''


class Partner(models.Model):
    _inherit = 'res.partner'

    partner_code = fields.Char('Code')

    @api.model
    def signup_retrieve_info(self, token):
        res = super(Partner, self).signup_retrieve_info(token)
        partner = self._signup_retrieve_partner(token, raise_exception=True)
        res['partner_code'] = partner.partner_code
        return res

    def _signup_partner(self):
        group_portal = self.env.ref('base.group_portal')
        if self.company_id:
            company_id = self.company_id.id
        else:
            company_id = self.env.company.id
        user_portal = self.sudo().with_context(company_id=company_id)._create_user()
        if not user_portal.active or group_portal not in user_portal.groups_id:
            user_portal.write({'active': True, 'groups_id': [(4, group_portal.id)]})
            # prepare for the signup process
            # user_portal.partner_id.signup_prepare()
        # user_portal.partner_id.signup_prepare(signup_type="reset", expiration=False)
        # self.related_employee.user_id = user_portal
        user_portal.with_context(create_user=False).action_reset_password()
        return True

    def _create_user(self):
        """ create a new user for wizard_user.partner_id
            :returns record of res.users
        """
        company_id = self.env.context.get('company_id')
        return self.env['res.users'].with_context(no_reset_password=True)._create_user_from_template({
            'email': extract_email(self.email),
            'login': extract_email(self.email),
            'partner_id': self.id,
            'company_id': company_id,
            'company_ids': [(6, 0, [company_id])],
        })

    def _send_email(self, user):
        """ send notification email to a new portal user """
        if not self.env.user.email:
            raise UserError(_('You must have an email address in your User Preferences to send emails.'))

        # determine subject and body in the portal user's language
        template = self.env.ref('portal.mail_template_data_portal_welcome')
        for partner in self:
            lang = user.lang

            portal_url = partner.with_context(signup_force_type_in_url='', lang=lang)._get_signup_url_for_action()[
                partner.id]
            partner.signup_prepare()

            # return portal_url

            if template:
                template.with_context(dbname=self._cr.dbname, portal_url=portal_url, lang=lang).send_mail(partner.id,
                                                                                                          force_send=True)
            else:
                _logger.warning("No email template found for sending email to the portal user")

        return True
