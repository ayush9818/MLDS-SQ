# PyLint

### List all available checkers
pylint --list-msgs

### Basic Usage
pylint your_file.py

### Output Score Only
pylint --disable=all --enable=metrics your_file.py

### Generate Report
pylint --output-format=html your_file.py > report.html

### Select message severity

#### Disable messages with a severity of "R" (refactor). 
pylint --disable=R your_file.py

#### Enable by severity levels "R" (refactor), "C" (convention), "W" (warning), "E" (error), and "F" (fatal).
pylint --enable=E your_file.py

#### Set thershold for failing the process
pylint --fail-under=8 your_file.py