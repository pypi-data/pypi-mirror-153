"""
TODO
"""
from pathlib import Path

import pytest
from cppython_core.schema import (
    PEP621,
    CPPythonData,
    GeneratorConfiguration,
    PyProject,
    TargetEnum,
    ToolData,
)
from pytest_cppython.plugin import GeneratorUnitTests
from pytest_mock import MockerFixture

from cppython_vcpkg.plugin import VcpkgData, VcpkgGenerator

default_pep621 = PEP621(name="test_name", version="1.0")
default_cppython_data = CPPythonData(**{"target": TargetEnum.EXE})
default_tool_data = ToolData(**{"cppython": default_cppython_data})
default_pyproject = PyProject(**{"project": default_pep621, "tool": default_tool_data})
default_vcpkg_data = VcpkgData()


class TestCPPythonGenerator(GeneratorUnitTests):
    """
    The tests for the PDM interface
    """

    @pytest.fixture(name="generator")
    def fixture_generator(self) -> VcpkgGenerator:
        """
        Override of the plugin provided generator fixture.
        """
        configuration = GeneratorConfiguration(root_path=Path())
        return VcpkgGenerator(configuration, default_pep621, default_cppython_data, default_vcpkg_data)

    def test_install(self, generator: VcpkgGenerator, mocker: MockerFixture):
        """
        TODO
        """
