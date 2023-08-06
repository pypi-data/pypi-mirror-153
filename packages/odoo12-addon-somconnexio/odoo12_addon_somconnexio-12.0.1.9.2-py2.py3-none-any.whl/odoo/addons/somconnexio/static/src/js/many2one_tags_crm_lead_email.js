odoo.define('somconnexio.many2onetags', function (require) {
    "use strict";

    var relational_fields = require('web.relational_fields');
    var field_registry = require('web.field_registry');
    var M21Tags = relational_fields.FieldMany2OneTags;


    var FieldMany2OneTagsCRMLeadEmail = M21Tags.extend({
        fieldsToFetch: _.extend({}, M21Tags.prototype.fieldsToFetch, {
            email: { type: 'char' },
        }),
        tag_template: "FieldMany2OneTagsCRMLeadEmail",
    });

    field_registry.add(
        'many2one_tags_crm_lead_email',
        FieldMany2OneTagsCRMLeadEmail);

});
