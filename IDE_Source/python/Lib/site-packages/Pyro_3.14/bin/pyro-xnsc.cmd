@echo off
python -tt -c "import Pyro.xnsc,sys; Pyro.xnsc.main(sys.argv[1:])" %*
