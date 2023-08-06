# -*- coding:utf-8 -*-

import os
import tempfile

ENVIRONMENT_VARIABLE_TEMP = 'PYTHON_DVS_TEMP'


def __on_callback():  # type: () -> str
    if ENVIRONMENT_VARIABLE_TEMP in os.environ:
        dvs_temp = os.getenv(ENVIRONMENT_VARIABLE_TEMP, None)
    else:
        dvs_temp = tempfile.mkdtemp(prefix='dvs-execute-')
    # if isinstance(dvs_temp, tuple) and not os.path.exists(dvs_temp[1]):
    #     os.makedirs(dvs_temp[1])
    return dvs_temp


DVS_TEMP = __on_callback
