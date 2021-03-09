#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "a93fc801-051a-41ca-b436-64e026370665")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "7-_~6qwD_~bS1Q69EsIC1IgWzG1apm5dOS")
