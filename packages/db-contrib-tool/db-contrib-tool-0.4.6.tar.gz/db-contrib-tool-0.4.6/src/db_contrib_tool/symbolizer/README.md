# `symbolize`

Symbolize MongoDB C++ stacktraces from any Evergreen-generated binary;
including release binaries, patch builds, & mainline waterfall runs.

## Usage
 Help message, usage guide, and list of options:
 ```bash
 $ db-contrib-tool symbolize -h
 ```

### Cheat Sheet of Common Use Cases
```bash
# Symbolize MongoDB stacktraces from any Evergreen binary (including release binaries).
db-contrib-tool symbolize < fassert.stacktrace

# Extract and symbolize stacktraces from logs of live mongod/s/q processes.
tail mongod.log | db-contrib-tool symbolize --live

# Backwards compatible with mongosymb.py
```
