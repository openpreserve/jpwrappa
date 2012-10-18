build:
	pymakespec --onefile jpwrappa.py
	pyinstaller jpwrappa.spec
	@echo "Built in dist/jpwrappa" 	

install:
	mv dist/jpwrappa $(DESTDIR)

clean:
	rm -fR build
	rm -fR dist
	rm -f jpwrappa.spec
	rm -f logdict2.7.2.final.0-1.log
	rm -f logdict2.7.2.final.0-2.log
	rm -f logdict2.7.2.final.0-3.log
	rm -f warnjpwrappa.txt
