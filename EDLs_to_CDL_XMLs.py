from lxml import etree
import re
import string
import os
from sys import argv
from JFaves import *
from copy import deepcopy
import subprocess

class Media:
    'Common base class for all media elements'

#     def __init__(self):
    def __init__(self, asset_num, clipname, asset_type, transition_type, sourceIn,
                 sourceOut, recIn, recOut,  reel, slope, offset, power, saturation):

        self.asset_num = asset_num
        self.clipname = clipname
        self.asset_type = asset_type
        self.transition_type = transition_type
        self.sourceIn = sourceIn
        self.sourceOut = sourceOut
        self.recIn = recIn
        self.recOut = recOut
        self.reel = reel
        
        self.slope = slope
        self.offset = offset
        self.power = power
        self.saturation = saturation
        
    
    def displayBasicInfo(self):
        basicInfoTemplate = string.Template("""
Asset Num: $assetNum
Reel: $reel
Clip name: $clipName
Asset Type: $assetType
Transition Type: $transitionType
Source In: $sourceIn
Source Out: $sourceOut
Record In: $recIn
Record Out: $recOut
----------
Slope: $slope
Offset: $offset
Power: $power
Saturation: $saturation

****************""")
        print basicInfoTemplate.substitute(assetNum=str(self.asset_num), reel=self.reel,
        clipName=self.clipname, assetType=self.asset_type, transitionType=self.transition_type,
        sourceIn=self.sourceIn, sourceOut=self.sourceOut, recIn=self.recIn, recOut=self.recOut,
        slope=self.slope, offset=self.offset, power=self.power, saturation=self.saturation)
        
def edl_to_cdl_xmls(edl_file):

    def simpleParserEDL(edl_file):
        parsedList = []
        
        usefulLine = bool()
        
        with open(edl_file, 'r') as f:
            edl_content = f.read().splitlines()
        
        for i in edl_content:
            if re.match('^\d{3,6}', i, re.IGNORECASE):
                (asset_num, clipname, asset_type, transition_type,
                 sourceIn, sourceOut, recIn, recOut) = re.search('^(\d{3,6})\s*(\w*)\s*(.)\s*(.)\s*(\d\d.\d\d.\d\d.\d\d).*(\d\d.\d\d.\d\d.\d\d).*(\d\d.\d\d.\d\d.\d\d).*(\d\d.\d\d.\d\d.\d\d)',
                i).groups()
                
            elif re.match('^\*ASC_SOP', i, re.IGNORECASE):
                slope, offset, power = re.search('^\*ASC_SOP (\(.*?\))(\(.*?\))(\(.*?\))', i).groups()
            
            elif re.match('^\*ASC_SAT', i, re.IGNORECASE):
                saturation = re.search('^\*ASC_SAT (\d\.\d{0,})', i).groups()[0]

        
        
                newMedia = Media(asset_num=int(asset_num), clipname=clipname, asset_type=asset_type, transition_type=transition_type, sourceIn=sourceIn,
                                 sourceOut=sourceOut, recIn=recIn, recOut=recOut, reel='', slope=slope,
                                 offset=offset, power=power, saturation=saturation)    
                    
                newMedia.displayBasicInfo()
                
                parsedList.append(newMedia)
                
        print '\n\nEDL parsing is finished.'
        
        prettySep
        
        return parsedList

    def parsedEDL_to_XML(parsedList, edl_file):
        dirPathOnly, filenameWithExt, fileNameNoExt = getFileComponents(edl_file)
        
        XMLsDir = os.path.expanduser('~/Documents/RaimApps/XMLs_CDLs/' +
                    fileNameNoExt + '/' + timeStampDaFucker() + '/')
        os.makedirs(XMLsDir)
        
        
        xmlTemplateFile = os.path.join(self_dir, 'Resources/xmlTemplate.xml')
        
        xmlTemplateObj = etree.parse(xmlTemplateFile)
#         print etree.tostring(xmlTemplateObj, pretty_print=True)

        
        print 'Generating XMLs....'
        
        for p in parsedList:
            tempXMLObj = deepcopy(xmlTemplateObj)
            
            slopeElem = tempXMLObj.getroot().xpath('/ColorDecisionList/ColorDecision/ColorCorrection/SOPNode/Slope')[0]
            slopeElem.text = p.slope[1:-1]
            
            offsetElem = tempXMLObj.getroot().xpath('/ColorDecisionList/ColorDecision/ColorCorrection/SOPNode/Offset')[0]
            offsetElem.text = p.offset[1:-1]
            
            powerElem = tempXMLObj.getroot().xpath('/ColorDecisionList/ColorDecision/ColorCorrection/SOPNode/Power')[0]
            powerElem.text = p.power[1:-1]
            
            satElem = tempXMLObj.getroot().xpath('/ColorDecisionList/ColorDecision/ColorCorrection/SatNode/Saturation')[0]
            satElem.text = p.saturation
                        
#             print etree.tostring(tempXMLObj, pretty_print=True)
            
            cdl_filepath = os.path.join(XMLsDir, (p.clipname + '.cdl'))
            
            with open(cdl_filepath, 'a+') as f:
                print 'Writing %s' %(p.clipname + '.cdl')
                f.write(etree.tostring(tempXMLObj, xml_declaration=True, encoding="UTF-8"))
        subprocess.call(["open", "-R", XMLsDir])   
    
        print '\nProcess complete.'
    
  
            
            
#             root = etree.Element('ColorDecisionList')
#             ColorDecision = etree.SubElement(root, 'ColorDecision')
#             ColorCorrection = etree.SubElement(ColorDecision, 'ColorCorrection')
#             Slope = etree.SubElement(ColorCorrection, 'Slope')
#             print etree.tostring(root, pretty_print=True)
#             exit()
            
            
            
    
    
    parsedList = simpleParserEDL(edl_file)
    parsedEDL_to_XML(parsedList, edl_file)
    


if __name__ == '__main__':
    
    if len(argv) > 1:
        inputFiles = argv[1:]
#     else:
#         inputFiles = getClipboardData().splitlines()
    else:
        print "Please drag and drop the EDLs/CDLs you wish to create CDL/XMLs from."
#         exit()
        
        
#     inputFiles = ['/Users/harbor_editorial/Downloads/cdl_stuff/20161121_film_07 copy (Resolve).edl']
    
    for f in inputFiles:
        edl_to_cdl_xmls(f)



