#!/usr/bin/env python

# Test the logging facilities.

# Set the logfiles
import Pyro.util
Pyro.config.PYRO_LOGFILE = 'Pyro_sys_log'
Pyro.config.PYRO_USER_LOGFILE = 'Pyro_user_log'

print 'Creating the logging objects.'

SLog = Pyro.util.SystemLogger()
ULog = Pyro.util.UserLogger()


def tst(l, head):
	l.raw(head)
	l.error('test','Some error','#1')
	l.warn('test','Some warning','#1')
	l.msg('test','Some message','#1')
	l.error('test','error with numeric args',1,2,3,4)
	l.warn('test','warning with numeric args',1,2,3,4)
	l.msg('test','message with numeric args',1,2,3,4)
	l.error('test error without args')
	l.warn('test warning without args')
	l.msg('test message without args')

print 'Logging various things...'
Pyro.config.PYRO_TRACELEVEL = 0
Pyro.config.PYRO_USER_TRACELEVEL = 0
tst(SLog,'--- THIS IS THE SYSTEM LOG TEST ---\n')
tst(SLog,'YOU SHOULDNT SEE ANY MESSAGES BECAUSE TRACING IS OFF\n')
tst(ULog,'--- THIS IS THE USER LOG TEST ---\n')
tst(ULog,'YOU SHOULDNT SEE ANY MESSAGES BECAUSE TRACING IS OFF\n')
Pyro.config.PYRO_TRACELEVEL = 1
Pyro.config.PYRO_USER_TRACELEVEL = 1
tst(SLog,'YOU SHOULD ONLY SEE ERRORS (LEVEL 1)\n')
tst(ULog,'YOU SHOULD ONLY SEE ERRORS (LEVEL 1)\n')
Pyro.config.PYRO_TRACELEVEL = 2
Pyro.config.PYRO_USER_TRACELEVEL = 2
tst(SLog,'YOU SHOULD ONLY SEE ERRORS+WARNS (LEVEL 2)\n')
tst(ULog,'YOU SHOULD ONLY SEE ERRORS+WARNS (LEVEL 2)\n')
Pyro.config.PYRO_TRACELEVEL = 3
Pyro.config.PYRO_USER_TRACELEVEL = 3
tst(SLog,'YOU SHOULD SEE ALL (LEVEL 3)\n')
tst(ULog,'YOU SHOULD SEE ALL (LEVEL 3)\n')
Pyro.config.PYRO_TRACELEVEL = 4
Pyro.config.PYRO_USER_TRACELEVEL = 4
tst(SLog,'YOU SHOULD SEE ALL (LEVEL 4)\n')
tst(ULog,'YOU SHOULD SEE ALL (LEVEL 4)\n')
Pyro.config.PYRO_TRACELEVEL = -1
Pyro.config.PYRO_USER_TRACELEVEL = -1
tst(SLog,'YOU SHOULDNT SEE ANY MESSAGES BECAUSE TRACING IS -1\n')
tst(ULog,'YOU SHOULDNT SEE ANY MESSAGES BECAUSE TRACING IS -1\n')
print 'All done. See the logfiles!'
print 'System log went to:',SLog._logfile()
print 'User log went to:',ULog._logfile()
print "(or other destinations if so configured when using PYRO_STDLOGGING)"


