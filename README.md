
## Organization
```

rdg-datasets
  - <name_of_some_rdg>/
    - [conditional] import.[py/sh]
    - [conditional] generate.[py/sh] 
    - [conditional] migrate.[py/sh] 
    - [conditional] README.md
    - storage_format_version_N/<rdg_contents>
    - storage_format_version_N+1/<rdg_contents>
    - storage_format_version_N+2/<rdg_contents>
```

### The following scripts are conditionally present for each RDG. One of the following options must be present.
#### import.[py/sh]
Script to import this RDG from CSV
When to use:
This is the preferred option. If the RDG can be imported from CSV, do this.
#### generate.[py/sh]
Script to generate this RDG in special way
When to use:
To be used if this RDG is not importable from CSV. If generation is difficult to automate, consider using migrate. 
#### migrate.[py/sh]
Script to migrate this RDG from its current storage_format_version to the latest
When to use:
Some special RDGs are not easy to generate in an automatible fashion, but can be easily migrated to the latest storage_format_version by loading/storing them. 
#### README.md
Describes how to generate the RDG manually if it is not feasible to generate or migrate it.
If this RDG cannot be created by any of the above scripts, the steps to create it must be described in detail here.
If this is a special RDG, created to cover a specific test case, describe how it is special and the test case(s) here. 


### Requirements of the conditional scripts
- the "main" function must be called uprev to be found by the global uprev script
- the uprev function must return the path to where the new rdg can be found
- the scripts must keep the organization outlined above
