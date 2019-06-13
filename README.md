# APIMethodDocExtractionTool
 This tool extracts the documentation for classes and methods in an Android API library and exports the documentation to 
a formatted text file. 

 Execution speed has been enhanced for this tool by utilizing python concurrent modules as well as asynchronous http 
requests. Thousands of API web pages can be fully scraped in a matter of minutes. On our testing machine we scraped 
documentation on over 9,000 Api urls in under 2.5 minutes.

 To use this to simply download the tool and run with a "ApiDocExtract 'library url' 'filename to extract to'" command
on command line. Specifically, the 'library url' parameter should be the url to the package index page in the desired 
library.
 
 This tool requires the "grequests", "lxml", and "beautifulsoup4" packages to be installed prior to running. Tool
has been tested with Python 3.7 only so it is most likely unstable in previous versions of python

***This tool was designed for libraries from "developer.android.com"***
