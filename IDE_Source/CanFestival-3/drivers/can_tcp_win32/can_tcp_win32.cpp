/*
This file is part of CanFestival, a library implementing CanOpen Stack. 

Copyright (C): Edouard TISSERANT

See COPYING file for copyrights details.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/

#include "Socket.h"

#include <iostream>

using namespace std;

extern "C" {
#include "can_driver.h"

//------------------------------------------------------------------------
UNS8 LIBAPI canReceive_driver(CAN_HANDLE fd0, Message *m)
{

    string l = reinterpret_cast<SocketClient*>(fd0)->ReceiveLine();

    int res = sscanf(l.c_str(),
            "{0x%3hx,%1hhd,%1hhd,{0x%2hhx,0x%2hhx,0x%2hhx,0x%2hhx,0x%2hhx,0x%2hhx,0x%2hhx,0x%2hhx}}",
            &m->cob_id,
            &m->rtr,
            &m->len,
            &m->data[0],
            &m->data[1],
            &m->data[2],
            &m->data[3],
            &m->data[4],
            &m->data[5],
            &m->data[6],
            &m->data[7]
            );


#if defined DEBUG_MSG_CONSOLE_ON
    printf("in : ");
    print_message(m);
#endif

  return res==11 ? 0 : 1 ;
}

UNS8 LIBAPI canSend_driver(CAN_HANDLE fd0, Message const *m)
{
    char s[1024];        
    sprintf(s,"{0x%3.3x,%1d,%1d,{0x%2.2x,0x%2.2x,0x%2.2x,0x%2.2x,0x%2.2x,0x%2.2x,0x%2.2x,0x%2.2x}}",
            m->cob_id,
            m->rtr,
            m->len,
            m->data[0],
            m->data[1],
            m->data[2],
            m->data[3],
            m->data[4],
            m->data[5],
            m->data[6],
            m->data[7]
            );

    reinterpret_cast<SocketClient*>(fd0)->SendLine(s);
#if defined DEBUG_MSG_CONSOLE_ON
    printf("out : ");
    print_message(m);
#endif
    return 0;
}

CAN_HANDLE LIBAPI canOpen_driver(s_BOARD *board)
{
    char *dst = "127.0.0.1";
    if(!strlen(board->busname)){
      dst=board->busname;
    }
    try {
      CAN_HANDLE res = (CAN_HANDLE) new SocketClient(dst, 11898);
      return res;
    } 
    catch (...) {
      cerr << "can_tcp_win32: couldn't connect to" << dst << endl;
      return NULL;
    }
}

int LIBAPI canClose_driver(CAN_HANDLE inst)
{
    delete reinterpret_cast<SocketClient*>(inst);
    return 1;
}

UNS8 LIBAPI canChangeBaudRate_driver( CAN_HANDLE fd, char* baud)
{
    cerr << "canChangeBaudRate not yet supported by this driver\n";
    return 0;
}
}
