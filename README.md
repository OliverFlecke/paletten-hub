# Mosquitto in Docker

Create container on Azure using:

```sh
az container create -g lars-rg --name palletten --image oliverflecke/mqtt:latest --ports 80 1883 8083 9001 --location northeurope --dns-name-label palletten
```
