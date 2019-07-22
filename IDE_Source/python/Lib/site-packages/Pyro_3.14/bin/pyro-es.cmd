@echo off
python -tt -c "from Pyro.EventService import Server; import sys; Server.start(sys.argv[1:])" %*
