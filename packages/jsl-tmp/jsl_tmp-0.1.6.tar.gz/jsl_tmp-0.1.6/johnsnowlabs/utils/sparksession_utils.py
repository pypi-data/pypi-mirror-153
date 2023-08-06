import os


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


def retry(fun, max_tries=10):
    for i in range(max_tries):
        try:
            time.sleep(0.3)
            fun()
            break
        except Exception:
            continue
