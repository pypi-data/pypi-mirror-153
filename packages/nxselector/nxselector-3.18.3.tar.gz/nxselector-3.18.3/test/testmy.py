#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2012-2018 DESY, Jan Kotanski <jkotan@mail.desy.de>
#
#    nexdatas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nexdatas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nexdatas.  If not, see <http://www.gnu.org/licenses/>.
# \package test nexdatas
# \file XMLConfiguratorTest.py
# unittests for field Tags running Tango Server
#
# import unittest
# import os
import sys
# import random
# import struct
# import binascii
# # import time
# # import threading
# # import PyTango
# # import json
# import nxsselector
# from nxsselector import Selector

import taurus.qt.qtgui.application
Application = taurus.qt.qtgui.application.TaurusApplication

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


if sys.version_info > (3,):
    unicode = str
    long = int


# comp_available tesQt
# \brief It tests XMLConfigurator
def testhelp():

    helps = ['--help', '-h']
    for hl in helps:
        print(hl)
        old_argv = sys.argv
        sys.argv = ['nxselector', hl]
        try:
            print("WW")
            app = Application(
                sys.argv,
                # cmd_line_parser=parser,
                app_name="NXS Component Selector",
                #            app_version=__version__,
                org_domain="desy.de",
                org_name="DESY")
            print("WW2")
            # Selector.main()
        except SystemExit as e:
            print("EXIT")
            print(e)
        except Exception as e:
            print("EXCEP")
            print(e)

        



if __name__ == '__main__':
    testhelp()
