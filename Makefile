all:
	python3 setup.py py2app
	echo "" > dist/SoundRain.app/Contents/Resources/qt.conf

debug:
	python3 setup.py py2app -A

clean:
	$(RM) -r build dist
