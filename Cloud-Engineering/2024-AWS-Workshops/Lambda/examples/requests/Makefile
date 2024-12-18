package:
	pip install -r requirements.txt --target ./package

package.zip: package
	cd package && zip -r ../package.zip . && cd .. && zip package.zip main.py

zip: package.zip
