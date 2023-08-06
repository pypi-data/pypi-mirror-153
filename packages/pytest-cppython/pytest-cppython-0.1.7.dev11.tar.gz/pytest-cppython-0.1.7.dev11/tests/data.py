"""
TODO
"""


import logging
from pathlib import Path
from typing import Type

from cppython_core.schema import (
    PEP621,
    CPPythonData,
    Generator,
    GeneratorConfiguration,
    GeneratorData,
    GeneratorDataT,
    Interface,
    InterfaceConfiguration,
    PyProject,
    TargetEnum,
    ToolData,
)

test_generator = GeneratorData()
test_cppython = CPPythonData(**{"target": TargetEnum.EXE})
test_tool = ToolData(cppython=test_cppython)
test_pep621 = PEP621(name="test-project", version="1.0.0", description="This is a test project")
test_pyproject = PyProject(project=test_pep621, tool=test_tool)

test_logger = logging.getLogger(__name__)
test_configuration = GeneratorConfiguration(root_path=Path())


class MockInterface(Interface):
    """
    TODO
    """

    def __init__(self, configuration: InterfaceConfiguration) -> None:
        super().__init__(configuration)

    @staticmethod
    def name() -> str:
        return "mock"

    def read_generator_data(self, generator_data_type: Type[GeneratorDataT]) -> GeneratorDataT:
        """
        TODO
        """
        return generator_data_type()

    def write_pyproject(self) -> None:
        """
        TODO
        """


class MockGenerator(Generator):
    """
    TODO
    """

    def __init__(
        self, configuration: GeneratorConfiguration, project: PEP621, cppython: CPPythonData, generator: GeneratorData
    ) -> None:
        super().__init__(configuration, project, cppython, generator)

        self.downloaded = False

    @staticmethod
    def name() -> str:
        return "mock"

    @staticmethod
    def data_type() -> Type[GeneratorData]:
        return GeneratorData

    def generator_downloaded(self, path: Path) -> bool:
        return self.downloaded

    def download_generator(self, path: Path) -> None:
        self.downloaded = True

    def update_generator(self, path: Path) -> None:
        pass

    def install(self) -> None:
        pass

    def update(self) -> None:
        pass

    def build(self) -> None:
        pass
