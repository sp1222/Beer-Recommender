from bs4 import BeautifulSoup
from collections import Counter
from math import pi
from openpyxl import Workbook
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import BeerCategoryClass
import BeerClass
import itertools as IT
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import re
import time

# CONSTANTS
# the starting row of beer information
BEER_REVIEW_START_ROW = 21
BEER_FEATURES_START_ROW = 50
BEER_WORD_COUNT_START_ROW = 70

# the starting row of category information
CATEGORY_FEATURES_START_ROW = 15
CATEGORY_BEER_REVIEW_COUNT = 41

# number of features in a beer
MAX_NUMBER_OF_FEATURES = 11

# File Names:
BEER_ALL_INFO = 'Beer_All_Info\\'
NEW_BEER_ALL_INFO = 'New_Beer_All_Info\\'
FILE_DIRECTORY = 'D:\\Python Projects\\Beer Recommender Project\\'

# funtion where selenium gathers html from each web page
def seleniumGetsHTML(site):

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(site)
    time.sleep(3)  ### Timer to allow time for the compiler to grab html

    html = BeautifulSoup(driver.page_source, 'html.parser')

    driver.close()
    driver.quit()

    return html

## returns the text of the starting node.
# add the first node to the tree here...
def buildTree(html, site):
    
    # create a root node
    rootNodeOfTree = BeerCategoryClass.BeerCategory()   
    key = 0
    # give root node basic attributes
    rootNodeOfTree.setCategoryName('All Beers')
    rootNodeOfTree.setCategoryKey(key)              # root node will have a key of 0 every time.
    rootNodeOfTree.setCategoryParent(None)          # root node has no parents
    rootNodeOfTree.setCategoryParentKey(key - 1)    # root node does not have a parent, thus root node's parent key is set to -1
    rootNodeOfTree.setCategory_href('/beer/styles') # since we are starting that this page manually, we will go ahead and enter this in manually
    rootNodeOfTree.setSubCategoriesExist(True)
    
    styleBreakClasses = html.findAll('div', {'class': 'stylebreak'})  # this will get all of the div tags with class 'stylebreak'
    for styleBreak in styleBreakClasses:
        key += 1
        currentCategory = BeerCategoryClass.BeerCategory()
        currentCategory.setCategoryName(styleBreak.find('b').get_text())
        currentCategory.setCategoryKey(key)
        currentCategory.setCategoryParent(rootNodeOfTree)
        currentCategory.setCategoryParentKey(rootNodeOfTree.getCategoryKey())
        currentCategory.setSubCategoriesExist(True)
        subCategoryLists = styleBreak.findAll('a')
        for subCategory in subCategoryLists:
            key += 1
            currentSubCategory = BeerCategoryClass.BeerCategory()
            currentSubCategory.setCategoryName(subCategory.get_text())
            currentSubCategory.setCategoryKey(key)
            currentSubCategory.setCategoryParent(currentCategory)
            currentSubCategory.setCategoryParentKey(currentCategory.getCategoryKey())
            currentSubCategory.setCategory_href(subCategory['href'])
            currentCategory.addSubCategory(currentSubCategory)
        rootNodeOfTree.addSubCategory(currentCategory)
    return rootNodeOfTree

    
#******************************************************************************************************************************
# Outputting tree to screen
# prints a visual representation of the categories and sub categories tree.
def printCategoryTree(currentCategory, level):

    if currentCategory.doSubCategoriesExist() == True:
        for sub in currentCategory.getSubCategories():
            print((' |    ')*level)
            print((' |    ')*level)
            print((' |    ')*(level-1) + ' |--' + sub.getCategoryName() + '  Key: ' + str(sub.getCategoryKey()))
            printCategoryTree(sub, (level+1))
        level -= 1    

#*******************************************************************************************************
# Sending tree information to an excel sheet.

def createWorkbookForAllCategories(root):

    for category in root.getSubCategories():
        for subCategory in category.getSubCategories():
            print('Saving Style: ' + subCategory.getCategoryName())
            wb = Workbook()
            categoryName = re.sub('\/', 'and', subCategory.getCategoryName())
            addStyleToNewWorkbook(wb, subCategory, 'None', -1, index = 0)
            fileName = NEW_BEER_ALL_INFO
            openFile = fileName + categoryName + '.xlsx'
            wb.save(openFile)


def addStyleToNewWorkbook(wb, currentCategory, pName, pkey, index):
    currentRow = 0
    currentColumn = 0

    categoryName = re.sub('\/', 'and', currentCategory.getCategoryName())
    wb.create_sheet(index = index, title = categoryName)
    wb.active = index
    sheet = wb.active
    
    catName = sheet.cell(row = 1, column = 1)
    catName.value = 'Category Name:'
    catName = sheet.cell(row = 1, column = 2)    
    catName.value = currentCategory.getCategoryName()

    catKey = sheet.cell(row = 2, column = 1)
    catKey.value = 'Category Key:'
    catKey = sheet.cell(row = 2, column = 2)    
    catKey.value = currentCategory.getCategoryKey()

    catParent = sheet.cell(row = 3, column = 1)
    catParent.value = 'Category Parent:'
    catParent = sheet.cell(row = 3, column = 2)    
    catParent.value = currentCategory.getCategoryParent().getCategoryName()
    
    catParentKey = sheet.cell(row = 4, column = 1)
    catParentKey.value = 'Category Parent Key:'
    catParentKey = sheet.cell(row = 4, column = 2)    
    catParentKey.value = currentCategory.getCategoryParentKey()
        
    catHREF = sheet.cell(row = 5, column = 1)
    catHREF.value = 'Category href:'
    catHREF = sheet.cell(row = 5, column = 2)
    catHREF.value = currentCategory.getCategory_href()

    catDesc = sheet.cell(row = 6, column = 1)
    catDesc.value = 'Category Description:'
    catDesc = sheet.cell(row = 6, column = 2)    
    catDesc.value = currentCategory.getCategoryDescription()

    catDesc = sheet.cell(row = 7, column = 1)
    catDesc.value = 'Minimum ABV:'
    catDesc = sheet.cell(row = 7, column = 2)    
    catDesc.value = currentCategory.getCategoryMinABV()

    catDesc = sheet.cell(row = 8, column = 1)
    catDesc.value = 'Maximum ABV:'
    catDesc = sheet.cell(row = 8, column = 2)    
    catDesc.value = currentCategory.getCategoryMaxABV()

    catDesc = sheet.cell(row = 9, column = 1)
    catDesc.value = 'Minimum IBU:'
    catDesc = sheet.cell(row = 9, column = 2)    
    catDesc.value = currentCategory.getCategoryMinIBU()

    catDesc = sheet.cell(row = 10, column = 1)
    catDesc.value = 'Maximum IBU:'
    catDesc = sheet.cell(row = 10, column = 2)    
    catDesc.value = currentCategory.getCategoryMaxIBU()

    ## category features go here.
    currentRow = CATEGORY_FEATURES_START_ROW
    if len(currentCategory.getCategoryFeaturesMatrix()) == MAX_NUMBER_OF_FEATURES:
        feature = currentCategory.getCategoryFeaturesMatrix()
        i = 0

        var = sheet.cell(row = currentRow, column = 1)
        var.value = 'Astringency'
        var = sheet.cell(row = currentRow, column = 2)
        var.value = feature[i]
        currentRow += 1
        i += 1
        
        var = sheet.cell(row = currentRow, column = 1)
        var.value = 'Body'
        var = sheet.cell(row = currentRow, column = 2)
        var.value = feature[i]
        currentRow += 1
        i += 1
        
        var = sheet.cell(row = currentRow, column = 1)
        var.value = 'Alcohol'
        var = sheet.cell(row = currentRow, column = 2)
        var.value = feature[i]
        currentRow += 1
        i += 1
        
        var = sheet.cell(row = currentRow, column = 1)
        var.value = 'Bitter'
        var = sheet.cell(row = currentRow, column = 2)
        var.value = feature[i]
        currentRow += 1
        i += 1
        
        var = sheet.cell(row = currentRow, column = 1)
        var.value = 'Sweet'
        var = sheet.cell(row = currentRow, column = 2)
        var.value = feature[i]
        currentRow += 1
        i += 1
        
        var = sheet.cell(row = currentRow, column = 1)
        var.value = 'Sour'
        var = sheet.cell(row = currentRow, column = 2)
        var.value = feature[i]
        currentRow += 1
        i += 1
        
        var = sheet.cell(row = currentRow, column = 1)
        var.value = 'Salty'
        var = sheet.cell(row = currentRow, column = 2)
        var.value = feature[i]
        currentRow += 1
        i += 1
        
        var = sheet.cell(row = currentRow, column = 1)
        var.value = 'Fruits'
        var = sheet.cell(row = currentRow, column = 2)
        var.value = feature[i]
        currentRow += 1
        i += 1
        
#        var = sheet.cell(row = currentRow, column = 1)
#        var.value = 'Dark Fruits'
#        var = sheet.cell(row = currentRow, column = 2)
#        var.value = feature[i]
#        currentRow += 1
#        i += 1
        
#        var = sheet.cell(row = currentRow, column = 1)
#        var.value = 'Citrus Fruits'
#        var = sheet.cell(row = currentRow, column = 2)
#        var.value = feature[i]
#        currentRow += 1
#        i += 1
        
#        var = sheet.cell(row = currentRow, column = 1)
#        var.value = 'Tropical Fruits'
#        var = sheet.cell(row = currentRow, column = 2)
#        var.value = feature[i]
#        currentRow += 1
#        i += 1
        
#        var = sheet.cell(row = currentRow, column = 1)
#        var.value = 'Vegetable'
#        var = sheet.cell(row = currentRow, column = 2)
#        var.value = feature[i]
#        currentRow += 1
#        i += 1
        
        var = sheet.cell(row = currentRow, column = 1)
        var.value = 'Hoppy'
        var = sheet.cell(row = currentRow, column = 2)
        var.value = feature[i]
        currentRow += 1
        i += 1
        
