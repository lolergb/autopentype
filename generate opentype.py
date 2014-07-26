# -*- coding: UTF-8 -*-
#
# ----------------------------------------------------------------------------------
#--- imports ----
import sys
import os.path
import re
import plistlib
import features
from features import *

sys.path.insert(0, 'extras/')
reload(features)

#--- Configuration for different ligatures ---
currentFont      = CurrentFont()
listGlyphs       = currentFont.keys()
path             = currentFont.path
pathFea          = "%s/features.fea" % (path)
pathGroup        = "%s/groups.plist" % (path)


#--- Generate basic ---
class generateOpentype:

    #--- Atributtes
    _debug = False

    def __init__(self):
        pass

    def debug(self, sms, result, indent = 1):

        indentDebug = ''

        if self._debug == True:
            indentDebug = '%s' % ('-' * indent)
            print '%s %s %s\n' % (indentDebug, sms, result)


    def createFile(self, name, extension):
        inName = '%s/%s%s' % (currentFont.path, name, extension)  # Name of text file coerced with +.txt

        try:
            file = open(inName,'w')   # Trying to create a new file or open one
            file.close()

        except:
            sys.exit(0) # quit Python


    def writeFea(self, content):

        this = generateOpentype()

        if self._debug == True:
            this.debug('This content for FEA:\n', content)
        else:
            fileOpen = open(pathFea, "w")
            fileOpen.write(content)
            fileOpen.close()


    def writeGroups(self, content):

        this = generateOpentype()

        if self._debug == True:
            this.debug('This content for Groups:\n', content)
        else:
            if os.path.isfile(pathGroup):
                prevContent = plistlib.readPlist(pathGroup)
                content = dict(prevContent.items() + content.items())
                plistlib.writePlist(content, pathGroup)
            else:
                this.createFile('groups', '.plist')
                content = dict(content.items())
                plistlib.writePlist(content, pathGroup)

    def start(self):

        output = ''

        for item in conf_features:
            if item == 'liga':
                output += '%s%s' % (generateFeatureForGlyphs().generateFeature(), '\n')
            else:
                output += '%s%s' %(generateFeatureForGroup().generateFeature(conf_features[item]['expresionRegular'], [conf_features[item]['init'], conf_features[item]['end']], conf_features[item]['nameGroup']), '\n')

        generateOpentype().writeFea(output)


#--- Generate only for glyphs ---
class generateFeatureForGlyphs:

    #--- Attributes ---
    _nameDefault          = conf_features['liga']['name']
    _expresionDefault     = conf_features['liga']['expresionRegular']
    _commentInitDefault   = conf_features['liga']['init']
    _commentEndDefault    = conf_features['liga']['end']

    # Generate one dicctionary with glyphs
    def searchGlyphs(self, expresionRegular):

        outListGlyphs = {}

        for glyphName in listGlyphs:
            if re.match(expresionRegular, glyphName):
                groupGlyphs = glyphName.replace('_', ' ')
                outListGlyphs[groupGlyphs] = glyphName

        return outListGlyphs


    def write(self, content):
        generateOpentype().writeFea(content)


    # name | expresion regular | comments
    def generateFeature(self, name = _nameDefault, expresionRegular = _expresionDefault, comments = [_commentInitDefault, _commentEndDefault]):

        this         = generateFeatureForGlyphs()
        listGlyphs   = this.searchGlyphs(expresionRegular)
        listKeys     = listGlyphs.keys()
        itemsFeature = ''
        initFeature  = '%s\nfeature %s {\n' % (comments[0], name)
        endFeature   = '} %s;\n%s\n' % (name, comments[1])

        for keys in listGlyphs:
            itemsFeature += '\tsub %s by %s;\n' % (keys, listGlyphs[keys])

        outFeature = initFeature + itemsFeature + endFeature

        return outFeature



#--- Generate only for group ---
class generateFeatureForGroup:

    #--- Attributes ---
    _expresionDefault     = conf_features['case']['expresionRegular']
    _commentInitDefault   = conf_features['case']['init']
    _commentEndDefault    = conf_features['case']['end']
    _groupsNames          = conf_features['case']['nameGroup']


    def write(self, content):
        generateOpentype().writeFea(content)


    def writeGroups(self, content):
        generateOpentype().writeGroups(content)


    # Generate one dicctionary with glyphs
    def searchGlyphs(self, expresionRegular = _expresionDefault):

        outListGlyphs = {}
        pureExpresionRegular = expresionRegular[3:]
        withPointExpresionRegular = pureExpresionRegular[1:]

        outListGlyphs[withPointExpresionRegular] = {}

        for glyphName in listGlyphs:
            if re.match(expresionRegular, glyphName):
                groupGlyphs = glyphName.replace(pureExpresionRegular, '')
                outListGlyphs[withPointExpresionRegular][groupGlyphs] = glyphName

        return outListGlyphs


    #Generate basic groups
    def generateBasicGroup(self, listGlyphs, groupsNames = _groupsNames):

        this        = generateFeatureForGroup()
        keys        = listGlyphs.keys()
        glyphs      = listGlyphs
        maxLoop     = int(len(groupsNames))
        groups      = {}
        dictToPlist = {}

        for key in keys:
            groups[key] = {}

            for element in range(maxLoop):
                if element % 2 == 0:
                    groups[key][groupsNames[element]]   = '[%s]' % (' '.join(glyphs[key]))
                    groups[key][groupsNames[element+1]] = '[%s]' % (' '.join(glyphs[key].values()))
                    dictToPlist[groupsNames[element]]   = glyphs[key].values()
                    dictToPlist[groupsNames[element+1]] = glyphs[key].keys()

        this.writeGroups(dictToPlist)

        return groups


    # name | expresion regular | comments
    def generateFeature(self, expresionRegular = _expresionDefault, comments = [_commentInitDefault, _commentEndDefault], groupsNames = _groupsNames):

        this         = generateFeatureForGroup()
        listGlyphs   = this.searchGlyphs(expresionRegular)
        groups       = this.generateBasicGroup(listGlyphs, groupsNames)
        groupName    = []


        itemsFeature = ''
        newItemsFeature = ''

        for items in groups:
            for item in groups[items]:
                newItemsFeature += '@%s = %s\n' % (item, groups[items][item])
                groupName.append(item)

        initFeature  = '%s\nfeature %s {\n' % (comments[0], groups.iterkeys().next())
        endFeature   = '} %s;\n%s\n' % (groups.iterkeys().next(), comments[1])
        itemsFeature = '\tsub @%s by @%s;\n' % (groupName[0], groupName[1])

        outFeature = '%s\n%s%s%s' % (newItemsFeature, initFeature, itemsFeature, endFeature)

        return outFeature


generateOpentype().start()
