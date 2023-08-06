from ..sc_test_case import SCTestCase


class TestServerAction(SCTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestServerAction, cls).setUpClass()
        # disable tracking test suite wise
        cls.env = cls.env(context=dict(
            cls.env.context,
            tracking_disable=True,
            test_queue_job_no_delay=False,
        ))

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.QueueJob = self.env['queue.job']
        self.partner = self.browse_ref('somconnexio.res_partner_2_demo')
        product_id = self.browse_ref('somconnexio.Fibra100Mb')
        broadband_isp_info = self.env['broadband.isp.info'].create(
            {
                'type': 'new',
                'phone_number': '98282082',
            }
        )
        self.line_params = {
            'name': product_id.name,
            'product_id': product_id.id,
            'product_tmpl_id': product_id.product_tmpl_id.id,
            'category_id': product_id.product_tmpl_id.categ_id.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        self.jobs_domain = [
            ('method_name', '=', '_send_background_email'),
            ('model_name', '=', 'ir.actions.server'),
        ]
        self.queued_jobs_before = self.QueueJob.search(self.jobs_domain)

        self.server_action = self.env['ir.actions.server'].search([
            ('name', '=', 'Send email on CRM Lead Line creation'),
            ('state', '=', 'background_email'),
        ])

    def test_run_action_background_email(self):
        self.assertFalse(self.queued_jobs_before)

        lead_line = self.env['crm.lead.line'].create(self.line_params)

        # The trigger from the base automation 'send_email_on_crm_lead_line_creation'
        # does not work automatically with odoo testing, so in here we will be forcing
        # the method execution ('run_action_background_email')
        self.server_action.with_context(
            active_id=lead_line.id).run_action_background_email('')

        queued_jobs_after = self.QueueJob.search(self.jobs_domain)
        self.assertEquals(1, len(queued_jobs_after))

    def test_do_not_run_action_background_email_change_address(self):
        self.assertFalse(self.queued_jobs_before)

        lc_broadband_isp_info = self.env['broadband.isp.info'].create(
            {
                'type': 'location_change',
                'phone_number': '98282082',
            }
        )
        self.line_params.update({
            'broadband_isp_info': lc_broadband_isp_info.id
        })
        lead_line = self.env['crm.lead.line'].create(self.line_params)
        self.server_action.with_context(active_id=lead_line.id)

        queued_jobs_after = self.QueueJob.search(self.jobs_domain)
        self.assertFalse(queued_jobs_after)

    def test_do_not_run_action_background_email_ba_change_holder(self):
        self.assertFalse(self.queued_jobs_before)

        hc_broadband_isp_info = self.env['broadband.isp.info'].create(
            {
                'type': 'holder_change',
                'phone_number': '98282082',
            }
        )
        self.line_params.update({
            'broadband_isp_info': hc_broadband_isp_info.id
        })
        lead_line = self.env['crm.lead.line'].create(self.line_params)
        self.server_action.with_context(active_id=lead_line.id)

        queued_jobs_after = self.QueueJob.search(self.jobs_domain)
        self.assertFalse(queued_jobs_after)

    def test_do_not_run_action_background_email_mbl_change_holder(self):
        self.assertFalse(self.queued_jobs_before)

        hc_mobile_isp_info = self.env['mobile.isp.info'].create(
            {
                'type': 'holder_change',
                'phone_number': '98282082',
            }
        )
        self.line_params.update({
            'mobile_isp_info': hc_mobile_isp_info.id
        })
        lead_line = self.env['crm.lead.line'].create(self.line_params)
        self.server_action.with_context(active_id=lead_line.id)

        queued_jobs_after = self.QueueJob.search(self.jobs_domain)
        self.assertFalse(queued_jobs_after)