#        var = sheet.cell(row = currentRow, column = 1)
#        var.value = 'Herbal'
#        var = sheet.cell(row = currentRow, column = 2)
#        var.value = feature[i]
#        currentRow += 1
#        i += 1
        
#        var = sheet.cell(row = currentRow, column = 1)
#        var.value = 'Floral'
#        var = sheet.cell(row = currentRow, column = 2)
#        var.value = feature[i]
#        currentRow += 1
#        i += 1
        
#        var = sheet.cell(row = currentRow, column = 1)
#        var.value = 'Smoke and Heat'
#        var = sheet.cell(row = currentRow, column = 2)
#        var.value = feature[i]
#        currentRow += 1
#        i += 1
        
        var = sheet.cell(row = currentRow, column = 1)
        var.value = 'Spices'
        var = sheet.cell(row = currentRow, column = 2)
        var.value = feature[i]
        currentRow += 1
        i += 1
        
        var = sheet.cell(row = currentRow, column = 1)
        var.value = 'Malty'
        var = sheet.cell(row = currentRow, column = 2)
        var.value = feature[i]
        currentRow += 1
        i += 1
        
#        var = sheet.cell(row = currentRow, column = 1)
#        var.value = 'Richness'
#        var = sheet.cell(row = currentRow, column = 2)
#        var.value = feature[i]
#        currentRow += 1
#        i += 1
        
#        var = sheet.cell(row = currentRow, column = 1)
#        var.value = 'Yeast'
#        var = sheet.cell(row = currentRow, column = 2)
#        var.value = feature[i]

    # save a list of beer and their review count,
    # will use this to determine how impacting the reviews will be on features
    var = sheet.cell(row = 40, column  = 1)
    var.value = 'Beer Name'
    var = sheet.cell(row = 40, column  = 2)
    var.value = 'Review Count'    
    currentRow = CATEGORY_BEER_REVIEW_COUNT
    currentColumn = 1    
    for beer in currentCategory.getCategoryBeers():
        var = sheet.cell(row = currentRow, column  = 1)
        var.value = beer.getBeerName()
        var = sheet.cell(row = currentRow, column  = 2)
        var.value = len(beer.getBeerReviewsFullContent())
        currentRow += 1

### START BEER INFORMATION
    # enter information for each beer into their own sheets after category sheet
    for eachItem in currentCategory.getCategoryBeers():
        index += 1
        beerName = eachItem.getBeerName()
        beerName = re.sub('[^A-Za-z0-9]+', '', beerName)
        wb.create_sheet(index = index, title = beerName)
        wb.active = index
        sheet = wb.active
        
        label = sheet.cell(row = 1, column = 1)
        label.value = 'Beer Name'
        var = sheet.cell(row = 1, column = 2)
        var.value = eachItem.getBeerName()
        
        label = sheet.cell(row = 2, column = 1)
        label.value = 'Beer key'
        var = sheet.cell(row = 2, column = 2)
        var.value = eachItem.getBeerKey()
        
        label = sheet.cell(row = 3, column = 1)
        label.value = 'Beer Style'
        var = sheet.cell(row = 3, column = 2)
        var.value = eachItem.getBeerStyle()
        print(var.value)
        
        label = sheet.cell(row = 4, column = 1)
        label.value = 'Beer Style Key'
        var = sheet.cell(row = 4, column = 2)
        var.value = eachItem.getBeerCategoryKey()
        
        label = sheet.cell(row = 5, column = 1)
        label.value = 'Brewery'
        var = sheet.cell(row = 5, column = 2)
        var.value = eachItem.getBeerBrewery()
        
        label = sheet.cell(row = 6, column = 1)
        label.value = 'Ave Rating'
        var = sheet.cell(row = 6, column = 2)
        var.value = eachItem.getBeerAverageRating()
        
        label = sheet.cell(row = 7, column = 1)
        label.value = 'Beer ABV'
        var = sheet.cell(row = 7, column = 2)
        var.value = eachItem.getBeerABV()
        
        label = sheet.cell(row = 8, column = 1)
        label.value = 'Beer Min IBU'
        var = sheet.cell(row = 8, column = 2)
        var.value = eachItem.getBeerMinIBU()
               
        label = sheet.cell(row = 9, column = 1)
        label.value = 'Beer Max IBU'
        var = sheet.cell(row = 9, column = 2)
        var.value = eachItem.getBeerMaxIBU()
        
        label = sheet.cell(row = 10, column = 1)
        label.value = 'Beer Description'
        var = sheet.cell(row = 10, column = 2)
        try:
            var.value = eachItem.getBeerDescription()
        except:
            var.value = 'error entering this description'

### BEER FULL REVIEWS HERE
        label = sheet.cell(row = 20, column = 1)
        label.value = 'Reviews:'
        currentRow = BEER_REVIEW_START_ROW
        currentColumn = 1
        columnWidth = 100
        for eachReview in eachItem.getBeerReviewsFullContent():
            var = sheet.cell(row = currentRow, column = currentColumn)            
            try:
                var.value = eachReview
            except:
                var.value = 'error entering this review'
            currentRow += 1

### BEER FEATURES MATRIX HERE
        # this is where we will save our beer features values
        currentRow = BEER_FEATURES_START_ROW
        if len(eachItem.getBeerFeaturesMatrix()) == MAX_NUMBER_OF_FEATURES:
            feature = eachItem.getBeerFeaturesMatrix()
            i = 0

            var = sheet.cell(row = currentRow, column = 1)
            var.value = 'Astringency'
            var = sheet.cell(row = currentRow, column = 2)
            var.value = feature[i]
            currentRow += 1
            i += 1
            
            var = sheet.cell(row = currentRow, column = 1)
            var.value = 'Body'
            var = sheet.cell(row = currentRow, column = 2)
            var.value = feature[i]
            currentRow += 1
            i += 1
            
            var = sheet.cell(row = currentRow, column = 1)
            var.value = 'Alcohol'
            var = sheet.cell(row = currentRow, column = 2)
            var.value = feature[i]
            currentRow += 1
            i += 1
            
            var = sheet.cell(row = currentRow, column = 1)
            var.value = 'Bitter'
            var = sheet.cell(row = currentRow, column = 2)
            var.value = feature[i]
            currentRow += 1
            i += 1
            
            var = sheet.cell(row = currentRow, column = 1)
            var.value = 'Sweet'
            var = sheet.cell(row = currentRow, column = 2)
            var.value = feature[i]
            currentRow += 1
            i += 1
            
            var = sheet.cell(row = currentRow, column = 1)
            var.value = 'Sour'
            var = sheet.cell(row = currentRow, column = 2)
            var.value = feature[i]
            currentRow += 1
            i += 1
            
            var = sheet.cell(row = currentRow, column = 1)
            var.value = 'Salty'
            var = sheet.cell(row = currentRow, column = 2)
            var.value = feature[i]
            currentRow += 1
            i += 1
            
            var = sheet.cell(row = currentRow, column = 1)
            var.value = 'Fruits'
            var = sheet.cell(row = currentRow, column = 2)
            var.value = feature[i]
            currentRow += 1
            i += 1
            
#            var = sheet.cell(row = currentRow, column = 1)
#            var.value = 'Dark Fruits'
#            var = sheet.cell(row = currentRow, column = 2)
#            var.value = feature[i]
#            currentRow += 1
#            i += 1
            
#            var = sheet.cell(row = currentRow, column = 1)
#            var.value = 'Citrus Fruits'
#            var = sheet.cell(row = currentRow, column = 2)
#            var.value = feature[i]
#            currentRow += 1
#            i += 1
            
#            var = sheet.cell(row = currentRow, column = 1)
#            var.value = 'Tropical Fruits'
#            var = sheet.cell(row = currentRow, column = 2)
#            var.value = feature[i]
#            currentRow += 1
#            i += 1
            
#            var = sheet.cell(row = currentRow, column = 1)
#            var.value = 'Vegetable'
#            var = sheet.cell(row = currentRow, column = 2)
#            var.value = feature[i]
#            currentRow += 1
#            i += 1
            
            var = sheet.cell(row = currentRow, column = 1)
            var.value = 'Hoppy'
            var = sheet.cell(row = currentRow, column = 2)
            var.value = feature[i]
            currentRow += 1
            i += 1
            
#            var = sheet.cell(row = currentRow, column = 1)
#            var.value = 'Herbal'
#            var = sheet.cell(row = currentRow, column = 2)
#            var.value = feature[i]
#            currentRow += 1
#            i += 1
            
#            var = sheet.cell(row = currentRow, column = 1)
#            var.value = 'Floral'
#            var = sheet.cell(row = currentRow, column = 2)
#            var.value = feature[i]
#            currentRow += 1
#            i += 1
            
#            var = sheet.cell(row = currentRow, column = 1)
#            var.value = 'Smoke and heat'
#            var = sheet.cell(row = currentRow, column = 2)
#            var.value = feature[i]
#            currentRow += 1
#            i += 1
            
            var = sheet.cell(row = currentRow, column = 1)
            var.value = 'Spices'
            var = sheet.cell(row = currentRow, column = 2)
            var.value = feature[i]
            currentRow += 1
            i += 1
            
            var = sheet.cell(row = currentRow, column = 1)
            var.value = 'Malty'
            var = sheet.cell(row = currentRow, column = 2)
            var.value = feature[i]
            currentRow += 1
            i += 1
            
#            var = sheet.cell(row = currentRow, column = 1)
#            var.value = 'Richness'
#            var = sheet.cell(row = currentRow, column = 2)
#            var.value = feature[i]
#            currentRow += 1
#            i += 1
            
#            var = sheet.cell(row = currentRow, column = 1)
#            var.value = 'Yeast'
#            var = sheet.cell(row = currentRow, column = 2)
#            var.value = feature[i]


