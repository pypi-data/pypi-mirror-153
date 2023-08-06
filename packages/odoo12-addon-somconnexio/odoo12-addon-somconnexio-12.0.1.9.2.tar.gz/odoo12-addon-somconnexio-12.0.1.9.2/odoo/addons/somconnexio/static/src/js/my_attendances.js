odoo.define('somconnexio.my_attendances_places', function (require) {
    var core = require('web.core');
    var QWeb = core.qweb;
    var MyAttendances = require('hr_attendance.my_attendances')
    var MyAttendancesPlaces = MyAttendances.include({
        events: {
            "click .o_hr_attendance_sign_in_out_icon": _.debounce(function() {
                this.update_attendance();
            }, 200, true),
            "focus #place": _.debounce(function() {
                $(".error").css("visibility", "hidden");
            }, 2000, true),
        },
        start: function () {
            var self = this;

            var def = this._rpc({
                    model: 'hr.employee',
                    method: 'search_read',
                    args: [[['user_id', '=', this.getSession().uid]], ['attendance_state', 'name']],
                })
                .then(function (res) {
                    self.employee = res.length && res[0];
                });

            var def_places = this._rpc({
                    model: 'hr.attendance.place',
                    method: 'search_read',
                    args: [[], ['code', 'name']],
                })
                .then(function (res) {
                    self.places = res.length && res;
                });

            var proms = $.when(def, def_places)
                .then(function() {
                    self.$el.html(QWeb.render("HrAttendanceMyMainMenu", {widget: self}));
                });

            return $.when(proms, this._super.apply(this, arguments));
        },

        update_attendance: function () {
            var self = this;
            var place_value = false;
            var place_full = true;
            var comments_value = false;
            if (this.employee.attendance_state != 'checked_in') {
                place_value = $("#place").val(); 
                if (!place_value) {
                    place_full = false;
                }
                comments_value = $("#comments").val();
                if (!comments_value) {
                    comments_value = false;
                }
            }

            if (place_full) {
                this._rpc({
                        model: 'hr.employee',
                        method: 'attendance_manual',
                        args: [
                            [self.employee.id],
                            'hr_attendance.hr_attendance_action_my_attendances', place_value, comments_value],
                    })
                    .then(function(result) {
                        if (result.action) {
                            self.do_action(result.action);
                        } else if (result.warning) {
                            self.do_warn(result.warning);
                        }
                    });
            } else {
                $(".error").css("visibility", "visible");
            }
        },
    });
});