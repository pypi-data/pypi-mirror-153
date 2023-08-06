from unittest import TestCase

from openmodule.utils.misc_functions import clean_service_name


class Base64ValidatorTest(TestCase):
    def test_clean_service_name(self):
        self.assertEqual(clean_service_name("om_alpr_nn_1"), "alpr_nn")
        self.assertEqual(clean_service_name("omg_alpr_nn_1r"), "omg_alpr_nn_1r")
        self.assertEqual(clean_service_name("enforcement:service"), "enforcement:service")
