#!/usr/bin/python

"""
=============================
renameFiles.py
v1.0, 1/18/16
=============================
"""
import argparse
import logging
import os
import sys
import re

__author__ = 'elainegee'

# Global variables
global logger
logger = logging.getLogger(__name__)

def setup_arg_parser():
    '''Setup argument parser.'''
    parser = argparse.ArgumentParser('renamePhotos takes a folder of files and incrementally renames the '
                                     'files that match the given extension (default is *) in the folder. Output '
                                     'filenames are given the nameHeader, incremented based on the time in which the'
                                     'files were last modified (default starting index is 0). Renaming occurs in place.')
    parser.add_argument('-f', '--folderPath', dest="FOLDERPATH",
                        help="Path to folder containing files to rename.",
                        required=True)
    parser.add_argument('-n', '--nameHeader', dest="NAMEHEADER",
                        help="Filename header to include when renaming files incrementally by time stamp. "
                             "See option '-i' for starting index.",
                        required=True)
    parser.add_argument('-i', '--nameIndex', dest="NAMEINDEX",
                        help='Starting index by which to increment renamed files [ default = 0 ].', default=0, required=False)
    parser.add_argument('-x', '--extension', dest="FILEEXTENSION", help="Only rename files with this extension [ default = '.*' ].",
                        default=".*", required=False)
    return parser

def main(folderPath, nameHeader, nameIndex, fileExtension):
    '''Main function to rename files in folder, in order of date modified timestamp.'''
    print "hello"
    logger.info("Getting sorted files in folder ...")
    fileList = sortFilesByTime(folderPath)
    logger.info("Renaming files, with the extension '" + fileExtension + "', incrementally ...")
    renameFiles(fileList, nameHeader, nameIndex, fileExtension)
    logger.info("DONE")

def sortFilesByTime(folderPath):
    '''Returns a list of the absolute paths to file, sorted by most recent content modification.'''
    modtime = lambda f: os.stat(os.path.join(folderPath, f)).st_mtime
    return list(sorted(os.listdir(folderPath), key=modtime))

def renameFiles(fileList, nameHeader, nameIndex, fileExtension):
    nFiles = len(fileList)
    nPad = len(str(nFiles))

    logger.info("Renaming " + str(nFiles) + " files.")
    logger.info("Key:")
    for absFilePath in fileList:
        fileName, ext = os.path.splitext(os.path.basename(absFilePath))
        p = re.compile(fileExtension)
        if p.match(ext):
            newName = os.path.join(nameHeader + "_" + str(nameIndex).zfill(nPad) + ext)
            os.rename(absFilePath, newName)
            logger.info("{" + absFilePath + ": " + newName + "}")
            nameIndex += 1

if __name__ == "__main__":
    # Set up logging
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter=(logging.Formatter('%(levelname)s: %(asctime)s: %(message)s'))
    out_hdlr.setLevel(logging.INFO)
    logger.addHandler(out_hdlr)
    logger.setLevel(logging.INFO)

    # Setup argparse
    parser = setup_arg_parser()
    args = parser.parse_args()

    folderPath = os.path.abspath(args.FOLDERPATH)
    nameHeader = args.NAMEHEADER
    nameIndex = args.NAMEINDEX
    fileExtension = args.FILEEXTENSION

    main(folderPath, nameHeader, nameIndex, fileExtension)