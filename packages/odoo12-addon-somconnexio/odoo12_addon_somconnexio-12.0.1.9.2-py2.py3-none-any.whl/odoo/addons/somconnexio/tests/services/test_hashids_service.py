from ..sc_test_case import SCTestCase
from ...services.hashids_service import HashGetter
from mock import patch, ANY


class HashIDsTests(SCTestCase):

    @patch('odoo.addons.somconnexio.services.hashids_service.Hashids')
    def test_deterministic_hash(self, hashids_mock):
        generated_hash = 'XxXx'
        hashids_mock.return_value.encode.return_value = generated_hash
        hash_code = HashGetter(ANY).get()
        self.assertEqual(
            generated_hash.upper(), hash_code
        )
