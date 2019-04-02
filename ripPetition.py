# ripPetition.py

from io import StringIO
import argparse
import json
import urllib.request
import datetime
import pathlib

## The basics
# url = "https://petition.parliament.uk/petitions/241584.json"

# pageObject = urllib.request.urlopen( url )

# pageContentAsString = pageObject.read().decode(pageObject.headers.get_content_charset())

# decodeJson = json.load(StringIO(pageContentAsString))
# #print (json.dumps(decodeJson, sort_keys=True, indent=4))

# print("Total: " + str(decodeJson["data"]["attributes"]["signature_count"]))
# for country in decodeJson["data"]["attributes"]["signatures_by_country"] :
# 	if(country["name"] == "United Kingdom"):
# 		print("UK   : " + str(country["signature_count"]))


## ----------------------------------------------------------------------------
## 
## ----------------------------------------------------------------------------
def main ():

    args = processArgs()

    # Use UTC so time is constant
    now = datetime.datetime.utcnow()
    
    fileName = now.strftime("%y%m%d_%H%M")
    filePath = "epetitions/brexit"
    fileName = filePath + "/" + fileName + ".json"
    print ("Write downloaded JSON to " + fileName)
    
    ## Make the directory path we need
    pathlib.Path(filePath).mkdir(parents=True, exist_ok=True)
    
    summaryData = filePath + "/summary.csv"

    ## ------------------------------------------------------------------------
    ## Get the JSON file from the webpage
    ## ------------------------------------------------------------------------
    pageObject = urllib.request.urlopen( args.url )
    pageContentAsString = pageObject.read().decode(pageObject.headers.get_content_charset())
    
    ## Write the sting to a file for backup
    print(pageContentAsString, file=open(fileName, 'w'))

    ## ------------------------------------------------------------------------
    ## load the json string into dict
    ## ------------------------------------------------------------------------
    decodeJson = json.load(StringIO(pageContentAsString))

    ## debug help
    if (args.d):
        testDebug(decodeJson)
    
    ## ------------------------------------------------------------------------
    ## Generate output from that dict
    ## ------------------------------------------------------------------------

    genOutput (args, now, summaryData, decodeJson, 10 , 10)

## ----------------------------------------------------------------------------
## 
## ----------------------------------------------------------------------------
def genOutput (args, now, summaryData, decodeJson, cynum, ctnum):
    
    ## ------------------------------------------------------------------------
    ## Country stats
    ## ------------------------------------------------------------------------
    
    ## get a list of sorted by most signatures first.
    sortedCountry = sorted(decodeJson["data"]["attributes"]["signatures_by_country"], key=lambda x: (x['signature_count']),reverse=True)
    
    print ("\nDateTime : " + str(now) + "\n")
    count = 0

    for country in sortedCountry :

    	if (count < cynum):

    		## 
    		print ("Total : " + 
    			'{:10,}'.format(decodeJson["data"]["attributes"]["signature_count"]) + " " + 
    			'{:30}'.format(str(country["name"])) + " " + 
    			'{:12,}'.format(country["signature_count"]) + " " + 
    			'{:3.2f}'.format(100*country["signature_count"]/decodeJson["data"]["attributes"]["signature_count"]) + 
    			"%")

    		if ( count == 0 ):
    			## We are most likely interested in the top result
    			print(
    			    str(now) + "," + 
    			    '{}'.format(decodeJson["data"]["attributes"]["signature_count"]) + "," + 
    			    '{}'.format(str(country["name"])) + "," + 
    			    '{}'.format(country["signature_count"]) + "," + 
    			    '{:3.2f}'.format(100*country["signature_count"]/decodeJson["data"]["attributes"]["signature_count"])
    			    , file=open(summaryData, 'a'))
    
    	count +=1;
    
    print("") # Line break
    
    ## ------------------------------------------------------------------------
    ## Constituency stats
    ## ------------------------------------------------------------------------
    dumpConstituencyStats(decodeJson, ctnum, True)
    dumpConstituencyStats(decodeJson, ctnum, False)

## ----------------------------------------------------------------------------
## 
## ----------------------------------------------------------------------------
def dumpConstituencyStats(decodeJson, number, rev):
    sortedConstituency = sorted(decodeJson["data"]["attributes"]["signatures_by_constituency"], key=lambda x: (x['signature_count']),reverse=rev)

    count = 0

    for constituency in sortedConstituency :
    	if (count < number):
    		print (
    			'{:8}'.format(str(constituency["signature_count"])) + " " + 
    			'{:30}'.format(str(constituency["mp"])) + " "
    			'{}'.format(str(constituency["name"]))
    			)
    	count+= 1
    
    print("") # Line break


## ----------------------------------------------------------------------------
## Methods
## https://jsonlint.com/
## ----------------------------------------------------------------------------
def testDebug(decodeJson):
	# Show the json structure in a readable form
    print (json.dumps(decodeJson, sort_keys=True, indent=4))
    ## Debug prints, these show the basic structure of the JSON 
    print(decodeJson["links"]["self"])
    print(decodeJson["data"]["id"])
    print(decodeJson["data"]["attributes"]["action"])
    print("Total: " + str(decodeJson["data"]["attributes"]["signature_count"]))
    for country in decodeJson["data"]["attributes"]["signatures_by_country"] :
    	if(country["name"] == "United Kingdom"):
    		print("UK   : " + str(country["signature_count"]))
    
## ----------------------------------------------------------------------------
## 
## ----------------------------------------------------------------------------
def processArgs():
	## Put all the arg parsing in a method and return the args.
    parser = argparse.ArgumentParser(description='Fetch and process a webpage.')

    parser.add_argument('-d', action="store_true", help='Print debug')
    parser.add_argument('-url', default='https://petition.parliament.uk/petitions/241584.json', help='URL to fetch')
    parser.add_argument('--filePath', default='epetitions/brexit', help='Path to output')

    args = parser.parse_args()

    return args

## ----------------------------------------------------------------------------
## run main
## ----------------------------------------------------------------------------
if __name__=="__main__":
   main()

