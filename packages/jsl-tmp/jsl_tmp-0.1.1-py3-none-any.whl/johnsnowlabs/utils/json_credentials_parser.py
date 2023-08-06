from dataclasses import dataclass
from enum import Enum
from functools import partial
from typing import Optional, Union
from abc import ABC, abstractmethod

import requests
import json
from johnsnowlabs.utils.enums import JslLibSparkVersionIdentifier,LibVersionIdentifier,Secret
import os
@dataclass
class JslSecrets:
    """Representation of a JSL credentials
    """
    HC_SECRET: Secret = None
    HC_LICENSE: Secret = None
    HC_VERSION: LibVersionIdentifier = None
    OCR_SECRET: Secret = None
    OCR_LICENSE: Secret = None
    OCR_VERSION: LibVersionIdentifier = None
    NLP_VERSION: LibVersionIdentifier = None
    AWS_ACCESS_KEY_ID: Secret = None
    AWS_SECRET_ACCESS_KEY: Secret = None

    @staticmethod
    def from_json_file_path(secrets_path):
        if not os.path.exists(secrets_path):
            raise FileNotFoundError(f'No file found for secrets_path={secrets_path}')
        f = open(secrets_path)
        creds = JslSecrets.from_json_dict(json.load(f))
        f.close()
        return creds

    @staticmethod
    def from_json_dict(secrets):
        hc_secret = secrets['JSL_SECRET'] if 'JSL_SECRET' in secrets else None
        if not hc_secret:
            hc_secret = secrets['SECRET'] if 'SECRET' in secrets else None
        hc_license = secrets['SPARK_NLP_LICENSE'] if 'SPARK_NLP_LICENSE' in secrets else None
        if not hc_license:
            hc_license = secrets['JSL_LICENSE'] if 'JSL_LICENSE' in secrets else None
        hc_version = secrets['JSL_VERSION'] if 'JSL_VERSION' in secrets else None
        nlp_version = secrets['PUBLIC_VERSION'] if 'PUBLIC_VERSION' in secrets else None
        aws_access_key_id = secrets['AWS_ACCESS_KEY_ID'] if 'AWS_ACCESS_KEY_ID' in secrets else None
        aws_access_key = secrets['AWS_SECRET_ACCESS_KEY'] if 'AWS_SECRET_ACCESS_KEY' in secrets else None
        ocr_license = secrets['SPARK_OCR_LICENSE'] if 'SPARK_OCR_LICENSE' in secrets else None
        ocr_secret = secrets['SPARK_OCR_SECRET'] if 'SPARK_OCR_SECRET' in secrets else None
        ocr_version = secrets['OCR_VERSION'] if 'OCR_VERSION' in secrets else None

        return JslSecrets(
            HC_SECRET=hc_secret,
            HC_LICENSE=hc_license,
            HC_VERSION=hc_version,
            OCR_SECRET=ocr_license,
            OCR_LICENSE=ocr_secret,
            OCR_VERSION=ocr_version,
            NLP_VERSION=nlp_version,
            AWS_ACCESS_KEY_ID=aws_access_key_id,
            AWS_SECRET_ACCESS_KEY=aws_access_key,
        )