### BEER WORD COUNTS START HERE
        # word count for each beer from description and reviews saved here
        currentRow = BEER_WORD_COUNT_START_ROW
        var = sheet.cell(row = currentRow, column = 1)
        var.value = 'Words'
        var = sheet.cell(row = currentRow, column = 2)
        var.value = 'Counts'
        
        currentRow += 1
        currentColumn = 1
        if eachItem.getBeerWordCount() != None:
            for keyVal in eachItem.getBeerWordCount():
                currentCell = sheet.cell(row = currentRow, column = currentColumn)
                # sends word to excel file
                variable = currentCell
                variable.value = keyVal[0]
                currentColumn += 1
                currentCell = sheet.cell(row = currentRow, column = currentColumn)
                # sends word count to excel file
                variable = currentCell
                variable.value = keyVal[1]
                currentRow += 1
                currentColumn = 1
        

# Look for any empty or blank pages and remove them from the workbook (this usually occurs at the end of the workbook)
    for sheet in wb:
        if sheet.cell(row = 1, column = 1).value == '' or sheet.cell(row = 1, column = 1).value == None:
            wb.remove(sheet)

#*******************************************************************************************************
# Get information from excel file, given that there is an implemented tree already made and information
# just needs to be filled in

def loadSubCategories(tree):
           
    # first we need to see if the name of the categories we want to collect data from exist as files
    fileList = os.listdir(FILE_DIRECTORY + BEER_ALL_INFO)
    print('Gathering File Names..')
    excelFileList = []
    fileName = BEER_ALL_INFO
    for file in fileList:
        excelFileList.append(fileName + file)  # list of file names

    print('Matching categories to their keys..')
    for excel in excelFileList:
        keyFound = False
        wb = load_workbook(excel)
        wb.active = 0
        key = int(wb.active.cell(row = 2, column = 2).value)
        for category in tree.getSubCategories():
            for subCategory in category.getSubCategories():
                if subCategory.getCategoryKey() == key:
                    print('Loading Style: ' + subCategory.getCategoryName())
                    subCategory = gatherInformation(0, wb, subCategory)
                    subCategory.setCategoryParent(category)
                    keyFound == True
                    break
            if keyFound == True:
                break

    category = tree.getSubCategories()[0]
#    for subCategory in category.getSubCategories():
#        print(subCategory.getCategoryName())
#        print(subCategory.getCategoryMaxIBU())
                    
    print('loading complete')

    return tree

def gatherInformation(index, wb, tempCategory):
    wb.active = index
    sheet = wb.active
    tempCategory.setCategoryName(sheet.cell(row = 1, column = 2).value)    
    tempCategory.setCategoryKey(int(sheet.cell(row = 2, column = 2).value))
    # we set category parent to the object being iterated after this function
    tempCategory.setCategoryParentKey(int(sheet.cell(row = 4, column = 2).value))
    tempCategory.setCategory_href(sheet.cell(row = 5, column = 2).value)
    tempCategory.setCategoryDescription(sheet.cell(row = 6, column = 2).value)
    tempCategory.setCategoryMinABV(float(sheet.cell(row = 7, column = 2).value))
    tempCategory.setCategoryMaxABV(float(sheet.cell(row = 8, column = 2).value))
    tempCategory.setCategoryMinIBU(int(sheet.cell(row = 9, column = 2).value))
    tempCategory.setCategoryMaxIBU(int(sheet.cell(row = 10, column = 2).value))
    # this is where we will load our keyword data bank for this beer
    currentRow = 15
    i = 0
    features = []
