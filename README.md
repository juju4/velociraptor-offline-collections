# Velociraptor offline collection samples

## Create collector binary

To create offline collection binary from velociraptor binaries:
```
F:> velociraptor.exe config repack config.yaml WinTriage.exe
# OR
velociraptor.exe --config server.config.yaml -v artifacts collect
   Server.Utils.CreateCollector
   --args OS=Windows
   --args artifacts='["""Generic.System.Pstree"""]'
   --args parameters='{"""Generic.System.Pstree""":{}}'
   --args target=ZIP
   --args opt_admin=N
   --args opt_prompt=N
   --output collector.zip
```
or on Linux:
```
wget https://github.com/Velocidex/velociraptor/releases/download/v0.6.7-1/velociraptor-v0.6.7-linux-amd64
./velociraptor-v0.6.7-linux-amd64 config repack LinuxTriage.yaml LinuxOfflineTriage
# OR
/opt/velociraptor/velociraptor --config /etc/velociraptor/server.config.yaml -v artifacts collect \
   Server.Utils.CreateCollector \
   --args OS=Linux \
   --args artifacts='["Linux.Mounts","Linux.Network.Netstat","Linux.RHEL.Packages","Linux.Ssh.AuthorizedKeys","Linux.Ssh.KnownHosts","Linux.Sys.BashHistory","Linux.Sys.BashShell","Linux.Sys.Crontab","Linux.Sys.LastUserLogin","Linux.Sys.Pslist","Linux.Sys.Services","Linux.Sys.SUID","Linux.Sys.Users","Linux.Syslog.SSHLogin","Linux.Users.InteractiveUsers","Linux.Users.RootUsers","Linux.Sys.Maps","Linux.Sys.CPUTime","Linux.Proc.Modules","Linux.Proc.Arp","Linux.OSQuery.Generic","Linux.Network.NetstatEnriched","Linux.Detection.AnomalousFiles","Linux.Debian.Packages","Generic.Collectors.File"]' \
   --args parameters='{"""Linux.Sys.BashShell""":{"""Command""":"""ls -la / /tmp /var/tmp"""},"""Generic.Collectors.File""":{"""collectionSpec""":"""Glob\\n/etc/*\\n/var/log/*\\nUsers\\\\*\\\\NTUser.dat\\n""","""Root""":"""/"""}}' \
   --args target=ZIP \
   --args opt_admin=N \
   --args opt_prompt=N \
   --args opt_tempdir=/var/tmp \
   --args opt_verbose=Y \
   --args opt_progress_timeout=300 \
   --args opt_cpu_limit=80 \
   --args opt_format=jsonl \
   --output collector.zip
```

To extract config from an existing collector binary.
```
Collector_velociraptor-v0.6.7-linux-amd64 config show > LinuxTriage.yaml
```

You can also do the same from web frontend of velociraptor server (Server Artifacts menu: paper plane icon).
Generate files will be available in web interface or locally in ${velociraptor_home}/clients/server/collections/

You may need to download artifacts pack from [Artifact Exchange](https://docs.velociraptor.app/exchange/) to get more artifacts.

## Transfer data

```
$ python3 provision_az_storageaccount.py
Provisioned resource group PythonAzureExample-Storage-rg
Provisioned storage account pythonazurestorage61324
Primary key for storage account: [REDACTED]
Connection string: DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=pythonazurestorage61324;AccountKey=[REDACTED]
Provisioned blob container blob-container-01
Provisioned W sas url https://pythonazurestorage61324.blob.core.windows.net/blob-container-01/IMAGE_PATH/IMAGE_NAME?se=2022-12-04T00%3A08%3A14Z&sp=cw&sv=2021-08-06&sr=b&sig=[REDACTED]
Provisioned RO sas url https://pythonazurestorage61324.blob.core.windows.net/blob-container-01/IMAGE_PATH/IMAGE_NAME?se=2022-12-04T00%3A08%3A14Z&sp=r&sv=2021-08-06&sr=b&sig=[REDACTED]
$ azcopy copy FILE "https://pythonazurestorage61324.blob.core.windows.net/blob-container-01/IMAGE_PATH/IMAGE_NAME?se=2022-12-04T00%3A08%3A14Z&sp=cw&sv=2021-08-06&sr=b&sig=[REDACTED]"
```

## Using data

Data can be reviewed
* either directly (usually json and/or csv outputs). [msticpy Velociraptor provider](https://msticpy.readthedocs.io/en/v2.9.0/data_acquisition/DataProv-Velociraptor.html) is also an option.
* either by loading into velociraptor server ([Importing collections into the GUI](https://docs.velociraptor.app/docs/offline_triage/#importing-collections-into-the-gui), [import_collection](https://docs.velociraptor.app/vql_reference/server/import_collection/); Menu collection - below eye > New collection > Server.Utils.ImportCollection)

## Known issues, troubleshooting

* "error: config repack: client_repack: Provided config file not valid: No API config" on config repack. This can be a configuration issue where need to remove line "Frontend: {}".

# References

* [Offline Collections, Velociraptor docs](https://docs.velociraptor.app/docs/offline_triage/#offline-collections)
* [How Can I Automate The Creation Of The Offline Collector? Velociraptor docs](https://docs.velociraptor.app/knowledge_base/tips/automate_offline_collector/)
* [Triage with Velociraptor  Pt 3, Oct 2019](https://docs.velociraptor.app/blog/2019/2019-10-08_triage-with-velociraptor-pt-3-d6f63215f579/)
* [Local Live Response with Velociraptor ++, Dec 2019](https://mgreen27.github.io/posts/2019/12/08/LocalLRwithVRaptor.html)
* [Triage with Velociraptor — Pt 4, Jul 2020](https://velociraptor.velocidex.com/triage-with-velociraptor-pt-4-cf0e60810d1e)
* [Creating Standalone Artifact Collector, Jun 2022](https://fiskeren.github.io/posts/creating_collector/)
* [triage.zip provides an out-of-the-box Velociraptor triage collector for Windows, pre-configured for rapid and effective incident response. The project is intended for responders who need a reliable offline collector without the hassle of building from scratch.](https://github.com/Digital-Defense-Institute/triage.zip)
* [Enriching Sysmon with Velociraptor, Aug 2025](https://signalsleuth.io/2025/08/31/sysmon_enrichment.html): Authenticode, TLSH, Process Call chains
* [Adaptive Collections with Velociraptor, Sep 2025](https://docs.velociraptor.app/blog/2025/2025-09-28-adaptive-collections/)
* [Memory Analysis with Velociraptor - Part 1, Nov 2025](https://docs.velociraptor.app/blog/2025/2025-11-15-memory-analysis-pt1/): Windows.Memory.Mem2Disk
