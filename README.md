# Spender.me Exporter
[Spender.me](https://spender.me/) is fantastic finance manager. But unfortunately the export data feature is not available for the moment. 

But what if spender.me will break or even shut down? Do you want to have a backup of your data in this case?Spender.py allows you to export all your data in json format. Store and keep it safe.

# Usage

Get data for October of 2017
```
./spender.py email password 09-2017
```

Get data from February to October of 2017
```
./spender.py email password 02-2017 09-2017
```

After script execution `data.txt` file will be created in the working directory.