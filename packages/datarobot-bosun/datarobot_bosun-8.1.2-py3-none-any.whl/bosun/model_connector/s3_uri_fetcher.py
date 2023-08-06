#  --------------------------------------------------------------------------------
#  Copyright (c) 2020 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2022.
#
#  DataRobot, Inc. Confidential.
#  This is proprietary source code of DataRobot, Inc. and its affiliates.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.
#
#  --------------------------------------------------------------------------------

import logging
import os
from urllib.parse import urlparse
import uuid

import boto3

from bosun.model_connector.uri_fetcher_base import URIFetcherBase

logger = logging.getLogger(__name__)


class S3Url(object):
    """
    >>> s = S3Url("s3://bucket/hello/world")
    >>> s.bucket
    'bucket'
    >>> s.key
    'hello/world'
    >>> s.url
    's3://bucket/hello/world'

    >>> s = S3Url("s3://bucket/hello/world?qwe1=3#ddd")
    >>> s.bucket
    'bucket'
    >>> s.key
    'hello/world?qwe1=3#ddd'
    >>> s.url
    's3://bucket/hello/world?qwe1=3#ddd'

    >>> s = S3Url("s3://bucket/hello/world#foo?bar=2")
    >>> s.key
    'hello/world#foo?bar=2'
    >>> s.url
    's3://bucket/hello/world#foo?bar=2'
    """

    def __init__(self, url):
        self._parsed = urlparse(url, allow_fragments=False)

    @property
    def bucket(self):
        return self._parsed.netloc

    @property
    def key(self):
        if self._parsed.query:
            return self._parsed.path.lstrip("/") + "?" + self._parsed.query
        else:
            return self._parsed.path.lstrip("/")

    @property
    def url(self):
        return self._parsed.geturl()


class S3Fetcher(URIFetcherBase):
    def __init__(self, base_dir):
        super().__init__("s3", base_dir)

    def fetch_artifact(self, uri):
        client = boto3.client("s3")
        s3_url = S3Url(uri)
        file_name = os.path.join(self._base_dir,
                                 os.path.basename(s3_url.key) + "_" + str(uuid.uuid4()))
        logger.info("uri:    {}".format(uri))
        logger.info("bucket: {}".format(s3_url.bucket))
        logger.info("key:    {}".format(s3_url.key))
        logger.info("local:  {}".format(file_name))
        client.download_file(s3_url.bucket, s3_url.key, file_name)
        return file_name
