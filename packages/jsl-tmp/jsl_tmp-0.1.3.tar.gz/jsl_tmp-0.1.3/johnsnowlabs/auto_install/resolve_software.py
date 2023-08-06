import sys

from johnsnowlabs.abstract_base.software_product import AbstractSoftwareProduct
from johnsnowlabs.auto_install.spark_nlp_software import Software
from johnsnowlabs.utils.enums import ProductName
from johnsnowlabs.utils.jsl_secrets import JslSecrets
from johnsnowlabs.utils.pip_utils import install_standard_pypi_lib


def check_dependencies(product: AbstractSoftwareProduct,
                       secrets: JslSecrets,
                       running_in_databricks: bool = False,
                       python_exec_path: str = sys.executable,
                       install_optional: bool = False,
                       install_licensed: bool = True,
                       sparknlp_to_latest: bool = True
                       ):
    """
    # NOTE: There is no product that has licensed dependencies.
    # INVARIANT :
    # Either the product itself is licensed and then no dependencies require license
    # Or product is free but it has licensed dependencies
    # -1 for DFS
    # 0 for BFS
    Spark NLP must be installed last, because we cannot re-load a lib
    :param product:
    :param secrets:
    :param running_in_databricks:
    :param python_exec_path:
    :param install_optional:
    :param install_licensed: install licensed products if license permits it
    :param sparknlp_to_latest: for some releases we might not want to go to latest spark release
    """
    # TODO check if licensed secrets.version matches up with latest. if not print info
    import site
    from importlib import reload
    reload(site)

    hard_nodes: Set[AbstractSoftwareProduct] = set([product])
    licensed_nodes: Set[AbstractSoftwareProduct] = set([])
    optional_nodes: Set[AbstractSoftwareProduct] = set([])
    install_results: Dict[AbstractSoftwareProduct:bool] = {}
    while hard_nodes:
        # 1. Check and install all hard dependencies
        hard_node = hard_nodes.pop()
        # a | b is equal to a.union(b)
        hard_nodes = hard_nodes | hard_node.hard_dependencies
        licensed_nodes = licensed_nodes | hard_node.licensed_dependencies
        optional_nodes = optional_nodes | hard_node.optional_dependencies

        if hard_node.check_installed():
            pass
        elif hard_node not in install_results and hard_node.name != ProductName.spark_nlp.value:
            # Only install if we don't already have an installation result
            # It could be that in previous iteration we have failed to install
            # So we don't need to try again here if an entry already exists
            install_results[hard_node] = hard_node.install(secrets) if hard_node.licensed else hard_node.install()

        # 2. Check and install all licensed dependencies
        if install_licensed:
            while licensed_nodes:
                licensed_node = licensed_nodes.pop()
                hard_nodes = hard_nodes | licensed_node.hard_dependencies
                licensed_nodes = licensed_nodes | licensed_node.licensed_dependencies
                optional_nodes = optional_nodes | licensed_node.optional_dependencies

                if licensed_node.check_installed():
                    pass
                elif licensed_node not in install_results and licensed_node.name != ProductName.spark_nlp.value :
                    install_results[licensed_node] = licensed_node.install(secrets)

        # 3. Check and install all optional dependencies
        if install_optional:
            # optional_nodes = optional_nodes | hard_node.optional_dependencies
            while optional_nodes:
                optional_node = optional_nodes.pop()
                hard_nodes = hard_nodes | optional_node.hard_dependencies
                licensed_nodes = licensed_nodes | optional_node.licensed_dependencies
                optional_nodes = optional_nodes | optional_node.optional_dependencies
                if optional_node.check_installed():
                    pass
                elif optional_node not in install_results and optional_node.name != ProductName.spark_nlp.value :
                    install_results[optional_node] = optional_node.install(
                        secrets) if optional_node.licensed else optional_node.install()

    if sparknlp_to_latest:
        # quick hack, todo cleaner
        install_results[Software.spark_nlp] = Software.spark_nlp.install()
    print(f'Tried to install {len(install_results)} products:')
    for installed_software, result in install_results.items():
        if installed_software.check_installed():
            print(f'{installed_software.logo}{installed_software.name} installed! ✅')
        else:
            print(f'{installed_software.logo}{installed_software.name} not installed! ❌')

    # TODO need flag wether to upgrade Spark NLP to latest or not
