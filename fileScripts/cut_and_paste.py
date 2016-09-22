import sys
import os

def uniqify(file, outfile):
    '''Cleans strings of unicode & combines the last column for repeat lines.'''
    with open(file, 'r') as f:
        data = {}
        for line in f:
            line = line.decode('unicode_escape').encode('ascii','ignore')
            line = line.strip('\n\r')
            toks = line.split(',')
            key  = toks[0] + "_" + toks[1] + "_" + toks[9]
            if key in data:
                data[key] += "," + toks[12]
            else:
                data[key] = '\t'.join(toks)
    with open(outfile, 'w') as of:
        for key, string in data.items():
            str_toks = string.split('\t')
            annos = str_toks[-1]
	    if ',' in annos:
                annos_toks = annos.split(',')
                toks_uniq = set(annos_toks)
                str_toks[-1] = ','.join(toks_uniq)
            of.write('\t'.join(str_toks)+ "\n")
 
if __name__ == "__main__":
    uniqify(sys.argv[1], sys.argv[2])
