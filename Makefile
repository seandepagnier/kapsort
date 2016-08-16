all: regions

install: all
	install kapsort.py /usr/local/bin
	mkdir -p /usr/local/share/kapsort
	install regions /usr/local/share/kapsort
	install kaps2regions.sh /usr/local/bin

regions: regions.gpx
	./gpx2regions.py < regions.gpx > regions.gpx
