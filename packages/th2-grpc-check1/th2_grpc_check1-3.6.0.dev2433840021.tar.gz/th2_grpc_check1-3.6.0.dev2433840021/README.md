# th2 gRPC check1 library (3.6.0)

This library contains proto messages and `Check1` service with RPC methods that are used in [th2 check1](https://github.com/th2-net/th2-check1 "th2-check1"). See [check1.proto](src/main/proto/th2_grpc_check1/check1.proto "check1.proto") file for details. <br>
Tool generates code from `.proto` files and uploads built packages (`.proto` files and generated code) to the specified repositories.

## How to maintain a project
1. Perform the necessary changes.
2. Update the package version of Java in `gradle.properties` file.
3. Update the package version of Python in `package_info.json` file.
4. Commit everything.

### Java
If you wish to manually create and publish a package for Java, run the following command:
```
gradle --no-daemon clean build publish artifactoryPublish \
       -Purl=${URL} \ 
       -Puser=${USER} \
       -Ppassword=${PASSWORD}
```
`URL`, `USER` and `PASSWORD` are parameters for publishing.

### Python
If you wish to manually create and publish a package for Python:
1. Generate services with `Gradle`:
    ```
       gradle --no-daemon clean generateProto
    ```
   You can find the generated files by following path: `src/gen/main/services/python`
2. Generate code from `.proto` files and publish everything using `twine`:
    ```
    pip install -r requirements.txt
    pip install twine
    python setup.py generate
    python setup.py sdist
    twine upload --repository-url ${PYPI_REPOSITORY_URL} --username ${PYPI_USER} --password ${PYPI_PASSWORD} dist/*
    ```
    `PYPI_REPOSITORY_URL`, `PYPI_USER` and `PYPI_PASSWORD` are parameters for publishing.

## Release notes

### 3.6.0

+ Update to `th2-grpc-common` version `3.11.1`

### 3.5.1

#### Changed:

+ `grpc-common` version is updated to 3.9.0

### 3.5.0

#### Added:
+ `silence_check` parameter for `CheckSequenceRule`. Enables automated check for extra messages that match the pre-filter.

#### Changed:
+ Migrated `grpc-common` version from `3.7.0` to `3.8.0`
  + Added `time_precision` and `decimal_precision` to `RootComparisonSettings` message
  + Added `EQ_TIME_PRECISION` and `EQ_DECIMAL_PRECISION` filter operations

### 3.4.2
+ Migrated `grpc-common` version from `3.6.0` to `3.7.0`
    + Added `check_repeating_group_order` parameter to `RootComparisonSettings` message

### 3.4.1
+ Migrated `grpc-common` version from `3.4.0` to `3.6.0`
  + Added the new parameters `description` to `RootMessageFilter` message

### 3.4.0

+ Update to `th2-grpc-common` version `3.4.0`

### 3.3.0
+ Implemented NoMessageCheck rule task. Updated CheckSequence rule task

### 3.2.0

+ Implement stubs creation for Python
