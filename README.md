
## Organization
```

rdg_datasets
  - <name_of_some_rdg>/
    - [conditional] import.py
    - [conditional] generate.py
    - [conditional] migrate.py
    - [conditional] README.md
    - storage_format_version_N/<rdg_contents>
    - storage_format_version_N+1/<rdg_contents>
    - storage_format_version_N+2/<rdg_contents>
    
csv_datasets
 - <name_of_some_csv_dataset>/
   - <csv_dataset_contents>
  
misc_datasets
  - <name_of_some_misc_dataset>
    - README.md describing what this misc dataset is and what it can be used for
```

if a rdg can be imported from csv, if possible, its directory should be named identically to the csv datasets directory


misc_datasets should be used only when the dataset does not fall into one of the other categories

### The following scripts are conditionally present for each RDG. One of the following options must be present.
#### import.py
Script to import this RDG from CSV
When to use:
This is the preferred option. If the RDG can be imported from CSV, do this.
#### generate.py
Script to generate this RDG in special way
When to use:
To be used if this RDG is not importable from CSV. If generation is difficult to automate, consider using migrate. 
#### migrate.py
Script to migrate this RDG from its current storage_format_version to the latest
When to use:
Some special RDGs are not easy to generate in an automatible fashion, but can be easily migrated to the latest storage_format_version by loading/storing them. 
#### README.md
Describes how to generate the RDG manually if it is not feasible to generate or migrate it.
If this RDG cannot be created by any of the above scripts, the steps to create it must be described in detail here.
If this is a special RDG, created to cover a specific test case, describe how it is special and the test case(s) here. 


## Requirements of the conditional scripts
- the "main" function must be called uprev to be found by the global uprev script
- the uprev function must return the path to where the new rdg can be found
- the scripts must keep the organization outlined above


## How to uprev the rdgs in this repo
1) ensure the most recent master commit of this repo is checked out: `git checkout main; git pull`
2) run `./uprev build_tools --build_dir=<katana_build_dir>`
2) run `./uprev rdgs --help` to see the required args
 - ex: `./uprev rdgs --storage_format_version <N> --build_dir <katana_build_dir>`
3) ensure `./uprev validate` passes for all rdgs
4) make a new commit with the message `upreved rdgs to storage_format_version_M`
5) create a katana repo PR to bump up the version of this submodule
