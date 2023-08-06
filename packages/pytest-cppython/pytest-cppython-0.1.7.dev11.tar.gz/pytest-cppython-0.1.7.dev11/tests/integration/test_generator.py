"""
Test the integrations related to the internal generator implementation and the 'Generator' interface itself
"""

import pytest

from pytest_cppython.plugin import GeneratorIntegrationTests
from tests.data import (
    MockGenerator,
    test_configuration,
    test_cppython,
    test_generator,
    test_pep621,
)


class TestMockGenerator(GeneratorIntegrationTests):
    """
    The tests for our Mock generator
    """

    @pytest.fixture(name="generator")
    def fixture_generator(self) -> MockGenerator:
        """
        Override of the plugin provided generator fixture.

        Returns:
            MockGenerator -- The Generator object to use for the CPPython defined tests
        """
        return MockGenerator(test_configuration, test_pep621, test_cppython, test_generator)

    def test_plugin_registration(self, generator: MockGenerator):
        """
        Override the base class preventing a registration check for the Mock
        """
