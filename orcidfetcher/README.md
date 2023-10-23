# ORCID PUBLICATIONS 2 VIVO

This script connects to ORCID's REST API over API KEYS and fetches 	bibliographic entries for research publications by person orcid identifier

The script is called with the following parameters:

```
	publications2vivo.py -j <jsoninputfile> -p <personoutfile> -w <worksoutfile> -m <personmap>
```
Where 
 -j <jsonfile> is a jsonfile containing an array of objects of the following format
 	: ```
 		[{
 			"firstName": "John", 
 		    "lastName": "Doe", 
 		    "orcid": "0000-0000-0000-0000"
 		}]
 	  ```
