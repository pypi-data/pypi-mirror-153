import sys
from typing import Dict, Optional, Union, List
from johnsnowlabs import hc, nlp, ocr
# TODO all these imports below should be INSIDE of methods!
from johnsnowlabs.abstract_base.lib_resolvers import try_import_lib, is_spark_version_env
from johnsnowlabs.abstract_base.software_product import AbstractSoftwareProduct
from johnsnowlabs.auto_install.offline_install import print_all_dependency_urls_for_secret
from johnsnowlabs.auto_install.softwares import SparkNlpSoftware, Software
from johnsnowlabs.utils.enums import ProductName, PyInstallTypes
from johnsnowlabs.utils.env_utils import is_running_in_databricks
from johnsnowlabs.utils.jsl_secrets import JslSecrets
from johnsnowlabs.utils.sparksession_utils import authenticate_enviroment_HC, authenticate_enviroment_OCR, retry
from johnsnowlabs.auto_install.install_software import check_and_install_dependencies


def install(
        access_token: Optional[str] = None,
        email: Optional[str] = None,
        passw: Optional[str] = None,
        license_number: int = 0,
        secrets_file: Optional[str] = None,
        product: Optional[ProductName] = None,
        python_exec_path: str = sys.executable,
        hc_license: Optional[str] = None,
        hc_secret: Optional[str] = None,
        ocr_secret: Optional[str] = None,
        ocr_license: Optional[str] = None,
        aws_access_key: Optional[str] = None,
        aws_key_id: Optional[str] = None,
        install_optional: bool = True,
        install_licensed: bool = True,
        sparknlp_to_latest: bool = True,
        offline: bool = False,
        gpu: bool = False,
        py_install_type=PyInstallTypes.wheel):
    secrets: JslSecrets = JslSecrets.build_or_try_find_secrets(access_token, email, passw,license_number,
                                                               secrets_file, hc_license, hc_secret,
                                                               ocr_secret, ocr_license, aws_access_key,
                                                               aws_key_id, True)

    if not product:
        # Default product is NLU
        # With default args it will install everything
        # since NLU depends on everything
        product = ProductName.nlu
    elif product == ProductName.spark_nlp.value:
        product = Software.spark_nlp
    elif product == ProductName.nlu.value:
        product = Software.nlu
    elif product == ProductName.healthcare.value:
        product = Software.spark_hc
    elif product == ProductName.ocr.value:
        product = Software.spark_ocr
    elif product == ProductName.nlp_display.value:
        product = Software.sparknlp_display
    elif product == ProductName.pyspark.value:
        product = Software.pyspark
    elif not offline:
        bck = "\n"
        raise Exception(f'Invalid install target: {product}'
                        f' please specify on of:\n{bck.join([n.value for n in ProductName])}')

    if offline:
        print_all_dependency_urls_for_secret(secrets, gpu, py_install_type)
    else:
        check_and_install_dependencies(product=product, secrets=secrets, install_optional=install_optional,
                                       install_licensed=install_licensed, sparknlp_to_latest=sparknlp_to_latest,
                                       python_exec_path=python_exec_path)

    # TODO if databricks, check configs are correctly set!


