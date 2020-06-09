odoo.define('helpdesk_hbku.website_my_portal', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    var publicWidget = require('web.public.widget');


    publicWidget.registry.WebsiteMyPortal = publicWidget.Widget.extend({
        selector: '.s_website_form',
        events: {
            'change #complaint_type': '_onChangeType',
            'change #complaint_against': '_onChangeAgainst',
        },


        /**
         * @override
         */
        start: function () {
            this.$type = this.$('#complaint_type');
            this.$against = this.$('#complaint_against');

            this.$related_student = this.$('#related_student');
            this.$related_college = this.$('#related_college');
            this.$related_employee = this.$('#related_staff');
            this.$related_services = this.$('#related_service');
            this.$other_complaints = this.$('#related_other');
            // this.$related_student.show();
            // this.$related_college.hide();
            // this.$related_employee.hide();
            // this.$related_services.hide();
            // this.$other_complaints.hide();
            return this._super.apply(this, arguments);
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         */

        _onChangeType: function () {
            var selectedId = this.$type.val();
            debugger;
            if (selectedId !== '') {
                ajax.jsonRpc("/website/portal/get_complaints_data", 'call', {
                    against: selectedId,
                    office_building: false,
                }).then(function (data) {
                    var options = '<option value=\"\">Complaint Against...</option>';
                    var againsts = data['againsts'];
                    // _.forEach(buildings, function (option) {
                    //     options.concat('<option value="'+option.id+'">'+option.name+'</option>')
                    // });
                    for (var i = 0; i < againsts.length; i++) {
                        options = options.concat('<option value="' + againsts[i].id + '" id="' + againsts[i].against + '" >' + againsts[i].name + '</option>');
                    }
                    $('#complaint_against').empty();
                    $('#complaint_against').append(options);
                })
            } else {
                this.$against.empty()
            }

        },

        _onChangeAgainst: function () {
            var selectedField = $(this.$against[0].selectedOptions)[0].id;
            if (selectedField == 'student') {
                this.$related_student.show();
                this.$related_college.hide();
                this.$related_employee.hide();
                this.$related_services.hide();
                this.$other_complaints.hide();
            } else if (selectedField == 'college') {
                this.$related_student.hide();
                this.$related_college.show();
                this.$related_employee.hide();
                this.$related_services.hide();
                this.$other_complaints.hide();
            } else if (selectedField == 'staff') {
                this.$related_student.hide();
                this.$related_college.hide();
                this.$related_employee.show();
                this.$related_services.hide();
                this.$other_complaints.hide();
            } else if (selectedField == 'service') {
                this.$related_student.hide();
                this.$related_college.hide();
                this.$related_employee.hide();
                this.$related_services.show();
                this.$other_complaints.hide();
            } else if (selectedField == 'other') {
                this.$related_student.hide();
                this.$related_college.hide();
                this.$related_employee.hide();
                this.$related_services.hide();
                this.$other_complaints.show();
            } else {
                this.$related_student.hide();
                this.$related_college.hide();
                this.$related_employee.hide();
                this.$related_services.hide();
                this.$other_complaints.hide();
            }


        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        // _onCGVCheckboxClick: function () {
        //     this._adaptPayButton();
        // },
    });
});


// odoo.define('website_calendar.appointment_form', function (require) {
//     'use strict';
//
//     require('web_editor.ready');
//
//     if (!$('.o_website_calendar_form').length) {
//         return $.Deferred().reject("DOM doesn't contain '.o_website_calendar_form'");
//     }
//
//     $(".appointment_submit_form select[name='country_id']").change(function () {
//         var country_code = $(this).find('option:selected').data('phone-code');
//         $('.appointment_submit_form #phone_field').val(country_code);
//     });
// });
