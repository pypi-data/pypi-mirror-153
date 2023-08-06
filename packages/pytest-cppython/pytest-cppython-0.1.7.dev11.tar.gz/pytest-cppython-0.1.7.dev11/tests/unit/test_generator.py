"""
Test the functions related to the internal generator implementation and the 'Generator' interface itself
"""

import pytest

from pytest_cppython.plugin import GeneratorUnitTests
from tests.data import (
    MockGenerator,
    test_configuration,
    test_cppython,
    test_generator,
    test_pep621,
)


class TestMockGenerator(GeneratorUnitTests):
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
