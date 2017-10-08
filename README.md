# Spender.me Exporter
[Spender.me](https://spender.me/) is fantastic finance manager. But unfortunately the export data feature is not available for the moment. Do you want to have a backup of your data in emergency case? [spender.py](https://github.com/zapletnev/spender-exporter/blob/master/spender.py) allows you to export all your data in json format. Store and keep it safe.

# Usage

Get data for October of 2017
```
./spender.py email password 09-2017
```

Get data from February to October of 2017
```
./spender.py email password 02-2017 09-2017
```

After script execution `data.json` file will be created in the working directory.
