# URL checker

Python script that loads a list of URLs.  
Resolves the URLs.  
Saves original, resolved, status and http or https.  
Saves to a csv. 

Use clicks for CLI.  
Use pandas for CSV

Uses concurrency  to process URLs in parallel.

**Usage**  
`pip install click pandas`  
`python3 url-checker.py -i urls.txt -o output.csv`

**Test**  
Script comes with automated tests.  
`python3 test.py`
