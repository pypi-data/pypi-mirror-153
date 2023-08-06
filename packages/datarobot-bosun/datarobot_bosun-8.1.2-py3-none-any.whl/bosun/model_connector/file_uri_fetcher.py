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
import shutil
from urllib.parse import urlparse, unquote
import uuid

from bosun.model_connector.uri_fetcher_base import URIFetcherBase

logger = logging.getLogger(__name__)


class FileURIFetcher(URIFetcherBase):
    def __init__(self, base_dir):
        super().__init__("file", base_dir)

    def fetch_artifact(self, uri):
        orig_file_path = unquote(urlparse(uri).path)
        priv_file_path = os.path.join(self._base_dir,
                                      os.path.basename(orig_file_path) + "_" + str(uuid.uuid4()))
        logger.info("uri:            {}".format(uri))
        logger.info("orig_file_path: {}".format(orig_file_path))
        logger.info("priv_file_path: {}".format(priv_file_path))
        shutil.copyfile(orig_file_path, priv_file_path)
        return priv_file_path
