from typing import Optional, List, Tuple
from johnsnowlabs.utils.enums import InstalledProductInfo, JslSuiteStatus, ProductName, LibVersionIdentifier, PyInstallTypes, \
    ProductLogo, SparkVersions

from johnsnowlabs.utils.env_utils import try_import
from johnsnowlabs.utils.jsl_secrets import JslSecrets
from johnsnowlabs.abstract_base.lib_resolvers import OcrLibResolver, NlpLibResolver, HcLibResolver


def get_spark_version_from_cli():
    # Get spark version from CLI
    spark_version = None
    print(f'You need to specify a Spark version, pick one of:{[v for v in SparkVersions]} ')
    # TODO Default to 'latest' !
    while spark_version not in SparkVersions:
        input(f"Please select a Pyspark version")
    return spark_version


def install_offline(secrets_path: Optional[str] = None):
    if not try_import('pyspark'):
        print(f"Could not detect pyspark version.")
        spark_version = get_spark_version_from_cli()
    else:
        # get spark from local and inform user about the version we use
        # TODO need list of valid Pyspark Version Identifiers
        pass
    if not secrets_path:
        # TODO check if JSL_HOME exists and if we have stuff there
        secrets_path = input(f'Please enter path to your secrets')

    secrets = JslSecrets.from_json_file_path(secrets_path)
    list_all_install_urls_for_secret(secrets, spark_version)
    pass


def verify_dependencies():
    # 0. Check java is installed, i.e. JAVA_HOME

    # 1. Check Spark Installed

    # 2. Check Spark Home/etc is set

    # 3. Check Spark Version is supported

    # 4. Python version chekcs

    # ?

    pass


def get_jsl_lib_install_data() -> JslSuiteStatus:
    """Get Install status and versio of all JSL libs and Pyspark"""
    if try_import('pyspark'):
        import pyspark
        pyspark_info = InstalledProductInfo(ProductName.pyspark, LibVersionIdentifier(pyspark.__version__))
    else:
        pyspark_info = InstalledProductInfo(ProductName.pyspark, None)

    if try_import('sparknlp'):
        import sparknlp
        spark_nlp_info = InstalledProductInfo(ProductName.spark_nlp, LibVersionIdentifier(sparknlp.version()))
    else:
        spark_nlp_info = InstalledProductInfo(ProductName.spark_nlp, None)

    if try_import('sparknlp_jsl'):
        import sparknlp_jsl
        spark_hc_info = InstalledProductInfo(ProductName.ocr, LibVersionIdentifier(sparknlp_jsl.version()))
    else:
        spark_hc_info = InstalledProductInfo(ProductName.ocr, None)

    if try_import('sparkocr'):
        import sparkocr
        spark_ocr_info = InstalledProductInfo(ProductName.ocr, LibVersionIdentifier(sparkocr.version()))
    else:
        spark_ocr_info = InstalledProductInfo(ProductName.ocr, None)

    if try_import('sparknlp_display'):
        import sparknlp_display
        nlp_display_info = InstalledProductInfo(ProductName.nlp_display,
                                                LibVersionIdentifier(sparknlp_display.version()))
    else:
        nlp_display_info = InstalledProductInfo(ProductName.nlp_display, None)

    if try_import('nlu'):
        import nlu
        nlu_info = InstalledProductInfo(ProductName.nlu, LibVersionIdentifier(nlu.version()))
    else:
        nlu_info = InstalledProductInfo(ProductName.nlu, None)

    return JslSuiteStatus(
        spark_nlp_info=spark_nlp_info,
        spark_hc_info=spark_hc_info,
        spark_ocr_info=spark_ocr_info,
        nlu_info=nlu_info,
        sparknlp_display_info=nlp_display_info,
        pyspark_info=pyspark_info, )
