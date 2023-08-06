odoo.define('somconnexio.many2manytags', function (require) {
    "use strict";

    var BasicModel = require('web.BasicModel');
    var core = require('web.core');
    var form_common = require('web.view_dialogs');
    var field_registry = require('web.field_registry');
    var relational_fields = require('web.relational_fields');

    var field_registry = require('web.field_registry');

    var M2MTags = relational_fields.FieldMany2ManyTags;


    var FieldMany2ManyTagsContractEmail = M2MTags.extend({
        fieldsToFetch: _.extend({}, M2MTags.prototype.fieldsToFetch, {
            email: { type: 'char' },
        }),
        tag_template: "FieldMany2ManyTagsContractEmail",
    });

    field_registry.add(
        'many2many_tags_contract_email',
        FieldMany2ManyTagsContractEmail);

});
