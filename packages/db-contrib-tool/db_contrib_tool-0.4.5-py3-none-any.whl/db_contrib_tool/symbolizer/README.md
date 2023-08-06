# `symbolize`

Symbolize MongoDB C++ stacktraces from any Evergreen-generated binary;
including release binaries, patch builds, & mainline waterfall runs.

## Usage
 Help message and list of options:
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

## Usage on Workstations

If the user is using this tool on a Virtual Workstation or another host that does
not have a browser, they must port forward the local authentication port 8989 from
their virtual host to their current host. If the user is sshing into a virtual host,
that command might look something like

```
ssh -L 8989:localhost:8989 user@virtual-host.amazonaws.com
```
