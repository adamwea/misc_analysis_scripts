#bin/bash

# more modular version

# Set the number of nodes
NODES=4

# Get total logical CPUs per node (includes hyperthreads)
CPUS_PER_NODE=$(lscpu | awk '/^CPU\(s\):/{print $2}')

# Get number of sockets per node
SOCKETS_PER_NODE=$(lscpu | awk '/^Socket\(s\):/{print $2}')

# Get cores per socket
CORES_PER_SOCKET=$(lscpu | awk '/^Core\(s\) per socket:/{print $4}')

# Get total cores per node
CORES_PER_NODE=$(( SOCKETS_PER_NODE * CORES_PER_SOCKET ))

# Get logical CPUs per core (hyperthreading ratio)
THREADS_PER_CORE=$(( CPUS_PER_NODE / CORES_PER_NODE ))

# Define the number of logical CPUs per task
CPUS_PER_TASK=4  # Modify as needed 

# Calculate number of tasks per node (ensuring each task fits within a socket)
TASKS_PER_NODE=$(( CPUS_PER_NODE / CPUS_PER_TASK ))

# Echo calculated values
echo "Nodes: $NODES"
echo "Total logical CPUs per node: $CPUS_PER_NODE"
echo "Sockets per node: $SOCKETS_PER_NODE"
echo "Cores per socket: $CORES_PER_SOCKET"
echo "Logical CPUs per core (Threads per core): $THREADS_PER_CORE"
echo "CPUs per task: $CPUS_PER_TASK"
echo "Number of tasks per node: $TASKS_PER_NODE"

# Run the salloc command
salloc -A m2043 -q interactive -C cpu -t 04:00:00 \
  --nodes=$NODES --ntasks-per-node=$TASKS_PER_NODE --cpus-per-task=$CPUS_PER_TASK \
  --image=adammwea/netsims_docker:v1 \
  --threads-per-core=$THREADS_PER_CORE --hint=socket

## Notes:
# aw 2025-02-07 12:29:24 - 8 cpus per simulation in a pop of 128 per gen = 8*128 = 1024 total cpus available across 4 nodes
# aw 2025-02-07 17:26:39 - 4 nodes, 4 cpus per task, 256 simulations per gen, 4*256 = 1024 total cpus available across 4 nodes