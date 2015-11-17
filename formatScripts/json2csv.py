import argparse
import logging
import sys
import os
import random
import string
import csv
import json

__author__='elainegee'

parser = argparse.ArgumentParser(description='Convert a json into an Excel-friendly csv.')

parser.add_argument('-j', '--json', type=str, default=sys.stdin,
                    required=True, help="Input JSON file to be reformatted.")

args = parser.parse_args()

def idGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

logging.basicConfig(format='%(levelname)s: %(asctime)s: %(message)s',
                        filename="json2csv_" + idGenerator() + ".log", level=logging.DEBUG)
logger = logging.getLogger('JSON2CSV')


def main():
    logger.info("Reformating '" + args.json + "' to a CSV file.")
    json_to_csv(args.json)
    logger.info("DONE.")

def ascii_dict_encoding(data):
    ''' Encode values as ascii.'''
    ascii_encode = lambda x: x.encode('ascii') if isinstance(x, unicode) else x
    return dict(map(ascii_encode, pair) for pair in data.items())

def json_to_csv(jsonFile):
    ''' Converts JSON file (Dictionary where each key-ed value is a list of 
    dictionaries) to CSV.'''
    with open(jsonFile, 'r') as f:
        # Load JSON into a list
        contents = json.load(f, object_hook=ascii_dict_encoding)
        print contents.keys()

    # Write out data
    print contents
    for varType, varList in contents.iteritems():
        outFilename = os.path.basename(jsonFile)[:-5] + "_" + varType + ".csv"
        outFH = csv.writer(open(outFilename, 'w'))
        # Write column header
        outFH.writerow(varList[0].keys()) 
        for variant in varList:
            outFH.writerow(variant.values())

        logger.info("\tOutput sent to '" + outFilename + "'") 
 
if __name__=="__main__":
    main()
