#  --------------------------------------------------------------------------------
#  Copyright (c) 2020 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2021.
#
#  DataRobot, Inc. Confidential.
#  This is proprietary source code of DataRobot, Inc. and its affiliates.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.
#
#  --------------------------------------------------------------------------------

from abc import ABC, abstractmethod


class URIFetcherBase(ABC):
    def __init__(self, prefix, base_dir):
        self._base_dir = base_dir
        self._prefix = prefix

    def get_prefix(self):
        return self._prefix

    @abstractmethod
    def fetch_artifact(self, uri):
        pass
