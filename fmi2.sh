./clean.sh

xterm -hold -e mpiexec --ompi-server file:/tmp/ompi-server.txt -n 1 python server.py &

xterm -hold -e mpiexec --ompi-server file:/tmp/ompi-server.txt -n 1 python client1.py &

xterm -hold -e mpiexec --ompi-server file:/tmp/ompi-server.txt -n 1 python client2.py &