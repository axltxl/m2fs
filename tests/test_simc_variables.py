# -*- coding: utf-8 -*-

import math
from midi2sim import simc


class TestSimConnectVariable:
    test_var_default = "HEADING_INDICATOR"
    test_var_mobiflight = "(A:HEADING INDICATOR,radians)"
    timeout = 1

    def test_get_variable_across_backends(self):
        """
        Test whether HEADING_INDICATOR variable
        is consistent in both backends
        """

        simc.set_backend(simc.SIMCONNECT_BACKEND_DEFAULT)
        simc.connect(timeout=self.timeout)
        v1 = simc.get_variable(self.test_var_default)
        simc.disconnect()

        simc.set_backend(simc.SIMCONNECT_BACKEND_MOBIFLIGHT)
        simc.connect(timeout=self.timeout)
        v2 = simc.get_variable(self.test_var_mobiflight)
        simc.disconnect()

        assert math.floor(v1.value) == math.floor(v2.value)
