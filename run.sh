#./clean.sh

#mpiexec --ompi-server file:/tmp/ompi-server.txt -n 1 python3 server.py

mpiexec -n 1 python3 server.py
