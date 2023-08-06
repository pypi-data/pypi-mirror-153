# `setup-repro-env`

## Table of contents

- [Usage](#usage)
  - [Cheatsheet](#cheatsheet-of-common-use-cases)
  - [Setup MongoDB binaries](#setup-mongodb-binaries)
    - [Setting up the latest available MongoDB binaries from the branch](#setting-up-the-latest-available-mongodb-binaries-from-the-branch)
    - [Setting platform explicitly](#setting-platform-explicitly)
    - [Setting up a specific MongoDB version](#setting-up-a-specific-mongodb-version)
    - [Setting up last-lts and last-continuous versions](#setting-up-last-lts-and-last-continuous-versions)
  - [Setup debug symbols](#setup-debug-symbols)
  - [Setup artifacts (including resmoke, python scripts, jstests, etc)](#setup-artifacts-including-resmoke-python-scripts-jstests-etc)
    - [Setting up artifacts](#setting-up-artifacts)
    - [Setting up artifacts with python venv](#setting-up-artifacts-with-python-venv)
    - [Running resmoke](#running-resmoke)

## Usage

Help message and list of options:
```bash
$ db-contrib-tool setup-repro-env -h
```

### Cheat Sheet of Common Use Cases
```bash
# Download the latest last-lts & last-continuous binaries. Need to run from the root of mongodb/mongo repo.
db-contrib-tool setup-repro-env

# Download a specific version
db-contrib-tool setup-repro-env [5.2, githash123abc, evgversion123abc, evgtask123abc]

# Set up a full repro env
db-contrib-tool setup-repro-env -ds -dv -da \
  mongodb_mongo_master_enterprise_rhel_80_64_bit_dynamic_required_jsCore_9adc8c129a972b7e098bd8c50c9b222f98dd2edb_22_02_16_03_30_27

db-contrib-tool setup-repro-env -ds -dv -da \
  --variant enterprise-rhel-80-64-bit-dynamic-required \
  61b11869850e6134e2fc49bc
```

### Setup MongoDB binaries

#### Setting up the latest available MongoDB binaries from the branch.

If there is no need to download a specific version of MongoDB pass in `<major.minor>` binary version or `master`:

```bash
$ db-contrib-tool setup-repro-env master 5.0
```

Installation directory is defaulted to `build/multiversion_bin` and links to binaries directory is defaulted to the
current working directory, but if there is a need to control those directories `--installDir` and `--linkDir` flags are
available:

```bash
$ db-contrib-tool setup-repro-env \
  --installDir /path/to/install_dir \
  --linkDir /path/to/link_dir \
  master 5.0
```

The binaries will be put in `/path/to/install_dir` under version directory. Symlinks to the binaries will be created in
`/path/to/link_dir`. Suffixes will be added to the symlink names of the binaries from non-master branch.

Installation directory tree example:

```
 |-master
 | |-dist-test
 | | |-LICENSE-Enterprise.txt
 | | |-MPL-2
 | | |-README
 | | |-THIRD-PARTY-NOTICES
 | | |-bin
 | | | |-mongo
 | | | |-mongoauditdecrypt
 | | | |-mongobridge
 | | | |-mongocryptd
 | | | |-mongod
 | | | |-mongodecrypt
 | | | |-mongokerberos
 | | | |-mongoldap
 | | | |-mongoqd
 | | | |-mongos
 | | | |-mongotmock
 | | | |-mqlrun
 | | | |-wt
 | | |-snmp
 | | | |-MONGOD-MIB.txt
 | | | |-MONGODBINC-MIB.txt
 | | | |-README-snmp.txt
 | | | |-enterprise_security_guide.md
 | | | |-mongod.conf.master
 | | | |-mongod.conf.master.selinux
 | | | |-mongod.conf.subagent
 |-5.0
 | |-dist-test
 | | |-LICENSE-Enterprise.txt
 | | |-MPL-2
 | | |-README
 | | |-THIRD-PARTY-NOTICES
 | | |-bin
 | | | |-mongo
 | | | |-mongobridge
 | | | |-mongocryptd
 | | | |-mongod
 | | | |-mongodecrypt
 | | | |-mongokerberos
 | | | |-mongoldap
 | | | |-mongos
 | | | |-mongotmock
 | | | |-mqlrun
 | | | |-wt
 | | |-snmp
 | | | |-MONGOD-MIB.txt
 | | | |-MONGODBINC-MIB.txt
 | | | |-README-snmp.txt
 | | | |-enterprise_security_guide.md
 | | | |-mongod.conf.master
 | | | |-mongod.conf.subagent
```

Links to binaries directory example:

```bash
total 0
lrwxrwxrwx 1 ec2-user ec2-user 63 Dec 24 10:02 mongo -> /home/ec2-user/test/build/multiversion_bin/master/dist-test/bin/mongo
lrwxrwxrwx 1 ec2-user ec2-user 60 Dec 24 10:03 mongo-5.0 -> /home/ec2-user/test/build/multiversion_bin/5.0/dist-test/bin/mongo
lrwxrwxrwx 1 ec2-user ec2-user 75 Dec 24 10:02 mongoauditdecrypt -> /home/ec2-user/test/build/multiversion_bin/master/dist-test/bin/mongoauditdecrypt
lrwxrwxrwx 1 ec2-user ec2-user 69 Dec 24 10:02 mongobridge -> /home/ec2-user/test/build/multiversion_bin/master/dist-test/bin/mongobridge
lrwxrwxrwx 1 ec2-user ec2-user 66 Dec 24 10:03 mongobridge-5.0 -> /home/ec2-user/test/build/multiversion_bin/5.0/dist-test/bin/mongobridge
lrwxrwxrwx 1 ec2-user ec2-user 69 Dec 24 10:02 mongocryptd -> /home/ec2-user/test/build/multiversion_bin/master/dist-test/bin/mongocryptd
lrwxrwxrwx 1 ec2-user ec2-user 66 Dec 24 10:03 mongocryptd-5.0 -> /home/ec2-user/test/build/multiversion_bin/5.0/dist-test/bin/mongocryptd
lrwxrwxrwx 1 ec2-user ec2-user 64 Dec 24 10:02 mongod -> /home/ec2-user/test/build/multiversion_bin/master/dist-test/bin/mongod
lrwxrwxrwx 1 ec2-user ec2-user 61 Dec 24 10:03 mongod-5.0 -> /home/ec2-user/test/build/multiversion_bin/5.0/dist-test/bin/mongod
lrwxrwxrwx 1 ec2-user ec2-user 70 Dec 24 10:02 mongodecrypt -> /home/ec2-user/test/build/multiversion_bin/master/dist-test/bin/mongodecrypt
lrwxrwxrwx 1 ec2-user ec2-user 67 Dec 24 10:03 mongodecrypt-5.0 -> /home/ec2-user/test/build/multiversion_bin/5.0/dist-test/bin/mongodecrypt
lrwxrwxrwx 1 ec2-user ec2-user 71 Dec 24 10:02 mongokerberos -> /home/ec2-user/test/build/multiversion_bin/master/dist-test/bin/mongokerberos
lrwxrwxrwx 1 ec2-user ec2-user 68 Dec 24 10:03 mongokerberos-5.0 -> /home/ec2-user/test/build/multiversion_bin/5.0/dist-test/bin/mongokerberos
lrwxrwxrwx 1 ec2-user ec2-user 67 Dec 24 10:02 mongoldap -> /home/ec2-user/test/build/multiversion_bin/master/dist-test/bin/mongoldap
lrwxrwxrwx 1 ec2-user ec2-user 64 Dec 24 10:03 mongoldap-5.0 -> /home/ec2-user/test/build/multiversion_bin/5.0/dist-test/bin/mongoldap
lrwxrwxrwx 1 ec2-user ec2-user 65 Dec 24 10:02 mongoqd -> /home/ec2-user/test/build/multiversion_bin/master/dist-test/bin/mongoqd
lrwxrwxrwx 1 ec2-user ec2-user 64 Dec 24 10:02 mongos -> /home/ec2-user/test/build/multiversion_bin/master/dist-test/bin/mongos
lrwxrwxrwx 1 ec2-user ec2-user 61 Dec 24 10:03 mongos-5.0 -> /home/ec2-user/test/build/multiversion_bin/5.0/dist-test/bin/mongos
lrwxrwxrwx 1 ec2-user ec2-user 68 Dec 24 10:02 mongotmock -> /home/ec2-user/test/build/multiversion_bin/master/dist-test/bin/mongotmock
lrwxrwxrwx 1 ec2-user ec2-user 65 Dec 24 10:03 mongotmock-5.0 -> /home/ec2-user/test/build/multiversion_bin/5.0/dist-test/bin/mongotmock
lrwxrwxrwx 1 ec2-user ec2-user 64 Dec 24 10:02 mqlrun -> /home/ec2-user/test/build/multiversion_bin/master/dist-test/bin/mqlrun
lrwxrwxrwx 1 ec2-user ec2-user 61 Dec 24 10:03 mqlrun-5.0 -> /home/ec2-user/test/build/multiversion_bin/5.0/dist-test/bin/mqlrun
lrwxrwxrwx 1 ec2-user ec2-user 60 Dec 24 10:02 wt -> /home/ec2-user/test/build/multiversion_bin/master/dist-test/bin/wt
lrwxrwxrwx 1 ec2-user ec2-user 57 Dec 24 10:03 wt-5.0 -> /home/ec2-user/test/build/multiversion_bin/5.0/dist-test/bin/wt
```

#### Setting platform explicitly

Most of the platforms are automatically detected, otherwise set it explicitly:

```bash
$ db-contrib-tool setup-repro-env \
  --edition enterprise \
  --platform ubuntu1804 \
  --architecture x86_64 \
  master 5.0
```

All available platforms can be found [here](https://github.com/10gen/db-contrib-tool/blob/main/src/db_contrib_tool/config/setup_repro_env_config.yml).

#### Setting up a specific MongoDB version

A specific version of MongoDB can be specified by a full commit hash, e.g. if `d9c83ee0c93970029e41234c77dc20b2c5ca6291`
is specified, the binaries are going to be downloaded from
[mongodb_mongo_master_d9c83ee0c93970029e41234c77dc20b2c5ca6291](https://evergreen.mongodb.com/version/mongodb_mongo_master_d9c83ee0c93970029e41234c77dc20b2c5ca6291)
Evergreen version, in case compiled binaries for your platform are available. If Evergreen version will appear on
non-master branches, suffixes will be added to the symlink names of the binaries.

```bash
$ db-contrib-tool setup-repro-env d9c83ee0c93970029e41234c77dc20b2c5ca6291
```

Another way is to specify Evergreen version ID, e.g. if `6172c9b65623435a4c0bdb1a` is specified, the binaries are going
to be downloaded from [6172c9b65623435a4c0bdb1a](https://evergreen.mongodb.com/version/6172c9b65623435a4c0bdb1a)
Evergreen version, in case compiled binaries for your platform are available. This way binaries can be downloaded from
Evergreen patches.

```bash
$ db-contrib-tool setup-repro-env 6172c9b65623435a4c0bdb1a
```

Evergreen task ID can be passed in, e.g. if `mongodb_mongo_master_enterprise_rhel_80_64_bit_dynamic_required_jsCore_9adc8c129a972b7e098bd8c50c9b222f98dd2edb_22_02_16_03_30_27`
is specified, the binaries are going to be downloaded from the same [mongodb_mongo_master_9adc8c129a972b7e098bd8c50c9b222f98dd2edb](https://evergreen.mongodb.com/version/mongodb_mongo_master_9adc8c129a972b7e098bd8c50c9b222f98dd2edb)
Evergreen version and the same `! Shared Library Enterprise RHEL 8.0` Evergreen buildvariant the task was running on.

```bash
$ db-contrib-tool setup-repro-env \
  mongodb_mongo_master_enterprise_rhel_80_64_bit_dynamic_required_jsCore_9adc8c129a972b7e098bd8c50c9b222f98dd2edb_22_02_16_03_30_27
```

#### Setting up last-LTS and last-continuous versions

If `--installLastLTS` and/or `--installLastContinuous` flags are passed, last-LTS and last-continuous versions will be
automatically calculated and downloaded, but this requires mongodb/mongo repo or downloaded artifacts on your machine.

The following command should be run from the root of mongodb/mongo repo or from the `installDir` of the
[artifacts](#setup-artifacts-including-resmoke-python-scripts-jstests-etc).

```bash
$ db-contrib-tool setup-repro-env \
  --installLastLTS \
  --installLastContinuous \
  master
```

If no versions are passed, last-LTS and last-continuous versions will be downloaded by default.

```bash
$ db-contrib-tool setup-repro-env
```

### Setup debug symbols

`--downloadSymbols` flag is to download debug symbols along with the binaries and set up the similar way as the
[binaries](#setting-up-the-latest-available-mongodb-binaries-from-the-branch).

```bash
$ db-contrib-tool setup-repro-env \
  --downloadSymbols \
  master
```

### Setup artifacts (including resmoke, python scripts, jstests, etc)

#### Setting up artifacts

`--downloadArtifacts` flag is to download artifacts that include resmoke, python scripts, jstests, etc.
When flag is passed installation directory is defaulted to `repro_envs` and links to binaries directory is defaulted to
`repro_envs/multiversion_bin`.

```bash
$ db-contrib-tool setup-repro-env \
  --downloadArtifacts \
  d9c83ee0c93970029e41234c77dc20b2c5ca6291
```

`--skipBinaries` flag is to skip downloading binaries, if you want artifacts only.

```bash
$ db-contrib-tool setup-repro-env \
  --downloadArtifacts \
  --skipBinaries \
  d9c83ee0c93970029e41234c77dc20b2c5ca6291
```

#### Setting up artifacts with python venv

`--downloadPythonVenv` flag is to download python venv for resmoke, python scripts, etc that are included in artifacts.

```bash
$ db-contrib-tool setup-repro-env \
  --downloadArtifacts \
  --downloadPythonVenv \
  d9c83ee0c93970029e41234c77dc20b2c5ca6291
```

Installation directory example:

```bash
$ ls -la repro_envs/d9c83ee0c93970029e41234c77dc20b2c5ca6291
total 36
drwxrwxr-x  9 ec2-user ec2-user  266 Dec 24 09:50 .
drwxrwxr-x  3 ec2-user ec2-user   54 Dec 24 09:49 ..
-rw-rw-r--  1 ec2-user ec2-user  552 Dec 22 08:17 .resmoke_mongo_release_values.yml
-rw-rw-r--  1 ec2-user ec2-user   44 Dec 22 08:17 .resmoke_mongo_version.yml
-rw-rw-r--  1 ec2-user ec2-user  644 Dec 22 08:17 all_feature_flags.txt
drwxrwxr-x 23 ec2-user ec2-user 4096 Dec 24 09:49 buildscripts
-rw-rw-r--  1 ec2-user ec2-user  294 Dec 22 08:04 compile_expansions.yml
drwxrwxr-x  4 ec2-user ec2-user  113 Dec 24 09:50 dist-test
drwxrwxr-x  4 ec2-user ec2-user  187 Dec 24 09:49 etc
drwxrwxr-x  6 ec2-user ec2-user 4096 Dec 24 09:49 evergreen
drwxrwxr-x 34 ec2-user ec2-user 4096 Dec 24 09:49 jstests
drwxrwxr-x  4 ec2-user ec2-user   38 Dec 24 09:49 src
drwxrwxr-x  5 ec2-user ec2-user   61 Dec 24 09:50 venv
-rw-rw-r--  1 ec2-user ec2-user  691 Dec 22 08:03 venv_readme.txt
```

After python venv is downloaded there is an extra step needed to make python venv "activatable". Refer to the python
venv readme file that is included and follow the steps described in it.

```bash
$ cd repro_envs/{version}
$ cat venv_readme.txt
# follow the steps described
```

#### Running resmoke

When the python venv can be activated we are ready to run resmoke.

```bash
$ cd repro_envs/{version}
$ . venv/bin/activate  # activating python venv
$ python buildscripts/resmoke.py run -h
```

###### Useful tips on running resmoke

`--installDir` resmoke run flag can be used to pass the path to the binaries, so that resmoke will find the binaries
that were downloaded by setup-repro-env command.<br>
If you're not running multiversion test and running resmoke from `build/repro_envs/{version}` use `dist-test/bin`:

Note that if you are running resmoke.py from the root of the mongo repo, there may be a `resmoke.ini` file generated
from compile that will override the options below. Please consider removing that file to use downloaded binaries. This
behavior is being addressed in [SERVER-62992](https://jira.mongodb.org/browse/SERVER-62992).

```bash
$ cd repro_envs/{version}
$ . venv/bin/activate
$ python buildscripts/resmoke.py run --installDir=dist-test/bin ...
```

For the multiversion test use symlink directory `../multiversion_bin`:

```bash
$ cd repro_envs/{version}
$ . venv/bin/activate
$ python buildscripts/resmoke.py run --installDir=../multiversion_bin ...
```

Another way is to add `/path/to/link_dir` to the PATH:

```bash
$ PATH="$PATH:/path/to/link_dir" python buildscripts/resmoke.py run ...
```

or

```bash
$ export PATH="$PATH:/path/to/link_dir"
$ python buildscripts/resmoke.py run ...
```
