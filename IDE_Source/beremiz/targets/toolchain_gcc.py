#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Beremiz, a Integrated Development Environment for
# programming IEC 61131-3 automates supporting plcopen standard and CanFestival.
#
# Copyright (C) 2007: Edouard TISSERANT and Laurent BESSARD
# Copyright (C) 2017: Paul Beltyukov
#
# See COPYING file for copyrights details.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os
import re
import operator
from util.ProcessLogger import ProcessLogger
import hashlib

includes_re = re.compile('\s*#include\s*["<]([^">]*)[">].*')

toolchain_dir  = os.path.dirname(os.path.realpath(__file__))
base_dir       = os.path.join(os.path.join(toolchain_dir, ".."), "..")


class toolchain_gcc():
    """
    This abstract class contains GCC specific code.
    It cannot be used as this and should be inherited in a target specific
    class such as target_linux or target_win32
    """
    def __init__(self, CTRInstance):
        self.CTRInstance = CTRInstance
        self.buildpath = None
        self.SetBuildPath(self.CTRInstance._getBuildPath())

    def getBuilderCFLAGS(self):
        """
        Returns list of builder specific CFLAGS
        """
        return [self.CTRInstance.GetTarget().getcontent().getCFLAGS()]

    def getBuilderLDFLAGS(self):
        """
        Returns list of builder specific LDFLAGS
        """
        return self.CTRInstance.LDFLAGS + \
            [self.CTRInstance.GetTarget().getcontent().getLDFLAGS()]

    def getCompiler(self):
        """
        Returns compiler
        """
        """
        if os.name in ("nt", "ce"):
	    prefix_dir    = os.path.join(os.path.join(base_dir, "mingw"), "bin")
            self.toolchain_prefix = prefix_dir + "\\gcc"
        else:
            self.toolchain_prefix = "arm-none-eabi-"
        return self.toolchain_prefix
        """


        return self.CTRInstance.GetTarget().getcontent().getCompiler()

    def getLinker(self):
        """
        Returns linker
        """
        """
        if os.name in ("nt", "ce"):
	    prefix_dir    = os.path.join(os.path.join(base_dir, "mingw"), "bin")
            self.toolchain_prefix = prefix_dir + "\\gcc"
        else:
            self.toolchain_prefix = "arm-none-eabi-"
        return self.toolchain_prefix
        """
        return self.CTRInstance.GetTarget().getcontent().getLinker()


    def GetBinaryCode(self):
        try:
            return open(self.exe_path, "rb").read()
        except Exception, e:
            return None

    def _GetMD5FileName(self):
        return os.path.join(self.buildpath, "lastbuildPLC.md5")

    def ResetBinaryCodeMD5(self):
        self.md5key = None
        try:
            os.remove(self._GetMD5FileName())
        except Exception, e:
            pass

    def GetBinaryCodeMD5(self):
        if self.md5key is not None:
            return self.md5key
        else:
            try:
                return open(self._GetMD5FileName(), "r").read()
            except Exception, e:
                return None

    def SetBuildPath(self, buildpath):
        if self.buildpath != buildpath:
            self.buildpath = buildpath
            self.exe = self.CTRInstance.GetProjectName() + self.extension
            self.exe_path = os.path.join(self.buildpath, self.exe)
            self.md5key = None
            self.srcmd5 = {}

    def append_cfile_deps(self, src, deps):
        for l in src.splitlines():
            res = includes_re.match(l)
            if res is not None:
                depfn = res.groups()[0]
                if os.path.exists(os.path.join(self.buildpath, depfn)):
                    deps.append(depfn)

    def concat_deps(self, bn):
        # read source
        src = open(os.path.join(self.buildpath, bn), "r").read()
        # update direct dependencies
        deps = []
        self.append_cfile_deps(src, deps)
        # recurse through deps
        # TODO detect cicular deps.
        return reduce(operator.concat, map(self.concat_deps, deps), src)

    def check_and_update_hash_and_deps(self, bn):
        # Get latest computed hash and deps
        oldhash, deps = self.srcmd5.get(bn, (None, []))
        # read source
        src = open(os.path.join(self.buildpath, bn)).read()
        # compute new hash
        newhash = hashlib.md5(src).hexdigest()
        # compare
        match = (oldhash == newhash)
        if not match:
            # file have changed
            # update direct dependencies
            deps = []
            self.append_cfile_deps(src, deps)
            # store that hashand deps
            self.srcmd5[bn] = (newhash, deps)
        # recurse through deps
        # TODO detect cicular deps.
        return reduce(operator.and_, map(self.check_and_update_hash_and_deps, deps), match)

    def calc_source_md5(self):
        wholesrcdata = ""
        for Location, CFilesAndCFLAGS, DoCalls in self.CTRInstance.LocationCFilesAndCFLAGS:
            # Get CFiles list to give it to makefile
            for CFile, CFLAGS in CFilesAndCFLAGS:
                CFileName = os.path.basename(CFile)
                wholesrcdata += self.concat_deps(CFileName)
        return hashlib.md5(wholesrcdata).hexdigest()

    def calc_md5(self):
        return hashlib.md5(self.GetBinaryCode()).hexdigest()

    def build(self):
        # Retrieve compiler and linker
        self.compiler = self.getCompiler()
        self.linker = self.getLinker()

        Builder_CFLAGS = ' '.join(self.getBuilderCFLAGS())

        # ----------------- GENERATE OBJECT FILES ------------------------
        obns = []
        objs = []
        relink = self.GetBinaryCode() is None
        for Location, CFilesAndCFLAGS, DoCalls in self.CTRInstance.LocationCFilesAndCFLAGS:
            if CFilesAndCFLAGS:
                if Location:
                    self.CTRInstance.logger.write(".".join(map(str, Location))+" :\n")
                else:
                    self.CTRInstance.logger.write(_("PLC :\n"))

            for CFile, CFLAGS in CFilesAndCFLAGS:
                if CFile.endswith(".c"):
                    bn = os.path.basename(CFile)
                    obn = os.path.splitext(bn)[0]+".o"
                    objectfilename = os.path.splitext(CFile)[0]+".o"

                    match = self.check_and_update_hash_and_deps(bn)

                    if match:
                        self.CTRInstance.logger.write("   [pass]  "+bn+" -> "+obn+"\n")
                    else:
                        relink = True

                        self.CTRInstance.logger.write("   [CC]  "+bn+" -> "+obn+"\n")

                        status, result, err_result = ProcessLogger(
                            self.CTRInstance.logger,
                            "\"%s\" -c \"%s\" -o \"%s\" %s %s" %
                            (self.compiler, CFile, objectfilename, Builder_CFLAGS, CFLAGS)
                        ).spin()

                        if status:
                            self.srcmd5.pop(bn)
                            self.CTRInstance.logger.write_error(_("C compilation of %s failed.\n") % bn)
                            return False
                    obns.append(obn)
                    objs.append(objectfilename)
                elif CFile.endswith(".o"):
                    obns.append(os.path.basename(CFile))
                    objs.append(CFile)

        # ---------------- GENERATE OUTPUT FILE --------------------------
        # Link all the object files into one binary file
        self.CTRInstance.logger.write(_("Linking :\n"))
        if relink:
            objstring = []

            # Generate list .o files
            listobjstring = '"' + '"  "'.join(objs) + '"'

            ALLldflags = ' '.join(self.getBuilderLDFLAGS())

            self.CTRInstance.logger.write("   [CC]  " + ' '.join(obns)+" -> " + self.exe + "\n")

            status, result, err_result = ProcessLogger(
                self.CTRInstance.logger,
                "\"%s\" %s -o \"%s\" %s" %
                (self.linker,
                 listobjstring,
                 self.exe_path,
                 ALLldflags)
            ).spin()

            if status:
                return False

        else:
            self.CTRInstance.logger.write("   [pass]  " + ' '.join(obns)+" -> " + self.exe + "\n")

        # Calculate md5 key and get data for the new created PLC
        self.md5key = self.calc_md5()

        # Store new PLC filename based on md5 key
        f = open(self._GetMD5FileName(), "w")
        f.write(self.md5key)
        f.close()

        return True
