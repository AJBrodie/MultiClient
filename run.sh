./clean.sh

mpiexec --ompi-server file:/tmp/ompi-server.txt -n 1 python server.py

term -hold -e mpiexec --ompi-server file:/tmp/ompi-server.txt -n 1 python client1.py


term -hold -e mpiexec --ompi-server file:/tmp/ompi-server.txt -n 1 python client2.py
