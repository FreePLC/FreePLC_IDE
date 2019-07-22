#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "$Revision$"

import __builtin__
import gettext
import os
import sys

gettext.install('Cloudplcide')  # this is a dummy to prevent gettext falling down

_dist_folder = os.path.split(sys.path[0])[0]
_beremiz_folder = os.path.join(_dist_folder, "beremiz")
_mingw_folder = os.path.join(os.path.join(_dist_folder, "mingw"), "bin")

#Ensure that Beremiz things are imported before builtins and libs.
sys.path.insert(1,_beremiz_folder)
sys.path.insert(1,_mingw_folder)

from Beremiz import *

class CloudPLCIdeLauncher(BeremizIDELauncher):
    """
    PLC IDE Launcher class
    """

    def __init__(self):

        os.environ["PATH"] = _mingw_folder+";" + os.environ["PATH"]
        env_dist = os.environ
        print env_dist["PATH"]

        BeremizIDELauncher.__init__(self)
        self.cloudplc_dir = os.path.dirname(os.path.realpath(__file__))
        self.splashPath = self.Cloudpath("images", "splash.png")

        import features
        # Let's import nucleron plcconnectors
        import plcconnectors
        import connectors

        connectors.connectors.update(plcconnectors.connectors)

        # Import Nucleron yaplctargets
        import plctargets
        import targets

        targets.toolchains.update(plctargets.toolchains)
        targets.targets.update(plctargets.plctargets)

        features.libraries = [
	    ('Native', 'NativeLib.NativeLibrary')]
        '''
        yangliang del for test
        features.catalog.append(('plcconfig',
                                 _('YAPLC Configuration Node'),
                                 _('Adds template located variables'),
                                 'yaplcconfig.yaplcconfig.YAPLCNodeConfig'))
        '''

    def Cloudpath(self, *args):
        return os.path.join(self.cloudplc_dir, *args)


# This is where we start our application
if __name__ == '__main__':
    beremiz = CloudPLCIdeLauncher()
    beremiz.Start()
