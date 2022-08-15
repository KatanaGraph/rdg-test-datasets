# ldbc_003_maximal

a version of ldbc_003 stored with as many optional rdg data structures as possible.
Intended to be used to test the STPG rdg format

# Generation

Generation of this rdg purposely requires work from the user, as often the definition of what makes a "maximal" rdg
will change between storage format versions.

Before regenerating, modify `generate-maximal-storage-format-rdg/generate-maximal-storage-format-rdg.cpp` to include any new optional data structures which were added by the new storage format version.


```
STORAGE_FORMAT_VERSION=storage_format_version_8
SRC_DIR=$(pwd)
BUILD_DIR=${SRC_DIR}/build
${BUILD_DIR}/external/katana/tools/generate-maximal-storage-format-rdg/generate-maximal-storage-format-rdg ${SRC_DIR}/external/katana/external/test-datasets/rdg_datasets/ldbc_003/${STORAGE_FORMAT_VERSION}/ ${SRC_DIR}/external/katana/external/test-datasets/rdg_datasets/ldbc_003_maximal/${STORAGE_FORMAT_VERSION}/
```


