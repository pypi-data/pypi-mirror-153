from dataclasses import dataclass
from enum import Enum
from functools import partial
from typing import Optional, Union
from abc import ABC, abstractmethod

import requests


class InstallType(str): pass


class Secret(str): pass


class Hardware(str): pass


class JslLibSparkVersionIdentifier(str):
    """Str representation of Spark Versions for a specific JSL libraries.
    Not all libraries are reffering to Spark versions in same fashion, so we use this."""
    pass


class LibVersionIdentifier(str):
    """Representation of a specific library version"""
    pass

class SparkVersions(Enum):

    v234 = LibVersionIdentifier('spark234')



class Products(Enum):
    healthcare = 'healthcare'
    spark_nlp = 'spark-nlp'
    ocr = 'Spark OCR'
    finance = 'finance'
    nlp_display = 'nlp_display'
    nlu = 'nlu'
    pyspark = 'pyspark'

class ProductLogo(Enum):
    healthcare = '🩺' # 🏥  💊 ❤️ ‍🩹 ‍⚕️💉
    spark_nlp = '🚀'
    ocr = '👀'  # 👁️  🤖 🦾🦿
    finance = 'finance'
    nlp_display = 'nlp_display'
    nlu = '🤖'
    pyspark = '⚡'
    java = '☕'
    python = '🐍' # 🐉



class ScalaVersion(Enum):
    scala11 = 'scala11'
    scala12 = 'scala12'


class HardwareTarget(Enum):
    gpu = Hardware('gpu')
    # cpu must be '' because its not present in urls
    cpu = Hardware('')


class PyInstallTypes(Enum):
    tar = InstallType('.tar.gz')
    wheel = InstallType('-py3-none-any.whl')


class JavaInstallTypes(Enum):
    jar = InstallType('jar')


class NlpSparkVersionId(Enum):
    # Spark 3.2.x
    spark32x = JslLibSparkVersionIdentifier('-spark32')
    # Spark 3.0.x/3.1.x. Has no 'spark' in name
    spark30x_and_spark31x = JslLibSparkVersionIdentifier('')
    # 2.4.x and 2.3.x suspport dropped
    spark23 = JslLibSparkVersionIdentifier('-spark23')
    spark24 = JslLibSparkVersionIdentifier('-spark24')


class OcrSparkVersionId(Enum):
    spark23 = JslLibSparkVersionIdentifier('23')
    spark30 = JslLibSparkVersionIdentifier('30')
    spark32 = JslLibSparkVersionIdentifier('32')


class HcSparkVersionId(Enum):
    # HC jars have no scala version in name
    # Spark 3.2.x
    spark32x = JslLibSparkVersionIdentifier('-spark32')
    # Spark 3.0.x/3.1.x. Has no 'spark' in name
    spark30x_and_spark31x = JslLibSparkVersionIdentifier('')
    # 2.4.x and 2.3.x uspport dropped
    spark23 = JslLibSparkVersionIdentifier('-spark23')
    spark24 = JslLibSparkVersionIdentifier('-spark24')


@dataclass
class InstalledProductInfo:
    """Representation of a JSL product install. Version is None if not installed  """
    product: Products
    version: Optional[LibVersionIdentifier] = None


@dataclass
class UrlDependency:
    """Representation of a URL"""
    url: str
    dependency_type: str

    def validate(self):
        # Try GET on the URL and see if its valid/reachable
        return requests.head(self.url).status_code == 200


@dataclass
class JslSuite:
    """Representaton and install status of all JSL products
    version is None for uninstalled products
    """
    spark_nlp_info: Optional[InstalledProductInfo] = None
    spark_hc_info: Optional[InstalledProductInfo] = None
    spark_ocr_info: Optional[InstalledProductInfo] = None
    nlu_info: Optional[InstalledProductInfo] = None
    sparknlp_display_info: Optional[InstalledProductInfo] = None
    pyspark_info: Optional[InstalledProductInfo] = None
