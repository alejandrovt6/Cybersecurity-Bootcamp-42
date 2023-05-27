import subprocess

# Path of python files
file1 = '42coin_node1.py'
file2 = '42coin_node2.py'
file3 = '42coin_node3.py'

# Exec python files
process1 = subprocess.Popen(['python', file1])
process2 = subprocess.Popen(['python', file2])
process3 = subprocess.Popen(['python', file3])

# Wait for processes to finish
process2.wait()
process3.wait()

# Print the exit codes of the processes
print('Proceso 1 terminado con código de salida:', process1.returncode)
print('Proceso 2 terminado con código de salida:', process2.returncode)
print('Proceso 3 terminado con código de salida:', process3.returncode)
