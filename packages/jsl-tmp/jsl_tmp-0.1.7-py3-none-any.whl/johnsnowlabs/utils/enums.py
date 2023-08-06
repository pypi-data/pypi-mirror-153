from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from functools import partial
from typing import Optional, Union
from abc import ABC, abstractmethod

import requests


class InstallType(str): pass


class Secret(str): pass


class Hardware(str): pass


class ProductPlatform(Enum):
    # TODO MAYBE DROP
    java = 'java'
    spark = 'spark'
    python = 'python'


class JslLibSparkVersionIdentifier(str):
    """Str representation of Spark Versions for a specific JSL libraries.
    Not all libraries are reffering to Spark versions in same fashion, so we use this."""
    pass


class LibVersionIdentifier(str):
    """Representation of a specific library version"""
    pass


class SparkVersions(Enum):
    v234 = LibVersionIdentifier('spark234')


class ScalaVersion(Enum):
    scala11 = 'scala11'
    scala12 = 'scala12'


class HardwareTarget(Enum):
    gpu = Hardware('gpu')
    # cpu must be '' because its not present in urls
    cpu = Hardware('')


class PyInstallTypes(Enum):
    # TODO these names are used as public params which are hard to access for users
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
    spark24 = JslLibSparkVersionIdentifier('24')
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


class LatestCompatibleProductVersion(Enum):
    healthcare = LibVersionIdentifier('healthcare')
    spark_nlp = LibVersionIdentifier('3.4.4')
    ocr = LibVersionIdentifier('Spark OCR')
    finance = LibVersionIdentifier('finance')
    nlp_display = LibVersionIdentifier('nlp_display')
    nlu = LibVersionIdentifier('nlu')
    pyspark = LibVersionIdentifier('3.2.1')
    spark = LibVersionIdentifier('3.0.0')
    java = LibVersionIdentifier('java')
    python = LibVersionIdentifier('python')


class ProductName(Enum):
    healthcare = 'healthcare'
    spark_nlp = 'spark-nlp'
    ocr = 'Spark OCR'
    finance = 'finance'
    nlp_display = 'nlp_display'
    nlu = 'nlu'
    pyspark = 'pyspark'
    spark = 'spark'
    java = 'java'
    python = 'python'


class ProductLogo(Enum):
    healthcare = '🩺'  # 🏥  💊 ❤️ ‍🩹 ‍⚕️💉
    spark_nlp = '🚀'
    ocr = '🕶'  # 👁️  🤖 🦾🦿 🥽 👀 🕶 🥽 ⚕
    finance = '🤑'  # 🤑🏦💲💳💰💸💵💴💶💷
    nlp_display = '🎨'
    nlu = '🤖'
    pyspark = '🐍+⚡'
    spark = '⚡'
    java = '☕'
    python = '🐍'  # 🐉


class ProductSlogan(Enum):
    healthcare = 'Cure the planet with NLP!'
    spark_nlp = 'Lighting Fast NLP Engine!'
    ocr = 'Empower your NLP with a set of eyes'  # 👁️  🤖 🦾🦿 🥽 👀 🕶 🥽 ⚕
    pyspark = 'The big data Engine'
    nlu = '1 line to conquer NLP'
    finance = 'NLP for money'
    nlp_display = 'Visualize your NLP!'
    spark = '⚡'
    java = '☕'
    python = '🐍'  # 🐉


@dataclass
class InstalledProductInfo:
    """Representation of a JSL product install. Version is None if not installed  """
    product: ProductName
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
class JslSuiteStatus:
    """Representation and install status of all JSL products and its dependencies.
    Version attribute of InstalledProductInfo is None for uninstalled products
    """
    spark_nlp_info: Optional[InstalledProductInfo] = None
    spark_hc_info: Optional[InstalledProductInfo] = None
    spark_ocr_info: Optional[InstalledProductInfo] = None
    nlu_info: Optional[InstalledProductInfo] = None
    sparknlp_display_info: Optional[InstalledProductInfo] = None
    pyspark_info: Optional[InstalledProductInfo] = None
