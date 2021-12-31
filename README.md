
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

## How to add an rdg to this repo

Required information:
- name of your rdg
- `storage_format_version` of your rdg
  - you can see what storage_format_version you rdg is by running `grep -rni "storage_format_version" *` in the directory containing your rdg
  - if there are no matches, your rdg is `storage_format_version_1`
- wherever you see `<rdg-name>` replace it with the name of your rdg

1) take a look at the organization section above, specifically the `rdg_datasets` section
2) create a directory in `rdg_datasets` called `<rdg-name>`
3) create a `storage_format_version_#` directory in your `<rdg-name>` directory
  - ensure the `storage_format_verion_3` matches the version in the rdg
4) put the rdg contents in the `storage_format_verison_#` directory
  - it is important that the contents of the rdg are directly in the `storage_format_version_#` directory, and not nested inside another directory
5) create a `README.md` in your `<rdg-name>` directory for your rdg with general notes about what this rdg tests, and how it was created.
6) copy one of `[migrate.py, import.py, generate.py]` from another rdg to your `<rdg-name>` directory
  - take a look at the definitions of each of these scripts above to see which is appropriate
  - modify the scripts variables to match your rdg

Now your rdg can be easily upreved to the latest `storage_format_version`
