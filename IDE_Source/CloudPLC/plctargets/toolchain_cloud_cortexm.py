import os, sys
from toolchain_cloud import toolchain_cloud
from toolchain_cloud import plc_rt_dir as plc_rt_dir

toolchain_dir  = os.path.dirname(os.path.realpath(__file__))
base_dir       = os.path.join(os.path.join(toolchain_dir, ".."), "..")

class toolchain_cloud_cortexm(toolchain_cloud):

    def GetBinaryCode(self):
        if os.path.exists(self.exe_path):
            command = [self.exe_path + ".bin", self.load_addr]
            return command
        else:
	    return None
