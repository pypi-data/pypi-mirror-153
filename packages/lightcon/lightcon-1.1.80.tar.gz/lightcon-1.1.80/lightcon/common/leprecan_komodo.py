#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# 
#--------------------------------------------------------------------------
# Copyright (c) 2021 Light Conversion, UAB
# All rights reserved.
# www.lightcon.com
#==========================================================================
from ..common.leprecan_base import LepreCanBase
from ..common.komodo import Komodo

class LepreCanKomodo(LepreCanBase):
    def __init__(self):
        self.can_service = Komodo
    