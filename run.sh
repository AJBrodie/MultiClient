./clean.sh

mpiexec --ompi-server file:/tmp/ompi-server.txt -n 1 python server.py

