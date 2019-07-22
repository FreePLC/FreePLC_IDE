@echo off
python -tt -c "import Pyro.naming,sys; Pyro.naming.main(sys.argv[1:])" %*
