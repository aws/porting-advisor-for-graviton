Porting Advisor for Graviton
=============================

This is a fork of [Porting advisor](https://github.com/arm-hpc/porting-advisor), an open source project by the ARM High Performance Computing group. Originally, it was coded as a Python module that analyzed some known incompatibilities for C and Fortran code.

 It is a command line tool that analyzes source code for known code patterns and dependency libraries. It then generates a report with any incompatibilities with our Graviton processors. This tool provides suggestions of minimal required and/or recommended versions to run on Graviton instances for both language runtime and dependency libraries. It can run on non-ARM based machines (no Graviton processor needed). This tool does not work on binaries, just source code. It does not make any code modifications, it doesn’t make API level recommendations, nor does it send data back to AWS.

 This tool scans all files in a source tree, regardless of whether they are included by the build system or not. As such it may erroneously report issues in files that appear in the source tree but are excluded by the build system. Currently, the tool supports the following languages/dependencies:

* Python 3+
    * Python version
    * PIP version
    * Dependency versions in requirements.txt file
* Java 8+
    * Java version
    * Dependency versions in pom.xml file
    * JAR scanning for native method  calls (requires JAVA to be installed)
* Go 1.11+
    * Go version
    * Dependency versions on go.mod file
* C, C++, Fortran
    * Inline assembly with no corresponding aarch64 inline assembly.
    * Assembly source files with no corresponding aarch64 assembly source files.
    * Missing aarch64 architecture detection in autoconf config.guess scripts.
    * Linking against libraries that are not available on the aarch64 architecture.
    * Use of architecture specific intrinsic.
    * Preprocessor errors that trigger when compiling on aarch64.
    * Use of old Visual C++ runtime (Windows specific).
    * The following types of issues are detected, but not reported by default:
        * Compiler specific code guarded by compiler specific pre-defined macros.
    * The following types of cross-compile specific issues are detected, but not reported by default.
        * Architecture detection that depends on the host rather than the target.
        * Use of build artifacts in the build process.


For more information on how to modify issues reported, use the tool’s built-in help:

```bash
./porting-advisor-linux-x86_64 -–help
```

If you run into any issues, see our [CONTRIBUTING](CONTRIBUTING.md#reporting-bugsfeature-requests) file.

# How to run:

## As a container

By using this option, you don't need to worry about Python or Java versions, or any other dependency that the tool needs. This is the quickest way to get started. 

**Pre-requisites**

- Docker or [containerd](https://github.com/containerd/containerd) + [nerdctl](https://github.com/containerd/nerdctl) + [buildkit](https://github.com/moby/buildkit)

**Build container image**

**NOTE:** if using containerd, you can substitute `docker` with `nerdctl`

```bash
docker build -t porting-advisor .
```

**NOTE:** on Windows you might need to run these commands to avoid bash scripts having their line ends changed to CRLF:

```shell
git config core.autocrlf false
git reset --hard
```

**Run container image**

After building the image, we can run the tool as a container. We use `-v` to mount a volume from our host machine to the container.

We can run it directly to console:

```bash
docker run --rm -v my/repo/path:/repo porting-advisor /repo
```

Or generate a report:

```bash
docker run --rm -v my/repo/path:/repo -v my/output:/output porting-advisor /repo --output /output/report.html
```

Windows example:

```shell
docker run --rm -v /c/Users/myuser/repo:/repo -v /c/Users/myuser/output:/output porting-advisor /repo --output /output/report.html
```

## As a Python script

**Pre-requisites**

- Python 3.10 or above (with PIP3 and venv module installed).
- (Optionally) Open JDK 17 (or above) and Maven 3.5 (or above) if you want to scan JAR files for native methods.

**Enable Python Environment**

Linux/Mac:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Powershell:
```shell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Install requirements**
```bash
pip3 install -r requirements.txt
```

**Run tool (console output)**
```bash
python3 src/porting-advisor.py ~/my/path/to/my/repo
```

**Run tool (HTML report)**
```bash
python3 src/porting-advisor.py ~/my/path/to/my/repo --output report.html
```

## As a binary

### Generating the binary

**Pre-requisites**

- Python 3.10 or above (with PIP3 and venv module installed).
- (Optionally) Open JDK 17 (or above) and Maven 3.5 (or above) if you want the binary to be able to scan JAR files for native methods.

The `build.sh` script will generate a self-contained binary (for Linux/MacOS). It will be output to a folder called `dist`.

```bash
./build.sh
```

For Windows, the `Build.ps1` will generate a folder with an EXE and all the files it requires to run.

```shell
.\Build.ps1
```

**Running the binary**

**Pre-requisites**

Once you have the binary generated, it will only require Java 11 Runtime (or above) if you want to scan JAR files for native methods. Otherwise, the file is self-contained and doesn't need Python to run.

Default behaviour, console output:
```bash
$ ./porting-advisor-linux-x86_64 ~/my/path/to/my/repo
```

Generating HTML report:
```bash
$ ./porting-advisor-linux-x86_64 ~/my/path/to/my/repo --output report.html
```

Generating a report of just dependencies (this creates an Excel file with just the dependencies we found on the repo, no suggestions provided):
```bash
$ ./porting-advisor-linux-x86_64 ~/my/path/to/my/repo --output dependencies.xlsx --output-format dependencies
```

### Sample console report output:

```bash
./dist/porting-advisor-linux-x86_64 ./sample-projects/
| Elapsed Time: 0:00:03

Porting Advisor for Graviton v1.0.0
Report date: 2023-01-06 23:48:20

13 files scanned.
detected java code. we recommend using Corretto. see https://aws.amazon.com/corretto/ for more details.
detected python code. if you need pip, version 19.3 or above is recommended. we detected that you have version 22.2.1.
detected python code. min version 3.7.5 is required. we detected that you have version 3.10.6. see https://github.com/aws/aws-graviton-getting-started/blob/main/python.md for more details.
./sample-projects/java-samples/pom.xml: dependency library: leveldbjni-all is not supported on Graviton
./sample-projects/java-samples/pom.xml: using dependency library snappy-java version 1.1.3. upgrade to at least version 1.1.4
./sample-projects/java-samples/pom.xml: using dependency library zstd-jni version 1.1.0. upgrade to at least version 1.2.0
./sample-projects/python-samples/incompatible/requirements.txt:3: using dependency library OpenBLAS version 0.3.16. upgrade to at least version 0.3.17
detected go code. min version 1.16 is required. version 1.18 or above is recommended. we detected that you have version 1.15. see https://github.com/aws/aws-graviton-getting-started/blob/main/golang.md for more details.
./sample-projects/java-samples/pom.xml: using dependency library hadoop-lzo. this library requires a manual build  more info at: https://github.com/aws/aws-graviton-getting-started/blob/main/java.md#building-multi-arch-jars
./sample-projects/python-samples/incompatible/requirements.txt:5: dependency library NumPy is present. min version 1.19.0 is required.
detected java code. min version 8 is required. version 11 or above is recommended. see https://github.com/aws/aws-graviton-getting-started/blob/main/java.md for more details.

Use --output FILENAME.html to generate an HTML report.
```