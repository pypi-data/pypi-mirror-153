from typing import Optional, List, Tuple
from johnsnowlabs.utils.enums import PyInstallTypes, ProductLogo
from johnsnowlabs.utils.jsl_secrets import JslSecrets
from johnsnowlabs.abstract_base.lib_resolvers import OcrLibResolver, NlpLibResolver, HcLibResolver


def print_all_dependency_urls_for_secret(secrets: JslSecrets, gpu=False, py_install_type=PyInstallTypes.wheel) -> Tuple[
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

    print('\n'.join(java_dependencies + py_dependencies))
    print(f'Make sure all these dependencies are installed on your Spark Driver and Worker nodes')
    return java_dependencies, py_dependencies
