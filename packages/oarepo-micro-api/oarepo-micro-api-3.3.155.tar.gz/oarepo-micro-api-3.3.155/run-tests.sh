#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET.
#
# OARepo Micro API is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

pydocstyle oarepo_micro_api tests && \
isort --check-only --df oarepo_micro_api && \
check-manifest --ignore ".travis-*" && \
python setup.py test
