from abc import abstractmethod, ABC
from typing import List, Dict, Set, Optional
import sys

from johnsnowlabs.abstract_base.lib_resolvers import JslLibDependencyResolverABC
from johnsnowlabs.utils.enums import ProductName, ProductPlatform, LibVersionIdentifier, ProductLogo, ProductSlogan
from johnsnowlabs.utils.env_utils import try_import, try_import_in_venv
from johnsnowlabs.utils.jsl_secrets import JslSecrets
from johnsnowlabs.utils.pip_utils import install_standard_pypi_lib, install_licensed_pypi_lib


class AbstractSoftwareProduct(ABC):
    """Only first degree dependencies may be contained in the hard/licensed/optional/ dependency lists
     Higher degree dependencies will be resolved by iterating the dependency graph
     By default the ABC implements a check_installed based on import.

     """
    name: ProductName
    logo: ProductLogo
    slogan: ProductSlogan = None
    platforms: Set[ProductPlatform] = set()
    hard_dependencies: Set['AbstractSoftwareProduct'] = set()
    licensed_dependencies: Set['AbstractSoftwareProduct'] = set()
    optional_dependencies: Set['AbstractSoftwareProduct'] = set()
    py_module_name: Optional[str] = None
    pypi_name: Optional[str] = None
    # Only defined for JSL libs below
    latest_version: Optional[LibVersionIdentifier] = None
    jsl_url_resolver: Optional[JslLibDependencyResolverABC] = None
    licensed: bool = False

    @classmethod
    def check_installed(cls, python_exec_path=None) -> bool:

        if cls.py_module_name and not python_exec_path:
            return try_import(cls.py_module_name)
        elif python_exec_path:
            return try_import_in_venv(cls.py_module_name, python_exec_path)
        print(f'Assuming {cls.name} is installed, no checks defined.')
        return True

    @classmethod
    def check_dependencys(cls, python_exec_path=None) -> bool:
        print(f'Assuming {cls.name} dependencies are fine, no checks defined.')
        return True

    @classmethod
    def health_check(cls) -> bool:
        print(f'Assuming {cls.name} is ok, no checks defined.')
        return True

    @classmethod
    def install(cls, secrets: Optional[JslSecrets] = None, py_path=sys.executable, upgrade=True) -> bool:
        """
        Install the product with default settings.
        Defaults to Pypi name install.
        """

        if cls.pypi_name:
            if secrets:
                return install_licensed_pypi_lib(secrets, cls.pypi_name, cls.py_module_name)
            else:
                return install_standard_pypi_lib(cls.pypi_name, cls.py_module_name,
                                                 python_path=py_path, upgrade=upgrade)
        return True
        # raise NotImplemented(f'No install defined for {cls.name}')

    @classmethod
    def install_cli(cls, ) -> bool:
        """
        Install the product configurable interactive from CLI
        TODO interactive Pypi?
        """
        if cls.pypi_name:
            return install_standard_pypi_lib(cls.pypi_name)
        raise NotImplemented(f'No install defined for {cls.name}')