#    while i < 18:
#        var = sheet.cell(row = currentRow, column = 2)
#        if var.value != '' or var.value != None:
#            features.append(sheet.cell(row = currentRow, column = 2).value)
#        currentRow += 1
#        i += 1
#    tempCategory.setCategoryFeaturesMatrix(features)    
    index += 1
    
    while index < len(wb.worksheets):
        wb.active = index
        sheet = wb.active
        
        currentColumn = 2
        currentRow = 1
        currentCell = sheet.cell(row = currentRow, column = currentColumn)
        while currentCell.value != '' and currentCell.value != None:
            tempItem = BeerClass.Beer()

            value = currentCell.value
            tempItem.setBeerName(value)
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            
            value = currentCell.value
            if value == '' or value == None:
                value = 0
            tempItem.setBeerKey(int(value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            
            value = currentCell.value
            if value == '' or value == None:
                value = 'NA'
            tempItem.setBeerStyle(value)
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            
            value = currentCell.value
            if value == '' or value == None:
                value = 0
            tempItem.setBeerCategoryKey(int(value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            
            value = currentCell.value
            if value == '' or value == None:
                value = 'NA'
            tempItem.setBeerBrewery(value)
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            
            value = currentCell.value
            if value == '' or value == None:
                value = 0.0
            tempItem.setBeerABV(float(value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            
            value = currentCell.value
            if value == '' or value == None:
                value = 0.0
            tempItem.setBeerAverageRating(float(value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            
            value = currentCell.value
            if value == '' or value == None:
                value = 0
            tempItem.setBeerMinIBU(int(value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            
            value = currentCell.value
            if value == '' or value == None:
                value = 0
            tempItem.setBeerMaxIBU(int(value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            
            value = currentCell.value
            if value == '' or value == None:
                value = 'NA'
            tempItem.setBeerDescription(value)

### LOAD BEER REVIEWS
            currentRow = BEER_REVIEW_START_ROW
            currentColumn = 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            while currentCell.value != '' and currentCell.value != None:
                value = currentCell.value
                tempItem.addBeerReviewsFullContent(value)
                currentRow += 1
                currentCell = sheet.cell(row = currentRow, column = currentColumn)

### LOAD BEER FEATURES
            currentRow = BEER_FEATURES_START_ROW
            currentColumn = 2
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            features = []
            while currentCell.value != '' and currentCell.value != None:
                features.append(currentCell.value)
                currentRow += 1
                currentCell = sheet.cell(row = currentRow, column = currentColumn)
            tempItem.setBeerFeaturesMatrix(features)
            
### LOAD BEER WORD COUNTS
#            currentRow += 6
#            currentColumn = 1
#            currentCell = sheet.cell()
#            while currentCell.value != '' and currentCell.value != None:


### ADD BEER TO CATEGORY
        tempCategory.addCategoryBeer(tempItem)

### GO TO NEXT PAGE
        index += 1

    return tempCategory

#*************************************************************************************************************
## these sets of functions web scrapes heb.com in each category and loads items to their respective categories
## in the category tree.

def startGetCategoryItems(root, site):

    sinceEpoch = time.time()
    startTimeObj = time.localtime(sinceEpoch)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    currentSite = site + root.getCategory_href()
    driver.get(currentSite)
    time.sleep(3)

    # we know that there are no items in each category in root's list of sub categories
    # we move on to each category's sub category where we will find our beer.

    # first we will see if there are any category files already in existence due to interrupts    
    key = 0
    for eachCategory in root.getSubCategories():
        for eachSubCategory in eachCategory.getSubCategories():
            # this is done to skip any category scraping for data we already have after loading
            # if we have more than one beer in this eachSubCategory, then we know that we already
            # have this information from a previous scrape session.
            # this has to be implemented because of SPECTRUM's wonderful internet connection....
            # to save time
            if len(eachSubCategory.getCategoryBeers()) == 0:
                print('Scraping ' + eachSubCategory.getCategoryName())
                key = openSubCategoryPages(eachSubCategory, driver, site, key)
    
    driver.close()
    driver.quit()
    
    sinceEpoch = time.time()
    endTimeObj = time.localtime(sinceEpoch)
    
    print('Started: %d:%d' %(startTimeObj.tm_hour, startTimeObj.tm_min))
    print('Finished: %d:%d' %(endTimeObj.tm_hour, endTimeObj.tm_min))

    return root

def cleanupDoubleDecimalStrings(string):

    if string != '' or string != None:
        newString = re.sub('[a-zA-Z()\s$\/%:]', '', string)
        minIBU = maxIBU = ''
        dividerFound = False
        for c in newString:
            if c == '-':
                dividerFound = True
                continue
            if dividerFound == False:
                minIBU += c
            else:
                if c == '|' or c == '%':
                    break
                maxIBU += c
    return minIBU, maxIBU

def cleanupSingleDecimalStrings(string):

    if string != '' or string != None:
        newString = re.sub('[a-zA-Z()\s$/%:]', '', string)
    return newString
    

def openSubCategoryPages(currentCategory, dr, site, key):

    # open pages of sub categories to get to list of beer   
    currentSite = site + currentCategory.getCategory_href()
    dr.execute_script("window.open(''); ")
    dr.switch_to.window(dr.window_handles[1])
    dr.get(currentSite)
    time.sleep(3)

    allHTML = BeautifulSoup(dr.page_source, 'html.parser')

    # details of beer style can be found in first <div> tag of <div id="ba-content">
    detailsTag = allHTML.find('div', {'id' : 'ba-content'})
    detailsTag = detailsTag.findAll('div')[0]
    currentCategory.setCategoryDescription(detailsTag.get_text())
    decimals = detailsTag.findAll('span')
    minABV, maxABV = cleanupDoubleDecimalStrings(decimals[0].get_text())
    minIBU, maxIBU = cleanupDoubleDecimalStrings(decimals[1].get_text())
    try:
        currentCategory.setCategoryMinABV(float(minABV))
        currentCategory.setCategoryMaxABV(float(maxABV))
    except:
        print('had an issue getting ABV in ' + currentCategory.getCategoryName())
        currentCategory.setCategoryManualEditFlag(True)
    try:
        currentCategory.setCategoryMinIBU(float(minIBU))
        currentCategory.setCategoryMaxIBU(float(maxIBU))
        currentCategory.setCategoryManualEditFlag(True)
    except:
        print('had an issue getting IBU in ' + currentCategory.getCategoryName())
    
    # only one tbody tag that holds line items of beer
    tbodyTag = allHTML.find('tbody')
    trTags = tbodyTag.findAll('tr')
    # the first three <tr> tags are as follows
    # tag 1: non-important
    # tag 2: links to the next 50 beers, not important yet.
    # tag 3: table headers allowing for re-ordering of beers, not very important
    # tag 4: start of beers, very important.
    # ...
    # ...
    # tag last: links to get to next 50 beers, very important.
    # starting at index 3, we will get the beer information available on this page.

    # this is where we go to each beer's individual website.
    
    index = 3 
    maxCount = len(trTags) - 2
    while index < maxCount:
        key += 1
        current_href = trTags[index].find('a')['href']
        # open pages of sub categories to get to list of beer   
        currentSite = site + current_href
        dr.execute_script("window.open(''); ")
        dr.switch_to.window(dr.window_handles[2])
        dr.get(currentSite)
        time.sleep(3)
        thisBeerHTML = BeautifulSoup(dr.page_source, 'html.parser')
        thisBeer = BeerClass.Beer()
        # since beerName is name of beer and name of brewery on the same string,
        # we get the the breweryName and sub out of beerName
        beerName = thisBeerHTML.find('div', {'class': 'titleBar'})
        breweryName = beerName.find('span').get_text()
        beerName = beerName.get_text()
        beerName = re.sub(breweryName, '', beerName)
        thisBeer.setBeerName(beerName)
        thisBeer.setBeerBrewery(breweryName)
        thisBeer.setBeerKey(key)
        thisBeer.setBeerCategoryKey(currentCategory.getCategoryKey())
        thisBeer.setBeerStyle(currentCategory.getCategoryName())
        # for finding beer stats
        beerStats = thisBeerHTML.findAll('dd', {'class': 'beerstats'})
        abv = cleanupSingleDecimalStrings(beerStats[1].get_text())
        try:
            thisBeer.setBeerABV(float(abv))
        except:
            print(thisBeer.getBeerName() + ' does not have an ABV on the website.\nSubstituting with the category average ABV')
            try:
                thisBeer.setBeerABV((float(minABV) + float(maxABV)) / 2)
            except:
                thisBeer.setBeerManualEditFlag(True)
        thisBeer.setBeerAverageRating(float(beerStats[3].find('span', {'class': 'ba-ravg Tooltip'}).get_text()))
            
        # for finding notes
        notes = thisBeerHTML.find('div', {'style': 'clear:both; margin:0; padding:0px 20px; font-size:1.05em;'})
        thisBeer.setBeerDescription(notes.get_text())
        try:
            thisBeer.setBeerMinIBU(float(minIBU))
            thisBeer.setBeerMaxIBU(float(maxIBU))
        except:
            thisBeer.setBeerManualEditFlag(True)
        # for finding all beer reviews
        beerReviews = thisBeerHTML.findAll('div', {'id': 'rating_fullview_content_2'})
        for each in beerReviews:
            thisBeer.addBeerReviewsFullContent(each.get_text())
        
        currentCategory.addCategoryBeer(thisBeer)
    
        dr.close()
        dr.switch_to.window(dr.window_handles[1])
        index += 1
    
    dr.close()
    dr.switch_to.window(dr.window_handles[0])

    # save to a new excel document after each category is scraped
    # because SPECTRUM...
    wb = Workbook()
    addStyleToNewWorkbook(wb, currentCategory, currentCategory.getCategoryName(), currentCategory.getCategoryKey(), index = 0)
    name = re.sub('\/', 'and',currentCategory.getCategoryName())
    file = 'Scrape\\'
    openFile = file + name + '.xlsx'
    wb.save(openFile)


    return key

#*******************************************************************************************************************************
# Manual Key Reassignment to individual beers so that each beer is garaunteed a unique key

def reassignKeys(root):
    key = 0
    for category in root.getSubCategories():
        for subCategory in category.getSubCategories():
            for beer in subCategory.getCategoryBeers():
                key += 1
                beer.setBeerKey(key)
    return root

#**********************************************************************************************************************************
# set of functions build keyword data banks

def compileWordCounts(root):

    invalidWords = []
    file = open('omitted words.txt', 'r')
    for word in file:
        word = re.sub('\n', '', word)
        invalidWords.append(word)
        
    # dictionary for all of the words in the category.
    # it gets broken down into sub categories
#    categoryWordCountDictionary = {}     # will house dictionaries in category
    subCategoryWordCountDictionary = {}  # will house dictionaries in sub category
#    currentBeerWordCountDictionary = {}
    
    # for getting category word dictionaries of words
    for category in root.getSubCategories():        
        # for getting sub category dictionaries of words
        for subCategory in category.getSubCategories():
#            subCategoryWordCountDictionary = {}  # will house dictionaries in sub category
            # gets words from the description of the sub category
            # as stated by BeerAdvocate                    
            # for getting beer dictionaries of words           
            for beer in subCategory.getCategoryBeers():                
                currentBeerWordCountDictionary = {} # empty dictionary of word count for current beer
                # gets words from the description of the beer
                # as stated by the brewery
                allWords = beer.getBeerDescription()
                allWords = re.sub('[^A-Za-z]+', ' ', allWords)
                allWords = allWords.lower()
                currentWord = ''
                for c in allWords:
                    if c == ' ' and currentWord != '':
                        
                        isValid = True
                        for invalid in invalidWords:
                            if currentWord == invalid:
                                isValid = False
                                break
                            
                        if isValid == True:
                            if currentWord in currentBeerWordCountDictionary:
                                count = currentBeerWordCountDictionary[currentWord]
                                count += 1
                                currentBeerWordCountDictionary[currentWord] = count
                            else:
                                currentBeerWordCountDictionary[currentWord] = 1
                        currentWord = ''
                        
                    else:
                        currentWord += c
                        
                # then we get the words from all of the reviews
                # left by users on BeerAdvocate
                for review in beer.getBeerReviewsFullContent():
                    allWords = review
                    allWords = re.sub('[^A-Za-z]+', ' ', allWords)
                    allWords = allWords.lower()
                    currentWord = ''
                    for c in allWords:
                        if c == ' ' and currentWord != '':
                            
                            isValid = True
                            for invalid in invalidWords:
                                if currentWord == invalid:
                                    isValid = False
                                    break

                            if isValid == True:
                                if currentWord in currentBeerWordCountDictionary:
                                    count = currentBeerWordCountDictionary[currentWord]
                                    count += 1
                                    currentBeerWordCountDictionary[currentWord] = count
                                else:

                                    currentBeerWordCountDictionary[currentWord] = 1
                            currentWord = ''
                        else:
                            currentWord += c
                currentBeerWordCountDictionary = sorted(currentBeerWordCountDictionary.items(), key=lambda x: x[1], reverse=True)
                beer.setBeerWordCount(currentBeerWordCountDictionary)

            # here we will add all of the beer words to the sub category words so that we can build a profile of the categories as well
            for word in currentBeerWordCountDictionary:
                if word[0] in subCategoryWordCountDictionary:
                    count = subCategoryWordCountDictionary[word[0]]
                    count += word[1]
                    subCategoryWordCountDictionary[word[0]] = count
                else:
                    subCategoryWordCountDictionary[word[0]] = word[1]
            subCategory.setCategoryFeaturesMatrix(subCategoryWordCountDictionary)
    return root


#*************************************************************************************************************************************
# function to get a combined word count from all beers.  This is to assist with sifting for beer related words manually

def combineWordCounts(root):
    combineWordCount = {}

    for category in root.getSubCategories():
        for subCategory in category.getSubCategories():
            for beer in subCategory.getCategoryBeers():
                for wordCount in beer.getBeerWordCount():
                    if wordCount[0] in combineWordCount:
                        count = combineWordCount[wordCount[0]]
                        count += wordCount[1]
                        combineWordCount[wordCount[0]] = count
                    else:
                        combineWordCount[wordCount[0]] = wordCount[1]
    combineWordCount = sorted(combineWordCount.items(), key=lambda x: x[1], reverse=True)    
    wb = Workbook()
    categoryName = 'Combine Word Count'
    fileName = 'Keyword Bank\\'
    openFile = fileName + categoryName + '.xlsx'
    wb.active = 0
    sheet = wb.active
    cell = sheet.cell(row = 1, column = 1)
    cell.value = 'Words'
    cell = sheet.cell(row = 1, column = 2)
    cell.value = 'Counts'
    currentRow = 2
    for wordCount in combineWordCount:
        cell = sheet.cell(row = currentRow, column = 1)
        cell.value = wordCount[0]
        cell = sheet.cell(row = currentRow, column = 2)
        cell.value = wordCount[1]
        currentRow += 1
    
    wb.save(openFile)

#***********************************************************************************************************************************
# function to build a features matrix for each beer by comparing word counts with those in the keyword data bank
# each count on a word will impact the order of magnitude for the feature it is stored under

def compileFeaturesDefinitions():

    features = {}    # an array of 19 features, dictionary of word with a magnitude of impact
    
    fileName = 'Keyword Bank\\'
    file = 'Beer Descriptors Simplified.xlsx'
    wb = load_workbook(fileName + file)

    # first we need to load the beer descriptors (features) and their respective impact magnitudes
    index = 0
    wb.active = index
    sheet = wb.active
    currentRow = 1
    currentColumn = 1
    currentCell = sheet.cell(row = currentRow, column = currentColumn)
    while index < 3:
        currentFeature = {}
        featureName = currentCell.value
        currentRow += 1
        currentCell = sheet.cell(row = currentRow, column = currentColumn)
        while currentCell.value != '' and currentCell.value != None:
            
            feature = currentCell.value
            currentColumn += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            impact = int(currentCell.value)
            currentFeature.update({feature : impact})
            
            currentRow += 1
            currentColumn -= 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)

        features.update({featureName : currentFeature})
            
        currentRow = 1
        currentColumn += 2
        currentCell = sheet.cell(row = currentRow, column = currentColumn)

        # if row 2 of the next feature is empty, we know we need to move to the next sheet.
        # and reset the currentCell to 2, 1
        if currentCell.value == '' or currentCell.value == None:
            index += 1
            if index == 3:
                break
            wb.active = index
            sheet = wb.active
            currentRow = 1
            currentColumn = 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)

    # next we iterate through the word counts of each beer and keep the words that match those in beerDescriptors.
    return features

# This function cycles through each feature's list of keywords (definition of features if you will)
# If a word from the beer's word count matches the feature's keyword, then it adds plus 1 to the feature matrix for that feature
# matrix: [astringent, mouthfeel, alcohol, bitter, sweet, sour, salty, fruity, hoppy, spicy, malty]
def wordCountToFeatures(root, features):

    for category in root.getSubCategories():
        for subCategory in category.getSubCategories():
            for beer in subCategory.getCategoryBeers():   
                matrixOfBeerFeatures = []           # n x 1 matrix
                for feature, impact in features.items():
                    magnitudeOfCurrentFeature = 0
                    for word in beer.getBeerWordCount():
                        for key in impact:
                            if word[0] == key:
                                magnitudeOfCurrentFeature += (int(word[1]) * int(impact[key]))
                    matrixOfBeerFeatures.append(magnitudeOfCurrentFeature)
                beer.setBeerFeaturesMatrix(matrixOfBeerFeatures)

    # here we calculate the features matrix for sub categories or styles
    # we sum up the features matrices of all beer in the sub category and divide by the number of beers in that sub category or style
    # we find the mean features matrix that represents the sub category or style.

    for category in root.getSubCategories():
        for subCategory in category.getSubCategories():
            matrixOfSubCategoryFeatures = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for beer in subCategory.getCategoryBeers():
                matrixOfSubCategoryFeatures = np.add(matrixOfSubCategoryFeatures, beer.getBeerFeaturesMatrix())
            matrixOfSubCategoryFeatures = matrixOfSubCategoryFeatures // len(subCategory.getCategoryBeers())
            subCategory.setCategoryFeaturesMatrix(matrixOfSubCategoryFeatures)
    
    return root

#***************************************************************************************************************************************
# Functions to gather data on select user inputs and store the data in a file.

def gatherUserInputInformation():

    startPage = 'https://www.beeradvocate.com/'
    beerURLs = ['beer/profile/148/11436/',      # Scottish Ale 80 Shillings
                'beer/profile/335/2904/',       # IPA American Mad Hatter
                'beer/profile/199/178740/',     # IPA American Sculpin Pineapple
                'beer/profile/31987/194673/',   # Stout Oatmeal Black House Nitro
                'beer/profile/137/30936/',      # Fruit and Field Apricot
                'beer/profile/3760/9781/',      # Porter American Coffee Porter
                'beer/profile/179/71896/',      # Sour - Flanders Oud Bruin Le Serpent Cerise
                'beer/profile/192/275731/',     # Wheat Beer Witbier Fat Tire Belgian White
                'beer/profile/8/46767/',        # Pale Ale American Drifter
                'beer/profile/26762/76498/']    # Porter Imperial Hellfighter

    dummyParent = BeerCategoryClass.BeerCategory()
    userCategory = BeerCategoryClass.BeerCategory()

    dummyParent.setCategoryName('')
    dummyParent.setCategoryKey(-1)
    
    userCategory.setCategoryName('User Input')
    userCategory.setCategoryKey(100)
    userCategory.setCategoryParent(dummyParent)
    userCategory.setCategoryParentKey(-1)

    key = 9000

    for currentBeerURL in beerURLs:
        currentSite = startPage + currentBeerURL
        thisBeerHTML = seleniumGetsHTML(currentSite)
        key += 1
        
        thisBeer = BeerClass.Beer()
        # since beerName is name of beer and name of brewery on the same string,
        # we get the the breweryName and sub out of beerName
        beerName = thisBeerHTML.find('div', {'class': 'titleBar'})
        breweryName = beerName.find('span').get_text()
        beerName = beerName.get_text()
        beerName = re.sub(breweryName, '', beerName)
        thisBeer.setBeerName(beerName)
        thisBeer.setBeerBrewery(breweryName)
        thisBeer.setBeerKey(key)
        # for finding beer stats
        beerStats = thisBeerHTML.findAll('dd', {'class': 'beerstats'})
        beerStyle = beerStats[0].find('a').get_text()
        thisBeer.setBeerStyle(beerStyle)

        # to get the category key, we will navigate through all of the styles and find the name that matches the name of this beer's style.

        excelList = os.listdir(FILE_DIRECTORY + BEER_ALL_INFO)
        desiredFile = ''
        for excel in excelList:
            if excel == beerStyle:
                desiredFile = BEER_ALL_INFO + file + '.xlsx'
                wb = load_workbook(desiredFile)
                wb.active = 1
                sheet = wb.active
                thisBeer.setBeerCategoryKey(sheet.cell(row = 2, column = 2).value) # find a way to fix this
                break
        

        
        abv = cleanupSingleDecimalStrings(beerStats[1].get_text())
        try:
            thisBeer.setBeerABV(float(abv))
        except:
            print(thisBeer.getBeerName() + ' does not have an ABV on the website.\nSubstituting with the category average ABV')
            try:
                thisBeer.setBeerABV((float(minABV) + float(maxABV)) / 2)
            except:
                thisBeer.setBeerManualEditFlag(True)
        thisBeer.setBeerAverageRating(float(beerStats[3].find('span', {'class': 'ba-ravg Tooltip'}).get_text()))
            
        # for finding notes
        notes = thisBeerHTML.find('div', {'style': 'clear:both; margin:0; padding:0px 20px; font-size:1.05em;'})
        thisBeer.setBeerDescription(notes.get_text())
#        try:
#            thisBeer.setBeerMinIBU(float(minIBU))
#            thisBeer.setBeerMaxIBU(float(maxIBU))
#        except:
#            thisBeer.setBeerManualEditFlag(True)
        # for finding all beer reviews
        beerReviews = thisBeerHTML.findAll('div', {'id': 'rating_fullview_content_2'})
        for each in beerReviews:
            thisBeer.addBeerReviewsFullContent(each.get_text())
        
        userCategory.addCategoryBeer(thisBeer)

        
    invalidWords = []
    file = open('omitted words.txt', 'r')
    for word in file:
        word = re.sub('\n', '', word)
        invalidWords.append(word)
        
    for beer in userCategory.getCategoryBeers():                
        currentBeerWordCountDictionary = {} # empty dictionary of word count for current beer
        # gets words from the description of the beer
        # as stated by the brewery
        allWords = beer.getBeerDescription()
        allWords = re.sub('[^A-Za-z]+', ' ', allWords)
        allWords = allWords.lower()
        currentWord = ''
        for c in allWords:
            if c == ' ' and currentWord != '':
                            
                isValid = True
                for invalid in invalidWords:
                    if currentWord == invalid:
                        isValid = False
                        break
                                
                if isValid == True:
                    if currentWord in currentBeerWordCountDictionary:
                        count = currentBeerWordCountDictionary[currentWord]
                        count += 1
                        currentBeerWordCountDictionary[currentWord] = count
                    else:
                        currentBeerWordCountDictionary[currentWord] = 1
                currentWord = ''
                            
            else:
                currentWord += c
                            
        # then we get the words from all of the reviews
        # left by users on BeerAdvocate
        for review in beer.getBeerReviewsFullContent():
            allWords = review
            allWords = re.sub('[^A-Za-z]+', ' ', allWords)
            allWords = allWords.lower()
            currentWord = ''
            for c in allWords:
                if c == ' ' and currentWord != '':
                                
                    isValid = True
                    for invalid in invalidWords:
                        if currentWord == invalid:
                            isValid = False
                            break

                    if isValid == True:
                        if currentWord in currentBeerWordCountDictionary:
                            count = currentBeerWordCountDictionary[currentWord]
                            count += 1
                            currentBeerWordCountDictionary[currentWord] = count
                        else:

                            currentBeerWordCountDictionary[currentWord] = 1
                    currentWord = ''
                else:
                    currentWord += c
        currentBeerWordCountDictionary = sorted(currentBeerWordCountDictionary.items(), key=lambda x: x[1], reverse=True)
        beer.setBeerWordCount(currentBeerWordCountDictionary)

                
    beerFeatures = compileFeaturesDefinitions()
    
    for beer in userCategory.getCategoryBeers():   
        matrixOfBeerFeatures = []           # n x 1 matrix
        for feature, impact in beerFeatures.items():
            magnitudeOfCurrentFeature = 0
            for word in beer.getBeerWordCount():
                for key in impact:
                    if word[0] == key:
                        magnitudeOfCurrentFeature += (int(word[1]) * int(impact[key]))
            matrixOfBeerFeatures.append(magnitudeOfCurrentFeature)
        beer.setBeerFeaturesMatrix(matrixOfBeerFeatures)

    wb = Workbook()
    addStyleToNewWorkbook(wb, userCategory, userCategory.getCategoryName(), userCategory.getCategoryKey(), index = 0)
    name = re.sub('\/', 'and',userCategory.getCategoryName())
    file = 'Scrape\\'
    openFile = file + name + '.xlsx'
    wb.save(openFile)



#********************************************************************************************************************************
# this function loads the basic information for all 5700 beer for machine learning application
# with the option to load user beer input from file as well.
def loadBeerInformation(getUser = False, getCategoryDictionary = False):

    beerList = []
    if getCategoryDictionary == True:
        dictionary = {}

    # first we need to see if the name of the categories we want to collect data from exist as files
    fileList = os.listdir(FILE_DIRECTORY + BEER_ALL_INFO)
    print('Gathering File Names..')
    fileName = BEER_ALL_INFO
    for file in fileList:
        wb = load_workbook(fileName + file)
        if getCategoryDictionary == True:
            index = 0
            wb.active = index
            sheet = wb.active
            dictionary[float(sheet.cell(row = 2, column = 2).value)] = str(sheet.cell(row = 1, column = 2).value)
        
        index = 1
        print('Getting beer information from ' + file)
        while index < len(wb.worksheets):
            beer = BeerClass.Beer()            
            wb.active = index
            sheet = wb.active
            currentRow = 1
            currentColumn = 2
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerName(re.sub('\n','',currentCell.value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerKey(int(currentCell.value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerStyle(re.sub('\n','',currentCell.value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerCategoryKey(int(currentCell.value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerBrewery(re.sub('\n','',currentCell.value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerAverageRating(float(currentCell.value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerABV(float(currentCell.value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerMinIBU(int(currentCell.value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerMaxIBU(int(currentCell.value))

            features = []
            currentRow = BEER_FEATURES_START_ROW
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            while currentCell.value != '' and currentCell.value != None:
                features.append(int(currentCell.value))
                currentRow += 1
                currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerFeaturesMatrix(features)
            beerList.append(beer)
            index += 1

    if getUser == True:
            
        userInputFile = 'User Input\\User Input.xlsx'
        wb = load_workbook(userInputFile)
        index = 1
        wb.active = index
        sheet = wb.active

        userBeerList = []
        userCV = []

        while index < len(wb.worksheets):        
            beer = BeerClass.Beer()
            beerCV = BeerClass.Beer()
            wb.active = index
            sheet = wb.active
            currentRow = 1
            currentColumn = 2
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerName(re.sub('\n','',currentCell.value))
            beerCV.setBeerName(re.sub('\n','',currentCell.value) + ' :: Cross Validation')
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerKey(int(currentCell.value))
            beerCV.setBeerKey(int(currentCell.value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerStyle(re.sub('\n','',currentCell.value))
            beerCV.setBeerStyle(re.sub('\n','',currentCell.value) + ' :: Cross Validation')
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerCategoryKey(int(currentCell.value))
            beerCV.setBeerCategoryKey(int(currentCell.value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerBrewery(re.sub('\n','',currentCell.value))
            beerCV.setBeerBrewery(re.sub('\n','',currentCell.value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerAverageRating(float(currentCell.value))
            beerCV.setBeerAverageRating(float(currentCell.value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerABV(float(currentCell.value))
            beerCV.setBeerABV(float(currentCell.value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerMinIBU(int(currentCell.value))
            beerCV.setBeerMinIBU(int(currentCell.value))
            currentRow += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerMaxIBU(int(currentCell.value))
            beerCV.setBeerMaxIBU(int(currentCell.value))

            features = []
            featuresCV = []
            currentRow = BEER_FEATURES_START_ROW
            currentCell = sheet.cell(row = currentRow, column = currentColumn)
            while currentCell.value != '' and currentCell.value != None:
                features.append(int(currentCell.value))
                featuresCV.append(int(currentCell.value + 1))
                currentRow += 1
                currentCell = sheet.cell(row = currentRow, column = currentColumn)
            beer.setBeerFeaturesMatrix(features)
            beerCV.setBeerFeaturesMatrix(features)
            userBeerList.append(beer)
            userCV.append(beerCV)
            index += 1
        if getCategoryDictionary == True:
            return beerList, userBeerList, userCV, dictionary
        else:
            return beerList, userBeerList, userCV
    return beerList

###*******************************************************************************************************************************
# Functions to run K Nearest Neighbor

# data will be a dictionary of beer, with beer keys being key and values being features
# predict is the user's chosen beer to compare with
# k is the number of neighbors we will be looking for.


def calculateEuclideanDistance(data, predict):

    euclideanDistance = np.linalg.norm(np.array(data) - np.array(predict))

    return euclideanDistance


#*****************************************************************************************************************************
# calculates all neighbors from data in dictionaries

def calculateAllNN(data, predict):

    results = {}

    # iterate through each user input of enjoyed beers
    for ukey, uval in predict.items():
        distances = []

        # for each of the 5600 beers in our data, determine the distance between the current user input
        for bkey, bval in data.items():
            distances.append([calculateEuclideanDistance(bval, uval), bkey, bval])
            
        # sort by shortest distance to the current user input
        distances = sorted(distances)

        ukeyValues = {}
        for dist in distances:
            ukeyValues.update({dist[1]: dist[0]})
        results.update({ukey: ukeyValues})
    return results


#**********************************************************************************************************************************
# functions to print recommendations based on each  userPredict beer.

def printBNearestNeighbors(data, aBeer, k, userInput):

    for dKey, dVal in data.items():
        knn = {}
        currentUserInputBeer = BeerClass.Beer()
        for userIn in userInput:
            if userIn.getBeerKey() == dKey:
                currentUserInputBeer = userIn
                break
        print('*************************************************************')
        print('\nRecommendations based on ' + currentUserInputBeer.getBeerName())
        print('Style:        ' + currentUserInputBeer.getBeerStyle())
        print(currentUserInputBeer.getBeerFeaturesMatrix())
        # match the key collected from allNN result to the list of beers that are in the allBeer list and print the data.
        counter = 0
        atK = False
        knn.update({currentUserInputBeer.getBeerName(): currentUserInputBeer.getBeerFeaturesMatrix()})
        for bkey, bvalues in dVal.items():
            for beer in aBeer:
                if bkey == beer.getBeerKey():
                    print('\nName:         ' + str(beer.getBeerName()))
                    print('Style:        ' + str(beer.getBeerStyle()))
                    print('Feature Dist: ' + str(bvalues))
                    print(beer.getBeerFeaturesMatrix())
                    knn.update({beer.getBeerName(): beer.getBeerFeaturesMatrix()})
                    counter += 1
                    if counter == k:
                        atK = True
                    break
            if atK == True:
                break
        graphRecommendations(knn)
#   knn = {'user Input Beer 1 Name': { 'user Input Beer 1 Name': [user input features]}, {'Recommendation 1': [recommendation 1 features]}, ..., {'Recommendation N': [recommendation N features]}}
#    return knn

#******************************************************************************************************************
# Graphing the user input features and the b nearest neighbors recommended.


def graphRecommendations(data):
    fig = plt.figure(figsize = (12, 12))
    ax = plt.subplot(polar = 'True')    
    MAX_NUMBER_OF_FEATURES = 11
    featureLabels = ['Astringency', 'Body', 'Alcoholic', 'Bitter', 'Sweet', 'Sour', 'Salty', 'Fruity', 'Hoppy', 'Spice', 'Malty']   
    color = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'brown', 'coral', 'darkgreen', 'gold', 'fuchsia', 'lightblue', 'maroon', 'teal', 'violet']
    currentColor = -1
    dataNames = []
    title = list(data.keys())[0]
    # here we unpack our data.
#   knn = {'user Input Beer 1 Name': [[user input features], {'Recommendation 1': [recommendation 1 features]}, ... , {'Recommendation N': [recommendation N features]}]}
    for name, features in data.items():
        dataNames.append(name)      # for legend chart
        # next we need to caluclate the angles for each feature
        angles = [n / float(MAX_NUMBER_OF_FEATURES) * 2 * pi for n in range(MAX_NUMBER_OF_FEATURES)]
        try:
            # we need to complete the polygon by adding the starting feature at the end.
            features += features[:1]
            # and we need to repate the first value to complete the circle
            angles += angles[:1]
        except:
            print('an error occurred in graphing')
            continue
        try:
            currentColor += 1
            plt.polar(angles, features, marker = '.', color = color[currentColor], label = name)
            
        except:
            print('something happened in plt.polar')
            continue
#   Fills the polygon that has been drawn onto the grid.
#    plt.fill(angles, features, alpha = 0.1)

        plt.xticks(angles[:-1], featureLabels)
    
    ax.set_rlabel_position(0)
    plt.yticks([25, 50, 75, 100, 125, 150], color = 'grey', size = 10)
    plt.ylim(0, 200)
    plt.title(title)
    legend = ax.legend(loc = 'upper right')
    fig.savefig('recommendations for ' + title + '.png')
    plt.show()


#******************************************************************************************************************
# function to classify the user input's beer style using KNN
# this function returns KNN distances and classification label.

def classifyNewBeerUsingBeerObjects(aBeer, nBeer, k):    

    distancesAll = []
    for beer in aBeer:
    # distancesAll = [euclideanDistance, beerKey, beerStyleKey]
        distancesAll.append([calculateEuclideanDistance(beer.getBeerFeaturesMatrix(), nBeer.getBeerFeaturesMatrix()), beer.getBeerKey(), beer.getBeerStyle()])
    distancesSorted = sorted(distancesAll)   # sort the distances by distance from shortest to longest
    distancesKNN = distancesSorted[:k]
    distancesKNN = np.array(distancesKNN)
    mostLabelsInDistancesKNN = Counter(distancesKNN[:,2]).most_common(1)[0][0]
    
    return distancesKNN, mostLabelsInDistancesKNN


#*********************************************************************************************************************
# Data Setup for KNN algorithms:
# Set up our numpy arrays for KNN algorithms
# beerFeatures = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11]
# beerStyle = [y]
# where xN is the feature from the features matrix

def dataSetup(listOfBeerIn, yAvailable = False):

    beerFeatures = np.empty(11)
    if yAvailable == True:
        beerStyle = np.empty(1)
    
    for beer in listOfBeerIn:
        xrow = np.array(beer.getBeerFeaturesMatrix())
#        print('xrow.shape')#
#        print(xrow.shape)
#        print('beerFeatures.shape before stacking')
#        print(beerFeatures.shape)
        beerFeatures = np.vstack((beerFeatures, xrow))        
#        print('beerFeatures.shape after stacking')
#        print(beerFeatures.shape)
        if yAvailable == True:
            yrow = np.array(beer.getBeerCategoryKey())
            beerStyle = np.vstack((beerStyle, yrow))

    # we need to delete the first row that came from np.empty, I guess..

    beerFeatures = np.delete(beerFeatures, 0, 0)
    if yAvailable == True:
        beerStyle = np.delete(beerStyle, 0, 0)

    if yAvailable == True:
        return beerFeatures, beerStyle
    return beerFeatures
        

#*******************************************************************************************************************
# classify beer using a list of type [array(beer.getBeerFeaturesMatrix()), style key]
# this will hopefully save some time.

def getSortedDistancesUsingNumpy(aBeer, nBeer, style):


    # calculate euclidean distance between new beer and each beer in all beer.
    euclideanDistance = np.array([ np.linalg.norm(a - nBeer) for a in aBeer])
    euclideanDistance = euclideanDistance.reshape((euclideanDistance.shape[0], 1))
    # aftcalculating euclidean distance, we append the corresponding styles to the array.
    distancesAll = np.append(euclideanDistance, style, axis = 1)
    distancesSorted = distancesAll[distancesAll[:,0].argsort()]   # sort the distances by distance from shortest to longest
    return distancesSorted
    

#********************************************************************************************************************
# Optimizing K

def optimizeKUsingNumpy(data, style, maxTrainingLabelsCount):

    highestAccuracyAtK = [0] * len(data)
    accuracyLimit = .8
    K = []
#    counter = -1
    for currentData, currentStyle in zip(data, style):
#        counter += 1
#        print('\nOptimizing K using data at index ' + str(counter))
#        print('currentStyle')
#        print(currentStyle)
        allSortedDistances = getSortedDistancesUsingNumpy(data, currentData, style)[1:]
        currentK = []        
        for k in range(1, len(data)):      
            distancesKNN = allSortedDistances[:k]
            labelsKNN = np.array(distancesKNN)[:,-1]
            correctLabelsCounted = (labelsKNN == currentStyle).sum()      
            total = len(distancesKNN)
            accuracy = correctLabelsCounted / total
#            if accuracy >= accuracyLimit:  # we will omit k with accuracies less than accuracyLimit
            currentK.append([accuracy, k, currentStyle])
            if accuracy > highestAccuracyAtK[k]:
                highestAccuracyAtK[k] = accuracy
        # once we reach the maximum number of labels in the data set, accuracy will only decline from here, so we break
            if correctLabelsCounted == maxTrainingLabelsCount:
                break

        currentK = sorted(currentK, reverse = True)
#        print('Best Accuracies and K:  ')
#        print('Accuracy  k')
#        print(currentK[0])
        if currentK[0][1] not in K and currentK[0][0] > accuracyLimit:
            K.append(int(currentK[0][1]))
    # here we want to get the most common accuracy for each k in K from frequencyOfAccuracyAtEachK.      
    fig, ax = plt.subplots()
    accLength = 100
    ax.plot(range(1, accLength), highestAccuracyAtK[1:accLength])
    ax.set(xlabel = 'k values', ylabel = 'accuracy at k', title = 'Accuracy of a value k during Training')
    ax.grid()
    fig.savefig('Accuracy of a value k during Training.png')
    plt.show()
    K = sorted(K)
    print('\nOptimized K values based on highest accuracy: ')
    print(K)
    return K
    

#***************************************************************************************
# function to test our optimized K values

def testOptimizedKUsingNumpy(data, style, K):

    # results will be [[k, highest accuracy, average accuracy, lowest accuracy]]    
    highestAccuracyAtK = []
    for k in K:
        highestAccuracyAtK.append([k, float(0)])
#    indexCounter = -1
    for currentData, currentStyle in zip(data, style):
#        indexCounter += 1
#        print('\nTesting K using data at index ' + str(indexCounter))
#        print('currentStyle')
#        print(currentStyle)        
        allSortedDistances = getSortedDistancesUsingNumpy(data, currentData, style)[1:]
        currentK = []
        accuracyIndexer = -1
        for k in K:
            accuracyIndexer += 1              
            distancesKNN = allSortedDistances[:k]            
            labelsKNN = np.array(distancesKNN)
            correctLabelsCounted = (labelsKNN == currentStyle).sum()                  
            total = len(distancesKNN)
            accuracy = correctLabelsCounted / total    
            currentK.append([accuracy, k])
            if highestAccuracyAtK[accuracyIndexer][1] < accuracy:
                highestAccuracyAtK[accuracyIndexer][1] = float(accuracy)
        currentK = sorted(currentK, reverse = True)        
#        print('Best Accuracies and K:  ')
#        print('Accuracy    k')
#        print(np.array(currentK))
    print('\nHighest accuracies at K')
    print(np.array(highestAccuracyAtK))
    fig, ax = plt.subplots()
    accLength = 40
    x = np.array(highestAccuracyAtK)[:, 0]
    y = np.array(highestAccuracyAtK)[:, 1]
    ax.plot(x, y)
    ax.set(xlabel = 'k values', ylabel = 'accuracy at k', title = 'Testing Accuracy of optimized k values')
    ax.grid()
    fig.savefig('Testing Accuracy of optimized k values.png')
    plt.show()
    K = sorted(K)
    print('\nOptimized K values based on highest accuracy: ')
    print(K)

#**************************************************************************************************
# Function to classify a new beer based on optimized K nearest neigbors.

def classifyANewBeerUsingNumpy(aBeerFeatures, aBeerStyles, uBeerFeatures, K, name, classDictionary):
    
    allSortedDistances = getSortedDistancesUsingNumpy(aBeerFeatures, uBeerFeatures, aBeerStyles)
    accuracyIndexer = -1
    mostCommonStylesAtK = []
    graphingData = {} 
    for k in K:
        distancesKNN = allSortedDistances[:k]
        labelsKNN = np.array(distancesKNN) 
        mostLabelsInDistancesKNN = Counter(labelsKNN[:,1]).most_common(1)
        mostCommonStylesAtK.append([k, mostLabelsInDistancesKNN[0][0], distancesKNN])
        dist = []
        style = []
        for i in distancesKNN:
            dist.append(i[0])
            style.append(i[1])
        graphingData.update({k: [dist, style]})
    graphClassifications(graphingData, name, classDictionary)
    return mostCommonStylesAtK

#*****************************************************************************************************************
# function that graphs the features of a new beer and the features using colors to represent classifications of the k nearest neighbors. 

def graphClassifications(data, title, classDictionary):
    
    color = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'brown', 'coral', 'darkgreen', 'gold', 'fuchsia', 'lightblue', 'maroon', 'teal', 'violet']
    # here we unpack our data.
    x_kValues = []
    y_distances = []
    z_classifications = []
    z_classificationsColor = {}
    for k, dist_style in data.items():
        x_kValues.append(k)
        y_distances = [d for d in dist_style[0]]
        z_classifications = [c for c in dist_style[1]]

    
    uniqueClassifications = list(set(z_classifications))
    colorIndex = 0
    for i in uniqueClassifications:
        z_classificationsColor.update({i: [color[colorIndex], classDictionary[i]]})
        colorIndex += 1

    fig, ax = plt.subplots()
    for x in range(0, len(x_kValues)):
        classificationIndex = int(z_classifications[x])
        label = z_classificationsColor[classificationIndex][1]
        classColor = z_classificationsColor[classificationIndex][0]
        ax.scatter(x_kValues[x], y_distances[x], s = 20, label = label, color = classColor)
        plt.plot([x + 1, x_kValues[x]], [0, y_distances[x]], color = classColor)

    plt.title(title)
    legend = ax.legend(bbox_to_anchor=(1.05, 1), loc = 'upper left')
    ax.set(xlabel = 'k values', ylabel = 'distance')
    fig.savefig('Classification of ' + title + '.png')
    plt.show()
    
#******************************************************************************************************************
# Main Menu Functions
    
def treeMenuOptions():
    # our tree object where we append the nodes and their respective data values.
    BeerCategoryTree = BeerCategoryClass.BeerCategory()

    beerURL = 'https://www.beeradvocate.com/'
    
    choice = -1
    while choice < 0 or choice > 7:
        print('\nData Collection')
        print('0. Go back: this will erase all loaded data')
        print('1. Build Empty Tree: build empty tree used to scrape website for information')
        print('2. Load Tree: load information from files for all beer styles and beer into the tree')
        print('3. Print Category Tree: print the tree of beer styles and unique keys to screen')
        print('4. Save Tree: save the tree to multiple excel files')
        print('5. Scrape for Items: scrape website for items in each category and add to empty tree.\n   This also saves the data during the process incase of internet drops')
        print('6. Manual Key Reassignment: reassigns keys to each beer in saved files\n   Due to internet interruptions, multiple beers may have the same key')
        print('7. Word Count Options: display a list of options for word counts')
        print('8. Get User Input Beer: scrape information for user input beer and store in file')
        try:
            choice = int(input())
        except:
            print('\nInvalid choice, please choose wisely.')
        if(choice == 1):
            beerURL = 'https://www.beeradvocate.com'
            print('\nBuilding category tree..\n')
            # gets the html via selenium and beautifulsoup combination
            # since we are starting a '/beer/styles', we will go ahead and append that
            # here to get the html for that page.
            customStartingPoint = '/beer/styles'
            soupSource = seleniumGetsHTML(beerURL + customStartingPoint)
            # get the tree's starting node.
            BeerCategoryTree = buildTree(soupSource, beerURL)
            print('\nTree has been built!')
            
        elif(choice == 2):
            # if option two is chosen and the tree has not been built, build the tree first.
            if BeerCategoryTree.getCategoryKey() == -1:
                beerURL = 'https://www.beeradvocate.com'
                print('\nBuilding category tree..\n')
                # gets the html via selenium and beautifulsoup combination
                # since we are starting a '/beer/styles', we will go ahead and append that
                # here to get the html for that page.
                customStartingPoint = '/beer/styles'
                soupSource = seleniumGetsHTML(beerURL + customStartingPoint)
                # get the tree's starting node.
                BeerCategoryTree = buildTree(soupSource, beerURL)
                print('\nTree has been built!')
                
            print('\nLoading beer information into initialized tree from workbooks..')
            BeerCategoryTree = loadSubCategories(BeerCategoryTree)
            
        elif(choice == 3):
            print('\nPrinting category tree to screen..\n')
            print(BeerCategoryTree.getCategoryName())
            printCategoryTree(BeerCategoryTree, 1)
            print('\nTree has been printed!')
            
        elif(choice == 4):
            print('\nSaving to file..')
            createWorkbookForAllCategories(BeerCategoryTree)
            print('\nSaving complete!')
            
        elif(choice == 5):
            beerURL = 'https://www.beeradvocate.com'
            print('\nGathering item information from website ' + beerURL + '..')
            BeerCategoryTree = startGetCategoryItems(BeerCategoryTree, beerURL)
            print('\nGathering of item information Complete!')
            
        elif(choice == 6):
            print('\nStarting key reassignments to beer')
            BeerCategoryTree = reassignKeys(BeerCategoryTree)
            print('\nKey reassignment complete!')
            
        elif(choice == 7):
            
            wordBankChoice = -1
            while wordBankChoice < 0 or wordBankChoice > 4:
                wordBankChoice = -1
                print('\nWord Count Options')
                print('0. Go Back')
                print('1. Compile Word Counts')
                print('2. Save Word Counts to a separate file - NOT YET AVAILABLE')
                print('3. Save combined word count to file')
                print('4. Compile features matrix based on keywords')
                try:
                    wordBankChoice = int(input())
                except:
                    print('\nInvalid choice, please choose wisely.')
                if wordBankChoice == 1:
                    print('\nCompiling Word Counts, this will take a few minutes..')
                    BeerCategoryTree = compileWordCounts(BeerCategoryTree)
                    print('\nWord Count Compile Complete!')
                elif wordBankChoice == 2:
#                    saveWordCountsInCategory(BeerCategoryTree)
                    print('\nThis option is not yet available')
                elif wordBankChoice == 3:
                    print('\nSaving Combined Word Count..')
                    combineWordCounts(BeerCategoryTree)
                elif wordBankChoice == 4:
                    print('\nLoading Features Definitions..')
                    beerFeatures = compileFeaturesDefinitions()
                    print('\nConverting Word Counts To Features, this will take a few minutes..')
                    wordCountToFeatures(BeerCategoryTree, beerFeatures)
                    print('\nConverting Word Counts To Features Complete!')
                if wordBankChoice != 0:
                    wordBankChoice = -1
                else:
                    break

        if choice == 8:
            print('\nGetting User Input Information..')
            gatherUserInputInformation()
            print('\nUser Input Information gathered!')

                
        if choice != 0:
            choice = -1
        else:
            break        

# Main Menu Option 2
def dataMenuOptions():
   
    # empty dictionaries of recommendations based on neighbors to userPredict based on different sets of features.
    # our lists of beer objects
    userInput = userCrossValidation = allBeer = []
    categoryDictionary = {}
    optimizedK = None
    knnResult = []
    knnResultingLabel = None    
    choice = -1
    while choice < 0 or choice > 2:
        print('\nData Options')
        print('0. Go back: this will erase all loaded data')
        print('1. Load Beer Information: load collected beer, user input, and cross validation information')
        print('2. KNN Operations: options for running KNN operations')


        try:
            choice = int(input())
        except:
            print('\nInvalid choice, please choose wisely.')
        if choice == 1:
            print('\nLoading Beer Information..')
            
            allBeer, userInput, userCrossValidation, categoryDictionary = loadBeerInformation(getUser = True, getCategoryDictionary = True)
            AllBeerDict = {}
            for beer in allBeer:
                AllBeerDict[beer.getBeerKey()] = beer.getBeerFeaturesMatrix()
            userInputDict = {}
            for userP in userInput:
                userInputDict[userP.getBeerKey()] = userP.getBeerFeaturesMatrix()
            allNNResult = {}
            
            print('\nLoading Complete')


        elif choice == 2:           
            
            kChoice = -1
            while kChoice < 0 or kChoice > 2:
                print('\nK Nearest Neighbor Options')
                print('0. Go back: this will erase all KNN-related data')
                print('1. Optimize K: function to optimize K')
                print('2. Classify user input using KNN algorithm and optimized K')
                print('3. Run All Nearest Neighbors algorithm')
                print('4. Make Recommendations based on B Nearest Neighbors')
                try:
                    kChoice = int(input())
                except:
                    print('\nInvalid choice, please choose wisely.')

### kChoice == 1: Optimize K
                if kChoice == 1:
                    
                    np.set_printoptions(threshold=np.inf, precision = 3)
                    # Train
                    # Test
                # so we are going to divide our data into training and test sets
                    trainBeerStyleKeys = [0] * 150
                    trainBeer = []
                    testBeerStyleKeys = [0] * 150
                    testBeer = []

                    maxTrainingLabelsCount = 40
                    maxTestingLabelsCount = 10
                    
                    for i in range(0, len(allBeer)):
                        if trainBeerStyleKeys[(allBeer[i].getBeerCategoryKey() - 1)] < maxTrainingLabelsCount:
                            trainBeer.append(allBeer[i])
                            trainBeerStyleKeys[allBeer[i].getBeerCategoryKey() - 1] += 1
                        elif testBeerStyleKeys[(allBeer[i].getBeerCategoryKey() - 1)] < maxTestingLabelsCount:
                            testBeer.append(allBeer[i])
                            testBeerStyleKeys[allBeer[i].getBeerCategoryKey() - 1] += 1
                            
                    shuffledTrainBeer = trainBeer            
                    random.shuffle(shuffledTrainBeer)
                    shuffledTestBeer = testBeer            
                    random.shuffle(shuffledTestBeer)

                    # convert all of our beer data from beer objects to a matrix
        #            beerFeatures_X, beerStyle_y = dataSetup(trainBeer, yAvailable = True)        
                    trainSetFeatures_X, trainSetStyles_y = dataSetup(trainBeer, yAvailable = True)
                    testSetFeatures_X, testSetStyle_y = dataSetup(testBeer, yAvailable = True)

                    print('\nOptimizing K')
                    optimizedK = optimizeKUsingNumpy(trainSetFeatures_X, trainSetStyles_y, maxTrainingLabelsCount)   # this is using list of type [numpy.array(), beerKey], to save time.
                    print('\nOptimizing Complete!')

                    ### for testing purposes
#                    optimizedK = [1,2,3,4,5,7,8,9,0,3,5,34,56]

                    print('\nTesting Optimized K')
                    testOptimizedKUsingNumpy(testSetFeatures_X, testSetStyle_y, optimizedK)
                    print('\nTesting Complete!')

### kChoice == 2: Classify User Input
                elif kChoice == 2:

                    # for testing purposes:
#                    optimizedK = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                    
                    if len(optimizedK) != 0:
                        # this is where we convert allBeer into data and userPredict and userCrossValidation into data sets
                        # we will use allBeer data and optimizedK sets to classify each userPredict and userCrossValidation
                        # we must then graph the results, red for userPredict classification and black for the other classifications??

                        allBeerFeatures_X, allBeerStyles_y = dataSetup(allBeer, yAvailable = True)
                        for beer in userInput:
                            recommendationResultToGraph = {}
                            userBeerFeatures_X = dataSetup([beer])
                            listOfKResults = classifyANewBeerUsingNumpy(allBeerFeatures_X, allBeerStyles_y, userBeerFeatures_X, optimizedK, beer.getBeerName(), categoryDictionary)
                            print('\nBeer Name:      ' +  beer.getBeerName())
                            print('Beer Classifications based on optimized K values:')
                            for kResults in listOfKResults:
                                print('\nK-value:        ')
                                print(kResults[0])
                                print('Style Name:     ')
                                print(categoryDictionary[int(kResults[1])])


                            # here we package up the data to have it graphed.
                    else:
                        print('\nIt might be helpful to run option 1 first..')

                #  Option to run allNNResults for user input and cross validation.

                if kChoice == 3:                    
                    try:
                        # calculate all nearest neighbor distances
                        print('\nRunning all nearest neighbors algorithm on all features..')
                        allNNResult = calculateAllNN(AllBeerDict, userInputDict)
#                        print('\nRunning KNN algorithm on all Cross Validation features')
#                        allNNCrossValidationResult = calculateAllNN(AllBeerDict, userCrossValidationDict)
                        print('\nAll nearest neighbors  calculation complete!')
                    except:
                        print('You need to load your beer data first!')
#  Option to print the allNNResults and cross validation results
                if kChoice == 4:
                    print('\nHow many B recommendations do you want for each input? ')
                    try:
                        b = int(input())
                    except:
                        print('\nInvalid choice, please choose wisely.')
#                    try:
                    print('\nPrinting B Recommendations:')

                    
        ### SOMETHING GOING ON HERE!
                    
                    printBNearestNeighbors(allNNResult, allBeer, b, userInput)
                    print('\nRecommendations complete!')
#                    print('\nPrinting K Nearest Neighbors Cross Validation Results:')
#                    knnCrossValidationResult = printKNearestNeighbors(allNNCrossValidationResult, allBeer, k, userCrossValidation)
#                    except:
#                        print('\nWe need to run KNN algorithm first!')

#                    
                if kChoice != 0:
                    kChoice = -1
                else:
                    break
                
        if choice != 0:
            choice = -1  
        else:
            break

#***********************************************************************************************************************************
# menu options.

def main():

    choice = -1
    while choice < 0 or choice > 2:
        print('\nBeer Recommender Project')
        print('What operation are we running?')
        print('0. QUIT')
        print('1. Data Collection: web scraping, saving, and loading all beer data')
        print('2. Data Options: graphing and using ML techniques on beer data')

### Need a word counter put together with a means to save the word counter
### Need a key re-assignment for all beer, because we had to scrape data in multiple sessions there are multiple keys being reused.
# need a try except here.
        try:
            choice = int(input())
        except:
            print('\nInvalid choice, please choose wisely.')
        if(choice == 1):
            treeMenuOptions()
        elif(choice == 2):
            dataMenuOptions()

        if choice != 0:
            choice = -1
        else:
            break    

main()
