# Create Python Package

### Steps

1) Create a Directory: Make a directory for your package.

2) Set Up Structure: Inside the directory, create a structure like this:

mypackage/
├── src/
│   ├── mypackage/
│   │   ├── __init__.py
│   │   ├── mymodule1.py
│   │   └── mymodule2.py
│   └── setup.py
└── README.md

3) Write Code: Write your Python code in the module files (module1.py, module2.py, etc.).

4) Define __init__.py: In __init__.py, import modules and define what gets exported as part of your package's public interface.

5) Add setup.py: file to specify package metadata like name, version, dependencies, etc. 

6) Optional: Add README: Include a README file for documentation.
7) Optional: Add License: Add a license file (e.g., LICENSE) to specify how others can use your code.
    
8) Install Locally: Install your package locally using "pip install -e ." in your package directory.

#create the python package
pip install -e .

#verify installation
pip list | grep 'iris'

#add to path
#Replace /path/to/mypackage/src with the actual path to the src/ directory containing your package root. 
export PYTHONPATH=/path/to/mypackage/src:$PYTHONPATH
export PYTHONPATH=/Users/apujari/Documents/courses/CloudEngineering/code/Week6/code/src/iris_classifier:$PYTHONPATH
echo $PYTHONPATH

9) Test Your Package: Ensure your package works as expected by importing and using it in a Python script or interpreter.

10) Optional: Publish: If you want others to use your package, consider publishing it on the Python Package Index (PyPI).