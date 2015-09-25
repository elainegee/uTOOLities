#!/bin/python
import argparse
import sys
import glob
import logging
from datetime import datetime

def main():
    # Setup logging
    LOG_FILENAME="logging-parseDellyVCF-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".log"
    logging.basicConfig(filename=LOG_FILENAME,
                        level = logging.DEBUG,
                        format = '%(asctime)s: %(message)s')
    logging.info("Starting parsing of Delly VCF ")
    # Setup arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest=FOLDERS, nargs='+', help='List of folders containing a Delly VCF.', required=True)
    args = parser.parse_args()
    for folder in args.FOLDERS:
        grabDellyTx(folder)

class DellyVCFline(object):
     """
    Contains the lines of a Delly VCF.
    """
    def __init__(self, line):
        self.line = None
        self.info = None
        self.format = None
        self.chr1 = None
        self.chr2 = None
        self.pos1 = None
        self.pos2 = None
        self.precision = None
        self.filter = None
        self.connection = None
        self.PEsupport = None
        self.MQ = None  #for paired ends
        self.varDepth = None
        self.refPairs = None
        self.varPairs = None
        self.refJxReads = None
        self.varJxReads = None

    def loadVar(self):
        toks = self.line.strip('\n').split('\t')
        self.chr1 = toks[0]
        self.pos1 = toks[1]
        self.filter=toks[6]
        self.info=toks[7].split(';')
        self.precision=self.info[0]
        self.chr2 = getValue(self, list=self.info, key="CHR2")
        self.pos2 = getValue(self, list=self.info, key="END")
        self.connection = getValue(self, list=self.info, key="CT")
        self.PEsupport = getValue(self, list=self.info, key="PE")
        self.MQ = getValue(self, list=self.info, key="MAPQ")
        self.format=toks[7].split(':')
        self.varDepth = None
        self.refPairs = None
        self.varPairs = None
        self.refJxReads = None
        self.varJxReads = None

    def getValue(self, list, listkeys=None, key):
        '''
        Grabs the value from list for corresponding 'key', if it is uniquely found in listkeys (if None, then from list)
        :param list:
        :param listkeys:
        :param key:
        :return:
        '''
        if listkeys != None:
            keyList = listkeys
            valueList = list
        else:
            keyList = list
            valueList = list
        hitIndices = [i for i, s in enumerate(keyList) if key in s]
        if len(hitIndices) == 1:
            data=valueList[hitIndices[0]]
            if "=" in data:
                return data.split("=")[1]
            elif ";" in data:
                return data.split(";")[1]
            else:
                return data
        else:
            logging.error("Unique key '" + key + "' not found in '" + str(list) + "'.")
            raise SystemExit


def grabDellyTx(folder):
    #Find VCF in folder
    for file in glob.glob("*.vcf:):
        logger.info("Parsing " + file)
        with open(file, 'r') as f:
			lines=f.readlines()
			for line in enumerate(lines):
				if line[0] ! = "#":


if __name__ == "__main__":
    sys.exit(main())
