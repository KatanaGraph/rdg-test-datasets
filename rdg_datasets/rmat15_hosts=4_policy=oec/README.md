rmat15 views for 4 hosts partitioned with blocked oec

used to test loading from partitioned views

## Generation Steps:
mpirun -n 4 partition-dist --loadAllProperties --partition=blocked-oec --newRDG=rmat15_hosts=2_policy=oec rmat15
