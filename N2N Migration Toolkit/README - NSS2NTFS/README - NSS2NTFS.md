#Metamig Importer

##Requirement

* Mongo Local DB on workstation, not yet configured to use remote DB.
* Python 3
* lxml
* argparse
* Pymongo
* Pandas

##Description

Three scripts : 
* C
* metamigimporter.py : Import metamig file to mongodb
* nssconverter.py : Convert imported trustees to NTFS

Use the first to import, the second to convert & export.

## Usage

```sh
##Syntax

usage: TrusteesToMongo.py [-h] [-i] [-d] [-t INPUTFILE] [-v VOLNAME]

optional arguments:
  -h, --help            show this help message and exit
  -i, --inject          Import Mode
  -d, --delete          Delete Mode
  -t INPUTFILE, --trustees INPUTFILE
                        Fichier trustees Netware
  -v VOLNAME, --volname VOLNAME
                        Volume Name

usage: MetamigToMongo.py [-h] [-i] [-d] [-t INPUTFILE] [-v VOLNAME]
                          [-b DBNAME]

optional arguments:
  -h, --help            show this help message and exit
  -i, --inject          Import Mode
  -d, --delete          Delete Mode
  -t INPUTFILE, --trustees INPUTFILE
                        Fichier trustees metamig
  -v VOLNAME, --volname VOLNAME
                        Volume Name
  -b DBNAME, --database DBNAME
                        Database Name


usage: NSSConverter.py [-h] [-b DBNAME] [-v VOLNAME] [--generateRights] [-e]

optional arguments:
  -h, --help            show this help message and exit
  -b DBNAME, --database DBNAME
                        DB Name
  -v VOLNAME, --volname VOLNAME
                        Volume Name
  --generateRights      Generate rights
  -e, --exportToCSV     Export rights to CSV



##Exemple : 
./metamigimporter.py -i -t trustees/voldatag.trustees -v VOLDATAG -b Bollore
./nssconverter.py -v VOLDATAG -b Bollore --generateRights
./nssconverter.py -v VOLDATAG -b Bollore --exportToCSV
```

