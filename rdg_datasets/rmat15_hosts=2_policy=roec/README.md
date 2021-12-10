rmat15 views for 2 hosts partitioned with retained oec

used to test loading from partitioned views

## Generation Steps:
mpirun -n 2 partition-dist --loadAllProperties --partition=retained-oec --newRDG=rmat15_hosts=2_policy=roec rmat15
