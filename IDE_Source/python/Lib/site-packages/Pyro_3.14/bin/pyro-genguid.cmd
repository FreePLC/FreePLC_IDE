@echo off
python -tt -c "import Pyro.util,sys; Pyro.util.genguid_scripthelper(sys.argv[1:])" %*
