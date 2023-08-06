from typing import Optional, List, Tuple
import johnsnowlabs.utils.settings
from johnsnowlabs.utils.enums import InstalledProductInfo, JslSuite, Products, LibVersionIdentifier, PyInstallTypes, \
    ProductLogo, SparkVersions
import importlib

from johnsnowlabs.utils.json_credentials_parser import JslSecrets
from johnsnowlabs.utils.lib_resolvers import OcrLibResolver, NlpLibResolver, HcLibResolver


def list_all_install_urls_for_secret(secrets: JslSecrets, gpu=False, py_install_type=PyInstallTypes.wheel) -> Tuple[
    List[str], List[str]]:
    """
    Get URL for every dependency to which the secrets have access to with respect to CURRENT pyspark install.
    If no pyspark is installed, this fails because we need to know pyspark version to generate correct URL
    :param secrets:
    :param gpu: True for GPU Jars, otherwise CPU Jars
    :param py_install_type: PyInstallTypes.wheel or PyInstallTypes.tar
    :return: list of pre-formatted message arrays java_dependencies, py_dependencies
    """
    messages = []
    java_dependencies = []
    py_dependencies = []
    if gpu:
        java_dependencies.append(
            f'{ProductLogo.spark_nlp.value}{ProductLogo.java.value}  Spark NLP GPU Java Jar:'
            f' {NlpLibResolver.get_gpu_jar_urls(jsl_lib_version=secrets.NLP_VERSION, ).url}')
    else:
        java_dependencies.append(
            f'{ProductLogo.spark_nlp.value}{ProductLogo.java.value}  Spark NLP CPU Java Jar:'
            f' {NlpLibResolver.get_cpu_jar_urls(jsl_lib_version=secrets.NLP_VERSION, ).url}')

    if py_install_type == PyInstallTypes.wheel:
        py_dependencies.append(
            f'{ProductLogo.spark_nlp.value}{ProductLogo.python.value} Spark NLP for Python Wheel: '
            f'{NlpLibResolver.get_py_urls(jsl_lib_version=secrets.NLP_VERSION, install_type=PyInstallTypes.wheel).url}')
    else:
        py_dependencies.append(
            f'{ProductLogo.spark_nlp.value}{ProductLogo.python.value} Spark NLP for Python Tar:'
            f' {NlpLibResolver.get_py_urls(jsl_lib_version=secrets.NLP_VERSION, install_type=PyInstallTypes.tar).url}')

    # TODO MAKE SURE SPARK IS INSTALLED BEFORE THIS!!
    # IT WILL RECCOMEND JARS BASED ON CURRENT INSTALL!
    if secrets.HC_SECRET:
        java_dependencies.append(
            f'{ProductLogo.healthcare.value}{ProductLogo.java.value}  Spark NLP for Healthcare Java Jar:'
            f' {HcLibResolver.get_cpu_jar_urls(secrets.HC_SECRET, jsl_lib_version=secrets.HC_VERSION).url}')
        if py_install_type == PyInstallTypes.wheel:
            py_dependencies.append(
                f'{ProductLogo.healthcare.value}{ProductLogo.python.value} Spark NLP for Healthcare Python Wheel:'
                f' {HcLibResolver.get_py_urls(secret=secrets.HC_SECRET, jsl_lib_version=secrets.HC_VERSION, install_type=PyInstallTypes.wheel).url}')
        else:
            py_dependencies.append(
                f'{ProductLogo.healthcare.value}{ProductLogo.python.value} Spark NLP for Healthcare Python Tar:'
                f' {HcLibResolver.get_py_urls(secret=secrets.HC_SECRET, jsl_lib_version=secrets.HC_VERSION, install_type=PyInstallTypes.tar).url}')

    if secrets.OCR_SECRET:
        java_dependencies.append(
            f'{ProductLogo.ocr.value}{ProductLogo.java.value}  Spark OCR Java Jar:'
            f' {OcrLibResolver.get_cpu_jar_urls(secrets.OCR_SECRET, jsl_lib_version=secrets.OCR_VERSION).url}')
        if py_install_type == PyInstallTypes.wheel:
            py_dependencies.append(
                f'{ProductLogo.ocr.value}{ProductLogo.python.value} Spark OCR Python Wheel:'
                f' {OcrLibResolver.get_py_urls(secret=secrets.OCR_SECRET, jsl_lib_version=secrets.OCR_VERSION, install_type=PyInstallTypes.wheel).url}')
        else:
            py_dependencies.append(
                f'{ProductLogo.ocr.value}{ProductLogo.python.value} Spark OCR Python Tar:'
                f' {OcrLibResolver.get_py_urls(secret=secrets.OCR_SECRET, jsl_lib_version=secrets.OCR_VERSION, install_type=PyInstallTypes.tar).url}')

    # TODO WHEEL/TAR links!
    print('\n'.join(java_dependencies + py_dependencies))
    return java_dependencies, py_dependencies


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


def try_import(lib):
    try:
        importlib.import_module(lib)
    except Exception as _:
        return False
    return True


def get_jsl_lib_install_data() -> JslSuite:
    """Get Install status and versio of all JSL libs and Pyspark"""
    if try_import('pyspark'):
        import pyspark
        pyspark_info = InstalledProductInfo(Products.pyspark, LibVersionIdentifier(pyspark.__version__))
    else:
        pyspark_info = InstalledProductInfo(Products.pyspark, None)

    if try_import('sparknlp'):
        import sparknlp
        spark_nlp_info = InstalledProductInfo(Products.spark_nlp, LibVersionIdentifier(sparknlp.version()))
    else:
        spark_nlp_info = InstalledProductInfo(Products.spark_nlp, None)

    if try_import('sparknlp_jsl'):
        import sparknlp_jsl
        spark_hc_info = InstalledProductInfo(Products.ocr, LibVersionIdentifier(sparknlp_jsl.version()))
    else:
        spark_hc_info = InstalledProductInfo(Products.ocr, None)

    if try_import('sparkocr'):
        import sparkocr
        spark_ocr_info = InstalledProductInfo(Products.ocr, LibVersionIdentifier(sparkocr.version()))
    else:
        spark_ocr_info = InstalledProductInfo(Products.ocr, None)

    if try_import('sparknlp_display'):
        import sparknlp_display
        nlp_display_info = InstalledProductInfo(Products.nlp_display, LibVersionIdentifier(sparknlp_display.version()))
    else:
        nlp_display_info = InstalledProductInfo(Products.nlp_display, None)

    if try_import('nlu'):
        import nlu
        nlu_info = InstalledProductInfo(Products.nlu, LibVersionIdentifier(nlu.version()))
    else:
        nlu_info = InstalledProductInfo(Products.nlu, None)

    return JslSuite(
        spark_nlp_info=spark_nlp_info,
        spark_hc_info=spark_hc_info,
        spark_ocr_info=spark_ocr_info,
        nlu_info=nlu_info,
        sparknlp_display_info=nlp_display_info,
        pyspark_info=pyspark_info, )
