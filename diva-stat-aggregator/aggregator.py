""

""

# Get the template file name

# Read the template file
#   store each line in a list
#   get the first column (comma separated)
#   this field will be a key to report

# Get a file or directory name
# Go through the directory listing if directory
# for each export
#   for each line
#     read line, parse as keys
#     read line, parse as values
#     add linenum and filename
#   for each line of the template
#     get the template key
#     find the template key in the export
#     if found then append to template line
#     else append separator to template line

# If no file name then report
# Write out the template

import imp, os, sys

def main_is_frozen():
   return (hasattr(sys, "frozen") or # new py2exe
           hasattr(sys, "importers") # old py2exe
           or imp.is_frozen("__main__")) # tools/freeze

def get_main_file():
   if main_is_frozen():
       return sys.executable
   return os.path.realpath(__file__)

   
# Default logging
sys.stdout = open("stdout.log", "w")
sys.stderr = open("stderr.log", "w")

# Script locations
scriptFile = get_main_file()
scriptName = os.path.basename(scriptFile)
scriptDir = os.path.dirname(scriptFile)

import logging

logger = logging.getLogger(scriptName)
logger.setLevel(logging.DEBUG)

hdlr = logging.FileHandler(scriptFile + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 


import Tkinter, tkFileDialog, tkMessageBox, tkSimpleDialog

# Remove main window
root = Tkinter.Tk()
root.withdraw()

import csv

debug = False

#
def appendReport(exportName=None):
    "Import exported file and append data to the report"
    # Import the export
    logger.info('Importing ' + exportName)
    export = open(exportName, 'rb')
    exportCsv = csv.reader(export)
    lnum = 0
    dataDict = dict()
    for line in exportCsv:
        if lnum%3 == 0: # titles
            # append line number
            toks = []
            for field in line:
                toks.append('%03d_%s' % (lnum+1, field))
        elif lnum%3 == 1: # values
            # append line number
            j = 0
            for field in line:
                dataDict[toks[j]] = field
                j += 1
        lnum += 1
    
    export.close()
    # Append the imported data
    j = 0
    for tag in tags:
        dataField = ''
        if tag in dataDict:
            dataField = dataDict[tag]
        report[j].append(dataField)
        j += 1



# Build a template?
if (debug == False and tkMessageBox.askyesno(title=scriptName, \
    message="Convert an export file a temporary template?") == 1):
    # Get export file name
    exportName = tkFileDialog.askopenfilename(parent=root, \
        filetypes=[('CSV file', '*.csv')], \
        title='Choose an export file')
    if exportName == '':
        sys.exit(1)
    logger.info('Building a pre-template from ' + exportName)
    # Save as pre-template
    templateName = tkFileDialog.asksaveasfilename(parent=root, \
        filetypes=[('CSV file', '*.csv')], \
        initialdir=os.path.dirname(exportName), \
        initialfile='pre-template.csv', \
        title="Save the pre-template as...")
    if templateName == '':
        sys.exit(1)
    logger.info('Saving as ' + templateName)
    # Transform the export into a pre-template
    logger.info('Building...')
    export = open(exportName, 'rb')
    exportCsv = csv.reader(export)
    template = open(templateName, 'wb')
    templateCsv = csv.writer(template)
    lnum = 0
    for fields in exportCsv:
        if lnum%3 == 0: # titles
            # append line number
            tags = []
            for field in fields:
                if field != '':
                    tags.append('%03d_%s' % (lnum+1, field))
                else:
                    tags.append('')
            fields = tags
        templateCsv.writerow(fields)
        lnum += 1

    export.close()
    template.close()
    #Done
    logger.info('Done')
    sys.exit(1)

# Aggregate exports

# Get a template file or die
templateName = u'C:\\'
if debug == False:
    templateName = tkFileDialog.askopenfilename(parent=root, \
        filetypes=[('CSV file', '*.csv')], \
        title='Choose a template file')

if templateName == '':
    sys.exit(1)

# Read the template, extracting first field as tag
logger.info('Parsing ' + templateName)
template = open(templateName, 'rb')
templateCsv = csv.reader(template)
report = []
tags = []
for fields in templateCsv:
    report.append(fields)
    tags.append(fields[0]) 

template.close()

# Loop across files
while True:
    # Select a file
    exportName = tkFileDialog.askopenfilename(parent=root, \
        filetypes=[('CSV file', '*.csv')], \
        initialdir=os.path.dirname(templateName), \
        title='Choose an export file')
    if exportName == '':
        break
    appendReport(exportName)

# Loop across directories
import os, fnmatch
pattern = '*'
while True:
    # Select a directory
    dirName = tkFileDialog.askdirectory(parent=root, \
        initialdir=os.path.dirname(templateName), \
        title='Choose a directory of export files')
    if dirName == '':
        break
    # Select a pattern
    pattern = tkSimpleDialog.askstring('Pattern', \
        'File pattern (all by default)', \
        initialvalue=pattern)
    if pattern == None:
        break
    # Walk through the directory
    for rootdir, dirnames, filenames in os.walk(dirName):
        for filename in fnmatch.filter(filenames, pattern+'.csv'):
            appendReport(os.path.join(rootdir, filename))


# Save as report
while True:
    reportName = tkFileDialog.asksaveasfilename(parent=root, \
        filetypes=[('CSV file', '*.csv')], \
        initialdir=os.path.dirname(templateName), \
        title="Save the filled report as...")
    if reportName != '':
        break
    if tkMessageBox.askyesno(title=scriptName, \
        message="Do you really abort before saving?") == 1:
        sys.exit(1)
# Transform the export into a pre-template
logger.info('Saving as ' + reportName)
reportFile = open(reportName, 'wb')
reportCsv = csv.writer(reportFile)
lnum = 0
for line in report:
    reportCsv.writerow(line)

reportFile.close()
#Done
logger.info('Done')
sys.exit(1)
