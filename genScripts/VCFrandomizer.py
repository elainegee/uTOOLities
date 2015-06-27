import argparse
import sys
import random
import logging
import string


__author__='elainegee'

parser = argparse.ArgumentParser(description='Randomly select lines from a VCF.')

parser.add_argument('-f', '--file', type=argparse.FileType('r'), default=sys.stdin,
                    help='Input VCF file.')
parser.add_argument('-o','--output', type=argparse.FileType('w'), default=sys.stdout,
                    help='Output VCF file.')
parser.add_argument('-n', '--number', type=int, default=1, help='Number of lines randomly'
                                                                ' selected from input VCF.')
args = parser.parse_args()


class VCF(object):
    """
    Contains the lines of a VCF.
    """
    def __init__(self, vcf, output, nLines):
        self.file = vcf
        self.output= output
        self.nLines = nLines
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

    def randomizeVCF(self):
        tmpList = [random.choice(self.variants) for i in range(1, self.nLines + 1)]
        # sort by chromosome, then by position
        tmpList = sorted(tmpList, key=lambda x: (x[0],x[1]))
        outList = [vcfstring for (chrom, pos, vcfstring) in tmpList]
        self.output.write(self.header + ''.join(outList))

def idGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

logging.basicConfig(format='%(levelname)s: %(asctime)s: %(message)s',
                        filename="VCFrandomizer_" + idGenerator() + ".log", level=logging.DEBUG)
logger = logging.getLogger('VCFrandomizer')

def main():
    if args.number <= 0:
        raise Exception('ERROR: Cannot request non-positive number of output lines.')
    logger.info("Generating a randomized VCF with " + str(args.number) + " lines from '" + args.file.name + "'.")
    vcf = VCF(vcf=args.file, output=args.output, nLines=args.number)
    vcf.readVCF()
    if len(vcf.variants) < args.number:
        raise Exception('ERROR: Not enough variants to create a randomized VCF. '
                              'Input VCF only has ' + str(len(vcf.variants)) + ' variants, but '
                              'user requested ' + str(args.number) + ' output variants.')
    vcf.randomizeVCF()
    logger.info("Randomization completed successfully.\n--Output sent to '" + args.output.name +"'.\n--DONE.")


if __name__ =="__main__":
    main()