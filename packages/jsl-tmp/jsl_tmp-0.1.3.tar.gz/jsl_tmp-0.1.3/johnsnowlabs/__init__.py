import os
from typing import Dict
from johnsnowlabs import hc, nlp, ocr
from johnsnowlabs.abstract_base.lib_resolvers import try_import_lib, is_spark_version_env

import time


def retry(fun, max_tries=10):
    for i in range(max_tries):
        try:
            time.sleep(0.3)
            fun()
            break
        except Exception:
            continue


if not try_import_lib('pyspark', print_failure=True):
    print('Fixing Pyspark Install... TOOD')

if try_import_lib('nlu', print_failure=True):
    import nlu

if try_import_lib('sparknlp', print_failure=True):
    from sparknlp.annotator import *
    from sparknlp.base import *


def start(nlp=True, hc=False, ocr=False, gpu=False, hc_secret=None, ocr_secret=None,
          hc_license=None,
          ocr_license=None,
          aws_access_key=None,
          aws_key_id=None,
          spark_conf: Dict[str, str] = None,
          master_url: str = 'local[*]',
          secrets_file: str = None,
          #          jar_folder=None,
          ):
    from pyspark.sql import SparkSession

    if '_instantiatedSession' in dir(SparkSession) and SparkSession._instantiatedSession is not None:
        print('Warning::Spark Session already created, some configs may not take.')
    from johnsnowlabs.abstract_base.lib_resolvers import NlpLibResolver, HcLibResolver, OcrLibResolver
    if secrets_file:
        from johnsnowlabs.utils.jsl_secrets import JslSecrets
        secrets = JslSecrets.from_json_file_path(secrets_file)
        hc_license = secrets.HC_LICENSE
        ocr_license = secrets.OCR_LICENSE
        aws_access_key = secrets.AWS_SECRET_ACCESS_KEY
        aws_key_id = secrets.AWS_ACCESS_KEY_ID

    jars = []
    if nlp:
        if gpu:
            jars.append(NlpLibResolver.get_gpu_jar_urls().url)
        else:
            jars.append(NlpLibResolver.get_cpu_jar_urls().url)
    if hc:
        jars.append(HcLibResolver.get_cpu_jar_urls(hc_secret).url)
    if ocr:
        jars.append(OcrLibResolver.get_cpu_jar_urls(ocr_secret).url)

    builder = SparkSession.builder \
        .appName("John Snow Labs") \
        .master(master_url)

    default_conf = {"spark.driver.memory": "32G",
                    "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
                    "spark.kryoserializer.buffer.max": "2000M",
                    'spark.driver.maxResultSize': '2000M',
                    'spark.jars': ','.join(jars),
                    }

    if ocr:  # is_spark_version_env('32') and
        default_conf["spark.sql.optimizer.expression.nestedPruning.enabled"] = "false"
        default_conf["spark.sql.optimizer.nestedSchemaPruning.enabled"] = "false"
        default_conf["spark.sql.legacy.allowUntypedScalaUDF"] = "true"
        default_conf["spark.sql.repl.eagerEval.enabled"] = "true"

    for k, v in default_conf.items():
        builder.config(str(k), str(v))
    if spark_conf:
        for k, v in spark_conf.items():
            builder.config(str(k), str(v))

    # WTF is dis for?
    if hc:
        authenticate_enviroment_HC(hc_license, aws_key_id, aws_access_key)
    if ocr:
        authenticate_enviroment_OCR(ocr_license, aws_key_id, aws_access_key)
    spark = builder.getOrCreate()

    # if hc:
    #     spark._jvm.com.johnsnowlabs.util.start.registerListenerAndStartRefresh()
    if ocr:
        retry(spark._jvm.com.johnsnowlabs.util.OcrStart.registerListenerAndStartRefresh)
    return spark


def authenticate_enviroment_HC(SPARK_NLP_LICENSE, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY):
    """Set Secret environ variables for Spark Context"""
    os.environ['SPARK_NLP_LICENSE'] = SPARK_NLP_LICENSE
    os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY


def authenticate_enviroment_OCR(SPARK_OCR_LICENSE, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY):
    """Set Secret environ variables for Spark Context"""
    os.environ['SPARK_OCR_LICENSE'] = SPARK_OCR_LICENSE
    os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY


def authenticate_enviroment_HC_and_OCR(SPARK_NLP_LICENSE, SPARK_OCR_LICENSE, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY):
    """Set Secret environ variables for Spark Context"""
    authenticate_enviroment_HC(SPARK_NLP_LICENSE, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    authenticate_enviroment_OCR(SPARK_OCR_LICENSE, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

###### CLI
