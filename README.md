# Velociraptor offline collection samples

## Create collector binary

To create offline collection binary from velociraptor binaries:
```
F:> velociraptor.exe config repack config.yaml WinTriage.exe
```
or on Linux:
```
wget https://github.com/Velocidex/velociraptor/releases/download/v0.6.7-1/velociraptor-v0.6.7-linux-amd64
./velociraptor-v0.6.7-linux-amd64 config repack LinuxTriage.yaml LinuxOfflineTriage
```

To extract config from an existing collector binary.
```
Collector_velociraptor-v0.6.7-linux-amd64 config show > LinuxTriage.yaml
```

You can also do the same from web frontend of velociraptor server.
Generate files will be available in web interface or locally in ${velociraptor_home}/clients/server/collections/

## Using data

Data can be reviewed
* either directly (usually json and/or csv outputs)
* either by loading into velociraptor server ([Importing collections into the GUI](https://docs.velociraptor.app/docs/offline_triage/#importing-collections-into-the-gui), [import_collection](https://docs.velociraptor.app/vql_reference/server/import_collection/); Menu collection - below eye > New collection > Server.Utils.ImportCollection)

# References

* [Offline Collections, Velociraptor docs](https://docs.velociraptor.app/docs/offline_triage/#offline-collections)
* [How Can I Automate The Creation Of The Offline Collector? Velociraptor docs](https://docs.velociraptor.app/knowledge_base/tips/automate_offline_collector/)
* [Triage with Velociraptor  Pt 3, Oct 2019](https://docs.velociraptor.app/blog/2019/2019-10-08_triage-with-velociraptor-pt-3-d6f63215f579/)
* [Local Live Response with Velociraptor ++, Dec 2019](https://mgreen27.github.io/posts/2019/12/08/LocalLRwithVRaptor.html)
* [Triage with Velociraptor — Pt 4, Jul 2020](https://velociraptor.velocidex.com/triage-with-velociraptor-pt-4-cf0e60810d1e)
* [Creating Standalone Artifact Collector, Jun 2022](https://fiskeren.github.io/posts/creating_collector/)