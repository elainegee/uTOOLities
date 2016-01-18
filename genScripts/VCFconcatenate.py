import argparse
import sys
import random
import logging
import string
import os


__author__='elainegee'

parser = argparse.ArgumentParser(description='Concatenate multiple VCFs into one VCF (headers must match).'
                                             'Only unique-ifies two VCF lines if there are an exact match.'
                                             'Otherwise returns all original lines that are not matched.')

parser.add_argument('-i', '--Inputs', type=argparse.FileType('r'), default=sys.stdin, nargs="+", dest="INPUTS",
                    required=True, help='Input VCF file.')
parser.add_argument('-o','--output', type=argparse.FileType('w'), default=sys.stdout, required=True,
                    help='Output VCF file.')
parser.add_argument('-f','--forceHeaderOverride', type=bool, default=False, dest="OVERRIDE", required=False,
                    help='Set to true to override the requirement that the input headers must match.')
args = parser.parse_args()


class VCF(object):
    """
    VCF Object contains the header and lines of the input VCF file.
    """
    def __init__(self, vcf):
        self.file = vcf
        self.header = ""
        self.variants=[]

    def readVCF(self):
        for line in self.file:
            if line[0] == "#":
                self.header += line
            else:
                toks = line.split('\t')
                chrom = toks[0]
                pos = toks[1]
                self.variants.append((chrom, pos, line))

def getUniqueHeaderLines(headerList):
    '''
    Processes a list of header strings and returns one string representing a single header containing
    the unique strings across the list of headers.
    :param HeaderList:
    :return:
    '''
    headerStrList=headerList.pop(0).split('\n')
    while len(headerStrList[-1]) == 0:
        headerStrList.pop()
    vcfFieldStr = headerStrList.pop()
    for element in headerList:
        queryStrings = element.split('\n')
        [headerStrList.append(line) for line in queryStrings if line not in headerStrList and len(line) != 0]
    return '\n'.join(headerStrList.append(vcfFieldStr))


def catSortUniqifyVars(VCFObjectList):
    '''
    Returns sorted unique VCF lines across all VCF objects in the input list.
    :param VCFObjectList:
    :return:
    '''
    allVars = []
    for vcfObj in VCFObjectList:
        [allVars.append(x) for x in vcfObj.variants]
    # sort unique VCFlines by chromosome, then by position
    uniqueVars = list(set(allVars))
    uniqueVars = sorted(uniqueVars, key=lambda x: (x[0],x[1]))
    logging.info("NOTE: " + str(len(allVars) - len(uniqueVars)) + " repeated VCF lines removed from output.\n"
                 "--Final VCF contains " + str(len(uniqueVars)) + " lines.")
    return [vcfstring for (chrom, pos, vcfstring) in uniqueVars]

def idGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    '''
    Creates a string with randomized characters and digits
    :param size:
    :param chars:
    :return:
    '''
    return ''.join(random.choice(chars) for _ in range(size))

logging.basicConfig(format='%(levelname)s: %(asctime)s: %(message)s',
                        filename="VCFconcatenate_" + idGenerator() + ".log", level=logging.DEBUG)
logger = logging.getLogger('VCFconcatenate')

def main():
    logger.info("Analysis performed in working directory '" + os.getcwd() + "'.")
    logger.info("Concatenating " + str(len(args.INPUTS)) + " VCFs:\n" + "\n".join([x.name for x in args.INPUTS]))
    # Load VCF objects with data
    VCFObjs = [VCF(vcf=f) for f in args.INPUTS]
    [obj.readVCF() for obj in VCFObjs]
    VCFHeaders =[obj.header for obj in VCFObjs]
    uniqueHeaders = list(set(VCFHeaders))
    if len(uniqueHeaders) != 1:
        exceptionString = 'VCF headers do not match, cannot concatenate. ' + str(len(uniqueHeaders)) + \
                          ' unique headers found:\n' + '\n***\n'.join(uniqueHeaders)
        if args.OVERRIDE == True:
            logging.warning("WARNING: " + exceptionString + "\nIgnoring.")
            header = getUniqueHeaderLines(uniqueHeaders)
        else:
            logging.error("ERROR: " + exceptionString  + "\nAborting.")
            raise Exception(exceptionString)
    else:
        header = uniqueHeaders[0]
    newVars = catSortUniqifyVars(VCFObjs)
    args.output.write(header + ''.join(newVars))
    logger.info("Concatenation completed successfully.\n--Output sent to '" + args.output.name +"'.\n--DONE.")


if __name__ =="__main__":
    main()
