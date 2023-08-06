# -*- coding: UTF-8 -*-
# Copyright 2016-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino_xl.lib.sales import Plugin, _


class Plugin(Plugin):

    extends_models = ['InvoiceItem']
