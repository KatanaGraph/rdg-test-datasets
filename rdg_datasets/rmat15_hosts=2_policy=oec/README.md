rmat15 views for 2 hosts partitioned with blocked oec

used to test loading from partitioned views

## Generation Steps:
mpirun -n 2 partition-dist --loadAllProperties --partition=blocked-oec --newRDG=rmat15_hosts=2_policy=oec rmat15
