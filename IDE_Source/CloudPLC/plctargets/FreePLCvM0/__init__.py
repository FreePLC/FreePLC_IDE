import os, sys
from plctargets.toolchain_cloud_cortexm import toolchain_cloud_cortexm
from plctargets.toolchain_cloud_cortexm import plc_rt_dir as plc_rt_dir

linkfile_dir = os.path.dirname(os.path.realpath(__file__))

class FreePLCvM0_target(toolchain_cloud_cortexm):
    def __init__(self, CTRInstance):

        toolchain_cloud_cortexm.__init__(self, CTRInstance)
        self.base_flags       = self.base_flags + ["-mcpu=cortex-m0plus"]
        self.dev_family       = "FreePLCvM0"
        self.load_addr        = "0x2A000"
        self.runtime_addr     = "0x29000"
        self.linker_script    = os.path.join(linkfile_dir, "FreePLCvM0-app.ld")

