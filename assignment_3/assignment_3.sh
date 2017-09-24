(head -1 ../assignment_2/data/out/1050-1549.csv; tail -n +2 -q ../assignment_2/data/*.csv) > boliga_all.csv

wget --directory-prefix=./data/ http://download.geofabrik.de/europe/denmark-latest.osm.bz2
bzip2 -d ./data/denmark-latest.osm.bz2

pip install osmread