def start(
        access_token: Optional[str] = None,
        email: Optional[str] = None,
        passw: Optional[str] = None,
        license_number: int = 0,
        secrets_file: Optional[str] = None,
        hc_license: Optional[str] = None,
        hc_secret: Optional[str] = None,
        ocr_secret: Optional[str] = None,
        ocr_license: Optional[str] = None,
        aws_access_key: Optional[str] = None,
        aws_key_id: Optional[str] = None,
        spark_conf: Dict[str, str] = None,
        master_url: str = 'local[*]',
        jar_paths: List[str] = None,
        exclude_spark_nlp: bool = False,
        exclude_spark_nlp_healthcare: bool = False,
        exclude_spark_ocr: bool = False,
        gpu=False, ) -> 'pyspark.sql.SparkSession':
    """
    Start a SparkSession with JSL-Products of your choice and authenticates the environment to use licensed software
    based on supplied secrets and licenses.
    By default all libraries for which valid credentials are supplied will be loaded into the Spark Sessions JVM.
    You exclude any of them from being loaded by using the exclude parameters.

    If secrets_file and all license and secret parameters are None,
    the following strategy is applied to find secret and license information on this machine:

    1. The pattern os.getcwd()/*.json will be globed for valid JSL-Secret json files
     and substituted for the secrets_file parameter

    2. The pattern /content/*.json will be globed by default and searched for valid JSL-Secret json files
     and substituted for the secrets_file parameter

    3. Environment is checked for variable names match up with a secret name

    4. /~/.johnsnowlabs will be searched for default credentials file generated from CLI-login (TODO implement)

    5. Supply Email+password or Token to start a session?



    :param secrets_file: A file
    :param hc_license:
    :param hc_secret:
    :param ocr_secret:
    :param ocr_license:
    :param aws_access_key:
    :param aws_key_id:
    :param spark_conf:
    :param master_url:
    :param exclude_spark_nlp:
    :param exclude_spark_nlp_healthcare:
    :param exclude_spark_ocr:
    :param gpu:
    :return:
    """
    from pyspark.sql import SparkSession

    if '_instantiatedSession' in dir(SparkSession) and SparkSession._instantiatedSession is not None:
        print('Warning::Spark Session already created, some configs may not take.')
    from johnsnowlabs.abstract_base.lib_resolvers import NlpLibResolver, HcLibResolver, OcrLibResolver

    secrets: Union[JslSecrets, bool] = JslSecrets.build_or_try_find_secrets(access_token, email, passw, license_number,
                                                                            secrets_file,
                                                                            hc_license,
                                                                            hc_secret,
                                                                            ocr_secret, ocr_license,
                                                                            aws_access_key, aws_key_id)

    # Collect all Jar URLs for the SparkSession
    jars = []

    if jar_paths:
        jars += jar_paths

    if not exclude_spark_nlp:
        if gpu:
            jars.append(NlpLibResolver.get_gpu_jar_urls().url)
        else:
            jars.append(NlpLibResolver.get_cpu_jar_urls().url)
    if secrets:
        # Lib version is resolved from the lib string
        if secrets.HC_SECRET and not exclude_spark_nlp_healthcare:
            jars.append(HcLibResolver.get_cpu_jar_urls(secrets.HC_SECRET).url)
            authenticate_enviroment_HC(secrets.HC_LICENSE, secrets.AWS_ACCESS_KEY_ID, secrets.AWS_SECRET_ACCESS_KEY)

        if secrets.OCR_SECRET and not exclude_spark_ocr:
            jars.append(OcrLibResolver.get_cpu_jar_urls(secrets.OCR_SECRET).url)
            authenticate_enviroment_OCR(secrets.OCR_LICENSE, secrets.AWS_ACCESS_KEY_ID, secrets.AWS_SECRET_ACCESS_KEY)

    builder = SparkSession.builder \
        .appName("John Snow Labs") \
        .master(master_url)

    default_conf = {"spark.driver.memory": "32G",
                    "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
                    "spark.kryoserializer.buffer.max": "2000M",
                    'spark.driver.maxResultSize': '2000M',
                    'spark.jars': ','.join(jars), }

    if secrets and secrets.OCR_SECRET:
        # is_spark_version_env('32')
        default_conf["spark.sql.optimizer.expression.nestedPruning.enabled"] = "false"
        default_conf["spark.sql.optimizer.nestedSchemaPruning.enabled"] = "false"
        default_conf["spark.sql.legacy.allowUntypedScalaUDF"] = "true"
        default_conf["spark.sql.repl.eagerEval.enabled"] = "true"

    for k, v in default_conf.items():
        builder.config(str(k), str(v))
    if spark_conf:
        for k, v in spark_conf.items():
            builder.config(str(k), str(v))

    spark = builder.getOrCreate()

    # TODO what is this for?? We need bo th??
    if secrets and secrets.HC_SECRET:
        spark._jvm.com.johnsnowlabs.util.start.registerListenerAndStartRefresh()
    if secrets and secrets.OCR_SECRET:
        retry(spark._jvm.com.johnsnowlabs.util.OcrStart.registerListenerAndStartRefresh)
    return spark
