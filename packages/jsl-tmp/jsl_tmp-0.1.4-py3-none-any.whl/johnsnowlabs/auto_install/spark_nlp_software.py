from enum import Enum
from typing import Optional

from johnsnowlabs.abstract_base.lib_resolvers import NlpLibResolver, HcLibResolver, OcrLibResolver
from johnsnowlabs.abstract_base.software_product import AbstractSoftwareProduct
from johnsnowlabs.utils.enums import ProductName, ProductLogo, LibVersionIdentifier, LatestCompatibleProductVersion, \
    ProductSlogan
from johnsnowlabs.utils.env_utils import try_import
from johnsnowlabs.utils.jsl_secrets import JslSecrets
from johnsnowlabs.utils.pip_utils import install_standard_pypi_lib


class PythonSoftware(AbstractSoftwareProduct):
    name = ProductName.python.value
    logo = ProductLogo.python.value
    latest_version = LatestCompatibleProductVersion.python.value


class JavaSoftware(AbstractSoftwareProduct):
    name = ProductName.java.value
    logo = ProductLogo.java.java
    latest_version = LatestCompatibleProductVersion.java.value


class SparkSoftware(AbstractSoftwareProduct):
    name = ProductName.spark.value
    logo = ProductLogo.spark.value
    hard_dependencies = {JavaSoftware}
    latest_version = LatestCompatibleProductVersion.spark.value


class PysparkSoftware(AbstractSoftwareProduct):
    # TODO needs custom install for windows! (?)
    name = ProductName.pyspark.value
    logo = ProductLogo.pyspark.value
    slogan = ProductSlogan.pyspark.value
    hard_dependencies = {PythonSoftware}
    latest_version = LatestCompatibleProductVersion.pyspark.value
    py_module_name = 'pyspark'
    pypi_name = 'pyspark'


class SparkNlpSoftware(AbstractSoftwareProduct):
    name = ProductName.spark_nlp.value
    logo = ProductLogo.spark_nlp.value
    slogan = ProductSlogan.spark_nlp.value
    hard_dependencies = {SparkSoftware, PysparkSoftware}
    latest_version = LatestCompatibleProductVersion.spark_nlp.value
    jsl_url_resolver = NlpLibResolver
    py_module_name = 'sparknlp'
    pypi_name = 'spark-nlp'


class SparkHcSoftware(AbstractSoftwareProduct):
    name = ProductName.healthcare.value
    logo = ProductLogo.healthcare.value
    slogan = ProductSlogan.healthcare.value
    hard_dependencies = {SparkNlpSoftware}
    latest_version = LatestCompatibleProductVersion.healthcare.value
    jsl_url_resolver = HcLibResolver
    # todo doublecheck
    py_module_name = 'sparknlp_jsl'
    pypi_name = 'spark-nlp-jsl'
    licensed = True


class SparkOcrSoftware(AbstractSoftwareProduct):
    name = ProductName.ocr.value
    logo = ProductLogo.ocr.value
    slogan = ProductSlogan.ocr.value
    # TODO sparknlp/healtcare optional or hard?
    hard_dependencies = {SparkSoftware, PysparkSoftware}
    optional_dependencies = {SparkNlpSoftware, SparkHcSoftware}
    latest_version = LatestCompatibleProductVersion.ocr.value
    jsl_url_resolver = OcrLibResolver
    py_module_name = 'sparkocr'  #
    pypi_name = 'spark-ocr'
    licensed = True


class NlpDisplaySoftware(AbstractSoftwareProduct):
    name = ProductName.nlp_display.value
    logo = ProductLogo.nlp_display.value
    slogan = ProductSlogan.nlp_display.value
    hard_dependencies = {SparkSoftware}
    licensed_dependencies = {SparkHcSoftware}
    latest_version = LatestCompatibleProductVersion.nlp_display.value
    py_module_name = 'sparknlp_display'
    pypi_name = 'spark-nlp-display'


class NluSoftware(AbstractSoftwareProduct):
    name = ProductName.nlu.value
    logo = ProductLogo.nlu.value
    slogan = ProductSlogan.nlu.value

    hard_dependencies = {SparkNlpSoftware}
    licensed_dependencies = {SparkHcSoftware, SparkOcrSoftware}
    optional_dependencies = {NlpDisplaySoftware}  # Todo streamlit,sklearn,plotly, nlp-display
    latest_version = LatestCompatibleProductVersion.nlu.value
    py_module_name = 'nlu'
    pypi_name = 'nlu'

    @classmethod
    def health_check(cls) -> bool:
        import nlu
        try:
            pipe = nlu.load('sentiment')
            df = pipe.predict('I love peanut butter and jelly!')
            for c in df.columns:
                print(df[c])
        except Exception as err:
            print(f'Failure testing nlu. Err = {err}')
            return False
        return True


class Software:
    """Accessor to all classes that implement AbstractSoftwareProduct """
    spark_nlp = SparkNlpSoftware
    spark_hc = SparkHcSoftware
    spark_ocr = SparkOcrSoftware
    nlu = NluSoftware
    sparknlp_display = NlpDisplaySoftware
    pyspark = PysparkSoftware
    python = PythonSoftware
    java = JavaSoftware
    spark = SparkSoftware
