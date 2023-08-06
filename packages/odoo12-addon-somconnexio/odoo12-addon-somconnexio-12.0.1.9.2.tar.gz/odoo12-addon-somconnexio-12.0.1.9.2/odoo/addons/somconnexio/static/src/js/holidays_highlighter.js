// Copyright (C) 2018 by Camptocamp
// (C) 2021 by Coopdevs Treball SCCL
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define('somconnexio.holidays_highlighter', function (require) {
    'use strict';
    var calendarView = require('web.CalendarRenderer');
    //var Model = require('web.Model');

    calendarView.include({
        willStart: function () {
            var defHolidays = this._rpc({
                model: 'hr.holidays.public.line',
                method: 'search_read',
                args: [[], ['date']],
            });
            var defWeekendEnabled = this._rpc({
                model: 'ir.config_parameter',
                method: 'get_param',
                args: ['somconnexio.public_holiday_weekend_enabled'],
            });
            var defHolidayColor = this._rpc({
                model: 'ir.config_parameter',
                method: 'get_param',
                args: ['somconnexio.public_holiday_color'],
            });

            return $.when(defHolidays, defHolidayColor, defWeekendEnabled, this._super())
                .then(function (holidays, color, weekendEnabled) {
                    // As a result of `search_read` call is the JS object
                    // (dictionary), it's still our duty to clean up results
                    this.publicHolidays = holidays.map(
                        function (holiday) {
                            return holiday.date;
                        });
                    this.holidayColor = color;
                    this.weekendEnabled = Boolean(Number(weekendEnabled));
                }.bind(this));
        },
        _render: function() {
            var res = this._super();
            var self = this;
            setTimeout(function() {
                var visibleDays = self.$('.o_calendar_view .fc-day');
                _.each(visibleDays, function (dayCell) {
                    var dayDate = dayCell.getAttribute('data-date');
                    var [_, year, month, day] =
                        /(\d{4})-(\d{2})-(\d{2})/.exec(dayDate);
                    var date = new Date(year, month-1, day);
                    if (
                        self.publicHolidays.includes(dayDate) ||
                        (self.weekendEnabled && [6,0].includes(date.getDay()))
                    ) {
                        dayCell.style.backgroundColor = self.holidayColor;
                    }
                });
            });
            return res;
        }
    })
});
