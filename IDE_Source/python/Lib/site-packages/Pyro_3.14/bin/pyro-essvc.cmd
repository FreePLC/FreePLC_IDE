@echo off
python -tt -c "from Pyro.ext.ES_NtService import PyroES_NTService; import sys; sys.argv[0]='essvc.bat'; PyroES_NTService.HandleCommandLine()" %*
