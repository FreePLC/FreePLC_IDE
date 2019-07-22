#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Beremiz, a Integrated Development Environment for
# programming IEC 61131-3 automates supporting plcopen standard and CanFestival.
#
# Copyright (C) 2007: Edouard TISSERANT and Laurent BESSARD
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

import sys
import traceback
import atexit
from twisted.internet import reactor, threads
from autobahn.twisted import wamp
from autobahn.twisted.websocket import WampWebSocketClientFactory, connectWS
from autobahn.wamp import types
from autobahn.wamp.exception import TransportLost
from autobahn.wamp.serializer import MsgPackSerializer
from threading import Thread, Event

_WampSession = None
_WampConnection = None
_WampSessionEvent = Event()


class WampSession(wamp.ApplicationSession):
    def onJoin(self, details):
        global _WampSession, _WampSessionEvent
        _WampSession = self
        _WampSessionEvent.set()
        print 'WAMP session joined for :', self.config.extra["ID"]

    def onLeave(self, details):
        global _WampSession, _WampSessionEvent
        _WampSessionEvent.clear()
        _WampSession = None
        print 'WAMP session left'


PLCObjDefaults = {
    "StartPLC":          False,
    "GetTraceVariables": ("Broken", None),
    "GetPLCstatus":      ("Broken", None),
    "RemoteExec":        (-1, "RemoteExec script failed!")
}


def WAMP_connector_factory(uri, confnodesroot):
    """
    WAMP://127.0.0.1:12345/path#realm#ID
    WAMPS://127.0.0.1:12345/path#realm#ID
    """
    servicetype, location = uri.split("://")
    urlpath, realm, ID = location.split('#')
    urlprefix = {"WAMP":  "ws",
                 "WAMPS": "wss"}[servicetype]
    url = urlprefix+"://"+urlpath

    def RegisterWampClient():

        # start logging to console
        # log.startLogging(sys.stdout)

        # create a WAMP application session factory
        component_config = types.ComponentConfig(
            realm=realm,
            extra={"ID": ID})
        session_factory = wamp.ApplicationSessionFactory(
            config=component_config)
        session_factory.session = WampSession

        # create a WAMP-over-WebSocket transport client factory
        transport_factory = WampWebSocketClientFactory(
            session_factory,
            url=url,
            serializers=[MsgPackSerializer()],
            debug=False,
            debug_wamp=False)

        # start the client from a Twisted endpoint
        conn = connectWS(transport_factory)
        confnodesroot.logger.write(_("WAMP connecting to URL : %s\n") % url)
        return conn

    AddToDoBeforeQuit = confnodesroot.AppFrame.AddToDoBeforeQuit

    def ThreadProc():
        global _WampConnection
        _WampConnection = RegisterWampClient()
        AddToDoBeforeQuit(reactor.stop)
        reactor.run(installSignalHandlers=False)

    def WampSessionProcMapper(funcname):
        wampfuncname = '.'.join((ID, funcname))

        def catcher_func(*args, **kwargs):
            global _WampSession
            if _WampSession is not None:
                try:
                    return threads.blockingCallFromThread(
                        reactor, _WampSession.call, wampfuncname,
                        *args, **kwargs)
                except TransportLost, e:
                    confnodesroot.logger.write_error(_("Connection lost!\n"))
                    confnodesroot._SetConnector(None)
                except Exception, e:
                    errmess = traceback.format_exc()
                    confnodesroot.logger.write_error(errmess+"\n")
                    print errmess
                    # confnodesroot._SetConnector(None)
            return PLCObjDefaults.get(funcname)
        return catcher_func

    class WampPLCObjectProxy(object):
        def __init__(self):
            global _WampSessionEvent, _WampConnection
            if not reactor.running:
                Thread(target=ThreadProc).start()
            else:
                _WampConnection = threads.blockingCallFromThread(
                    reactor, RegisterWampClient)
            if not _WampSessionEvent.wait(5):
                _WampConnection = stopConnecting()
                raise Exception(_("WAMP connection timeout"))

        def __del__(self):
            global _WampConnection
            _WampConnection.disconnect()
            #
            # reactor.stop()

        def __getattr__(self, attrName):
            member = self.__dict__.get(attrName, None)
            if member is None:
                member = WampSessionProcMapper(attrName)
                self.__dict__[attrName] = member
            return member

    # Try to get the proxy object
    try:
        return WampPLCObjectProxy()
    except Exception, msg:
        confnodesroot.logger.write_error(_("WAMP connection to '%s' failed.\n") % location)
        confnodesroot.logger.write_error(traceback.format_exc())
        return None
