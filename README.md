# Emag-Scraper
This solution is desired to identify eMag products that stand out by indicators that do not can be used as filters.  
To this end, there are additional indicators visible in the product display. On the Emag website, we have two indicators "Top Favorite" and "Super Pret".  
The end result should be a list for each additional indicator. We choose to look for such products only for the categories that have a special label as well.  
We will search for the products that are on the first two pages of each category.

Software required:  
- python3  
- Within python:  
  - selenium - pip install selenium  
-The Chrome WebDriver compatible with the version of Chrome you use: https://chromedriver.chromium.org/downloads  
-Path to this WebDriver must be added to the Path in Environmental Variables, or else enter the path to the WebDriver directly in the code.  

Running:  
- After running the Python program a Chrome window will automatically open where the program will search.  
- Leave the window open (without minimizing it or covering it with another page) and do not interact with it, it will close automatically at the end of the program.  
- Initially the program will wait for the cookie and login pop-up to appear and then close it for a few seconds.  
- After closing the window the program has completed the search and you will have the results found in the console.  

Results:  
- The results will be in the form of dictionary lists grouped by category as in the query and will be printed to the terminal.  
