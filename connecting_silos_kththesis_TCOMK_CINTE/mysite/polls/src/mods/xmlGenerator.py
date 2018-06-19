from eulxml import xmlmap
from eulxml.xmlmap import  mods as modsFile
from eulxml.xmlmap import load_xmlobject_from_file
from xml.dom import minidom
import xml.etree.ElementTree as ET
import lxml.etree as etree
import optparse
import sys
import codecs, locale
import os
import re 
import simplejson as json
import json
import shutil
root = ET.Element("modsCollection")
root.set("xmlns", "http://www.loc.gov/mods/v3")
root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
root.set("xsi:schemaLocation", "http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-2.xsd")
mods = ET.Element( "mods")
root.append(mods)
mods.set("xmlns", "http://www.loc.gov/mods/v3")
mods.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")    
mods.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
mods.set("version", "3.2")
mods.set("xsi:schemaLocation","http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-2.xsd" )


def modsData(file,inputjson):
    global examinor, organization, title, subheading, supervisor, keywords, absEng, absSV, name1, last1, name2, last2
    with open(inputjson) as input:
                content = json.load(input)
                input.close()

    #genre
    genre2= ET.Element("genre")
    mods.append(genre2)
    genre2.set("authority" , "diva")
    genre2.set("type", "publicationTypeCode")
    genre2.text="studentThesis"

    genre= ET.Element("genre")
    mods.append(genre)
    genre.set("authority" , "diva")
    genre.set("type", "publicationType")
    genre.set("lang", "swe")
    genre.text="Studentuppsats (Examensarbete)"

    genre3= ET.Element("genre")
    mods.append(genre3)
    genre3.set("authority" , "diva")
    genre3.set("type", "publicationType")
    genre3.set("lang", "eng")
    genre3.text="Student thesis"

    genre4= ET.Element("genre")
    mods.append(genre4)
    genre4.set("authority" , "diva")
    genre4.set("type", "publicationType")
    genre4.set("lang", "nor")
    genre4.text="Oppgave"

     #Examinor
    examinator = ET.Element("name")
    mods.append(examinator)
    examinator.set("type", "personal")
    name = ET.SubElement(examinator , "namePart")
    name.set("type", "family")
    name.text= content["familyName_examinar"]
    last = ET.SubElement(examinator , "namePart")
    last.set("type", "given")
    last.text = content["givenName_examinar"]
    job = ET.SubElement(examinator , "namePart")
    job.set("type", "termsOfAddress")
    job.text = content["jobTitle_examinar"]
    role =ET.SubElement(examinator , "role")
    roleTerm = ET.SubElement(role , "roleTerm")
    roleTerm.set("type" , "code")
    roleTerm.set("authority" , "marcrelator")
    roleTerm.text ="ths"
    org = ET.SubElement(examinator , "affiliation")
    org.text = content["name_examinar"]

    #supervisor
    handledare = ET.Element("name")
    mods.append(handledare)
    handledare.set("type", "personal")
    name = ET.SubElement(handledare , "namePart")
    name.set("type", "family")
    name.text= content["familyName_supervisor"]
    last = ET.SubElement(handledare , "namePart")
    last.set("type", "given")
    last.text = content["givenName_supervisor"]
    jobh = ET.SubElement(handledare , "namePart")
    jobh.set("type", "termsOfAddress")
    jobh.text = content["jobTitle-en_supervisor"]
    role =ET.SubElement(examinator , "role")
    role =ET.SubElement(handledare , "role")
    roleTerm = ET.SubElement(role , "roleTerm")
    roleTerm.set("type" , "code")
    roleTerm.set("authority" , "marcrelator")
    roleTerm.text ="ths"
    
     #organization
    orglist = []
    organisation = ET.Element("name")
    mods.append(organisation)
    for word in content["Orgnization"].split(","):
       org = ET.SubElement(organisation , "namePart")
       org.text = word
    role =ET.SubElement(organisation , "role")
    roleTerm = ET.SubElement(role , "roleTerm")
    roleTerm.set("type" , "code")
    roleTerm.set("authority" , "marcrelator")
    roleTerm.text ="pbl"

    #title and subtitle 
    heading = ET.Element("titleInfo ")
    mods.append(heading)
    heading.set("lang", "")
    name = ET.SubElement(heading , "title")
    subname = ET.SubElement(heading , "subTitle")
    name.text =  content["title"]
    subname.text = content["subtitle"]
   
     #keywords
    keyterms = ET.Element("subject ")
    mods.append(keyterms)
    keyterms.set("lang", "eng")
    for word in content["Keyword(en)"].split(","):
        topic= ET.SubElement(keyterms, "topic")
        topic.text =  word.replace(",", "")

    #english abstract 
    absenglish = ET.Element("abstract ")
    mods.append(absenglish)
    absenglish.set("lang", "eng")
    absenglish.text =  content["abstract(en)"]
    
    #swedish abstract 
    absswedish = ET.Element("abstract")
    mods.append(absswedish)
    absswedish.set("lang", "swe")
    absswedish.text =  content["abstract(sv)"]

     #author1
    writer1 = ET.Element("name")
    mods.append(writer1)
    name = ET.SubElement(writer1 , "namePart")
    name.set("type", "family")
    name.text= content["author_1_aftername"]
    last = ET.SubElement(writer1 , "namePart")
    last.set("type", "given")
    last.text = content["author_1_frontname"]
    role =ET.SubElement(writer1 , "role")
    roleTerm = ET.SubElement(role , "roleTerm")
    roleTerm.set("type" , "code")
    roleTerm.set("authority" , "marcrelator")
    roleTerm.text ="aut"

    #author2
    writer2 = ET.Element("name")
    mods.append(writer2)
    name = ET.SubElement(writer2 , "namePart")
    name.set("type", "family")
    name.text= content["author_2_aftername"]
    last = ET.SubElement(writer2 , "namePart")
    last.set("type", "given")
    last.text = content["author_2_frontname"]
    role =ET.SubElement(writer2 , "role")
    roleTerm = ET.SubElement(role , "roleTerm")
    roleTerm.set("type" , "code")
    roleTerm.set("authority" , "marcrelator")
    roleTerm.text ="aut"

def main(inputjson,outputdir):
    with open(outputdir+'modsXML.xml','wb+') as filehandle:
        modsData(filehandle,inputjson)
        xmlData = ET.tostring(root)
        filehandle.write(xmlData)
        filehandle.close()
        shutil.move(outputdir+'modsXML.xml',outputdir+'modsXML.mods')
    return os.getcwd()+'/'+outputdir+'modsXML.mods'

        
