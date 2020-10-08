from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import BeerCategoryClass
import BeerClass
import fnmatch
import json
import os
import re
import time

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


def createWorkbook(root, docName):
    wb = Workbook()
    addToNewWorkbook(wb, root, 'None', -1, index = 0)
    openFile = docName + '.xlsx'
    wb.save(openFile)

def addToNewWorkbook(wb, currentCategory, pName, pkey, index):

    categoryName = re.sub('\/', 'and',currentCategory.getCategoryName())
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

    subCatsExist = currentCategory.doSubCategoriesExist()
    catSubCatExists = sheet.cell(row = 11, column = 1)
    catSubCatExists.value = 'Sub Categories Exists:'
    catSubCatExists = sheet.cell(row = 11, column = 2)
    catSubCatExists.value = subCatsExist
    
    catSubCats = sheet.cell(row = 12, column = 1)
    catSubCats.value = 'Sub Categories:'
    catSubCatKeys = sheet.cell(row = 13, column = 1)
    catSubCatKeys.value = 'Sub Category Keys:'
    
    columnCount = 2
    for each in currentCategory.getSubCategories():
        catSubCats = sheet.cell(row = 12, column = columnCount)
        catSubCats.value = each.getCategoryName()
        catSubCatKeys = sheet.cell(row = 13, column = columnCount)
        catSubCatKeys.value = each.getCategoryKey()
        columnCount += 1
       
    label = sheet.cell(row = 15, column = 1)
    label.value = 'Name'       
    label = sheet.cell(row = 15, column = 2)
    label.value = 'key'       
    label = sheet.cell(row = 15, column = 3)
    label.value = 'Style'       
    label = sheet.cell(row = 15, column = 4)
    label.value = 'Style Key'       
    label = sheet.cell(row = 15, column = 5)
    label.value = 'Brewery'       
    label = sheet.cell(row = 15, column = 6)
    label.value = 'ABV'       
    label = sheet.cell(row = 15, column = 7)
    label.value = 'Ave Rating'       
    label = sheet.cell(row = 15, column = 8)
    label.value = 'Min IBU'       
    label = sheet.cell(row = 15, column = 9)
    label.value = 'Max IBU'       
    label = sheet.cell(row = 15, column = 10)
    label.value = 'Description'   
    label = sheet.cell(row = 15, column = 11)
    label.value = 'Reviews Full'       

    # this is where we loop each product item from currentCategory
    # and their respective product information.
    currentRow = 16
    currentColumn = 1
    for eachItem in currentCategory.getCategoryBeers():
        var = sheet.cell(row = currentRow, column = currentColumn)
        var.value = eachItem.getBeerName()
        currentColumn += 1
        
        var = sheet.cell(row = currentRow, column = currentColumn)
        var.value = eachItem.getBeerKey()
        currentColumn += 1
        
        var = sheet.cell(row = currentRow, column = currentColumn)
        var.value = eachItem.getBeerStyle()
        currentColumn += 1
        
        var = sheet.cell(row = currentRow, column = currentColumn)
        var.value = eachItem.getBeerCategoryKey()
        currentColumn += 1
        
        var = sheet.cell(row = currentRow, column = currentColumn)
        var.value = eachItem.getBeerBrewery()
        currentColumn += 1
        
        var = sheet.cell(row = currentRow, column = currentColumn)
        var.value = eachItem.getBeerABV()
        currentColumn += 1
        
        var = sheet.cell(row = currentRow, column = currentColumn)
        var.value = eachItem.getBeerAverageRating()
        currentColumn += 1
        
        var = sheet.cell(row = currentRow, column = currentColumn)
        var.value = eachItem.getBeerMinIBU()
        currentColumn += 1
        
        var = sheet.cell(row = currentRow, column = currentColumn)
        var.value = eachItem.getBeerMaxIBU()
        currentColumn += 1
        
        var = sheet.cell(row = currentRow, column = currentColumn)
        try:
            var.value = eachItem.getBeerDescription()
        except:
            var.value = 'error entering this description'
        currentColumn += 1

        for eachReview in eachItem.getBeerReviewsFullContent():
            var = sheet.cell(row = currentRow, column = currentColumn)
            try:
                var.value = eachReview
            except:
                var.value = 'error entering this review'
            currentColumn += 1

        currentColumn = 1
        currentRow += 1
        
    
# send subcategory to add to the workbook through.
    if subCatsExist == True:
        index += 1
        for subCategory in currentCategory.getSubCategories():
            addToNewWorkbook(wb, subCategory, currentCategory.getCategoryName(), currentCategory.getCategoryKey(), index = index)

# Look for any empty or blank pages and remove them from the workbook (this usually occurs at the end of the workbook)
    for sheet in wb:
        if sheet.cell(row = 1, column = 1).value == '' or sheet.cell(row = 1, column = 1).value == None:
            wb.remove(sheet)
        
#*******************************************************************************************************
# Get information from excel file, given that there is an implemented tree already made and information
# just needs to be filled in

def loadTree(tree):
           
    fileDirectory = 'D:\Python Projects\Beer Recommender Project'
    # first we need to see if the name of the categories we want to collect data from exist as files
    fileList = os.listdir(fileDirectory)
    excelFileList = []
    catName = []
    excludedFiles = []
    for file in fileList:
        full = file.split('.')
        if len(full) == 2:
            # exclude excel file names such as the 'keyword data bank'
            if full[1] == 'xlsx':
#                for excluded in excludedFiles:
                excelFileList.append(file)  # list of file names

    for excel in excelFileList:
        keyFound = False
        wb = load_workbook(excel)
        key = int(wb.active.cell(row = 2, column = 2).value)
        for category in tree.getSubCategories():
            for subCategory in category.getSubCategories():
                if subCategory.getCategoryKey() == key:
                    subCategory = gatherInformation(wb.active, subCategory)
                    subCategory.setCategoryParent(category)
                    keyFound == True
                    break
            if keyFound == True:
                break
                    
    print('loading complete')

    return tree

def gatherInformation(sheet, tempCategory):
    tempCategory.setCategoryName(sheet.cell(row = 1, column = 2).value)
    tempCategory.setCategoryKey(int(sheet.cell(row = 2, column = 2).value))
    # we set category parent to the object being iterated after this function
    tempCategory.setCategoryParentKey(int(sheet.cell(row = 4, column = 2).value))
    tempCategory.setCategory_href(sheet.cell(row = 5, column = 2).value)
    tempCategory.setCategoryDescription(sheet.cell(row = 6, column = 2).value)
    tempCategory.setCategoryMinABV(float(sheet.cell(row = 7, column = 2).value))
    tempCategory.setCategoryMaxABV(float(sheet.cell(row = 8, column = 2).value))
    tempCategory.setCategoryMinIBU(float(sheet.cell(row = 9, column = 2).value))
    tempCategory.setCategoryMaxIBU(float(sheet.cell(row = 10, column = 2).value))
    tempCategory.setSubCategoriesExist(sheet.cell(row = 11, column = 2).value)

    currentColumn = 1
    currentRow = 16
    currentCell = sheet.cell(row = currentRow, column = currentColumn)
    while currentCell.value != '' and currentCell.value != None:
        tempItem = BeerClass.Beer()

        value = currentCell.value
        tempItem.setBeerName(value)
        currentColumn += 1
        currentCell = sheet.cell(row = currentRow, column = currentColumn)
        
        value = currentCell.value
        if value == '' or value == None:
            value = 0
        tempItem.setBeerKey(int(value))
        currentColumn += 1
        currentCell = sheet.cell(row = currentRow, column = currentColumn)
        
        value = currentCell.value
        if value == '' or value == None:
            value = 'NA'
        tempItem.setBeerStyle(value)
        currentColumn += 1
        currentCell = sheet.cell(row = currentRow, column = currentColumn)
        
        value = currentCell.value
        if value == '' or value == None:
            value = 0
        tempItem.setBeerCategoryKey(int(value))
        currentColumn += 1
        currentCell = sheet.cell(row = currentRow, column = currentColumn)
        
        value = currentCell.value
        if value == '' or value == None:
            value = 'NA'
        tempItem.setBeerBrewery(value)
        currentColumn += 1
        currentCell = sheet.cell(row = currentRow, column = currentColumn)
        
        value = currentCell.value
        if value == '' or value == None:
            value = 0.0
        tempItem.setBeerABV(float(value))
        currentColumn += 1
        currentCell = sheet.cell(row = currentRow, column = currentColumn)
        
        value = currentCell.value
        if value == '' or value == None:
            value = 0.0
        tempItem.setBeerAverageRating(float(value))
        currentColumn += 1
        currentCell = sheet.cell(row = currentRow, column = currentColumn)
        
        value = currentCell.value
        if value == '' or value == None:
            value = 0
        tempItem.setBeerMinIBU(int(value))
        currentColumn += 1
        currentCell = sheet.cell(row = currentRow, column = currentColumn)
        
        value = currentCell.value
        if value == '' or value == None:
            value = 0
        tempItem.setBeerMaxIBU(int(value))
        currentColumn += 1
        currentCell = sheet.cell(row = currentRow, column = currentColumn)
        
        value = currentCell.value
        if value == '' or value == None:
            value = 'NA'
        tempItem.setBeerDescription(value)
        currentColumn += 1
        currentCell = sheet.cell(row = currentRow, column = currentColumn)

        # gets each review from the file
        while currentCell.value != '' and currentCell.value != None:
            value = currentCell.value
            tempItem.addBeerReviewsFullContent(value)
            currentColumn += 1
            currentCell = sheet.cell(row = currentRow, column = currentColumn)


        tempCategory.addCategoryBeer(tempItem)
        currentRow += 1
        currentColumn = 1
        currentCell = sheet.cell(row = currentRow, column = currentColumn)

       

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
                maxIBU += c
    return minIBU, maxIBU

def cleanupSingleDecimalStrings(string):

    if string != '' or string != None:
        newString = re.sub('[a-zA-Z()\s$/%:]', '', string)
    return newString


# for cleaning up reviews.. we will do this later
def cleanupReviews(string):
    newString
    return newString


# function to get the look, smell, taste, feel, overall numbers from the review
# do we need to do this?
def cleanupSpecificRatings(string):
    look = 0.0
    smell = 0.0
    taste = 0.0
    feel = 0.0
    overall = 0.0
    flag = False
    for c in string:
        if c == '\n':
            flag = True
#        if flag == False:
            # finish cleaning up the texts from reviews.   
    return look, smell, taste, feel, overall
    

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

        # this is where we get the next button to move to the second page.
#        pageCount += 1
#        nextPage = site + (trTags[-1].find('a')['href'])
#        dr.get(nextPage)
#        time.sleep(3)
#        allHTML = BeautifulSoup(dr.page_source, 'html.parser')
    
    dr.close()
    dr.switch_to.window(dr.window_handles[0])

    # save to a new excel document after each category is scraped
    # because SPECTRUM...
    wb = Workbook()
    addToNewWorkbook(wb, currentCategory, currentCategory.getCategoryName(), currentCategory.getCategoryKey(), index = 0)
    name = re.sub('\/', 'and',currentCategory.getCategoryName())
    openFile = name + '.xlsx'
    wb.save(openFile)


    return key



def printManualEditsList(tree):
    for categories in tree.getSubCategories():
        for subCategory in categories.getSubCategories():
            if subCategory.getCategoryManualEditFlag() == True:
                print(subCategory.getCategoryName())
                for eachBeer in subCategory.getCategoryBeers():
                    if eachBeer.getBeerManualEditFlag() == True:
                        print(eachBeer.getBeerName())
        

#***********************************************************************************************************************************
# menu options.


def treeMenuOptions():
    
    choice = -1
    while choice < 0 or choice > 6:
        print('beerAdvocate.com scraper')
        print('What operation are we running?')
        print('0. QUIT')
        print('1. Build Tree: scrape website for its to build a tree of beer styles')
        # NOTE: only if a categories tree already exists in the program!
        print('2. Print Tree: print the tree of beer styles and unique keys to screen')
        print('3. Save Tree: save the tree to a single excel file') # can remove this option since we save as we scrape data
        # NOTE: requires loading cateogires and items tree from excel
        print('4. Load Empty Tree: load all information into empty tree from excel files')  # need to construct this!
        print('5. Load Partial Tree: this option is specifically for when\n   the internet goes down during a scraping session')
        print('6. Scrape for Items: scrape website for items in each category\n   and add to the tree.  This also saves the data during the process')
### Need a word counter put together with a means to save the word counter
### Need a key re-assignment for all beer, because we had to scrape data in multiple sessions there are multiple keys being reused.



# need a try except here.
        choice = int(input())

        
    return choice

# option 1
# function that builds a category tree
def buildCategoryTree(url, name):
    print('\nBuilding category tree..\n')
    # our tree object where we append the nodes and their respective data values.
    tree = BeerCategoryClass.BeerCategory()
    # gets the html via selenium and beautifulsoup combination
    # since we are starting a '/beer/styles', we will go ahead and append that
    # here to get the html for that page.
    customStartingPoint = '/beer/styles'
    soupSource = seleniumGetsHTML(url + customStartingPoint)
    # get the tree's starting node.
    tree = buildTree(soupSource, url)
    print('\nTree has been built!')
    return tree

# option 2
# function that prints a visual representation of the tree to the screen
def printTree(currentCategory):
    print('\nPrinting category tree to screen..\n')
    print(currentCategory.getCategoryName())
    printCategoryTree(currentCategory, 1)
    print('\nTree has been printed!')

# option 3
# function to save tree to a workbook
def saveToWorkbook(tree, name):

    print('\nSaving to workbook titled ' + name + '..')
    createWorkbook(tree, name)
    print('\nSaving complete!')


# option 4
# function to save tree to a workbook
def loadFromWorkbook():

    print('\nLoading all information into uninstantiated tree from workbooks..')
    tree = loadTree(name)
    return tree

# option 5
# function to save tree to a workbook
def loadFromWorkbook(tree):

    print('\nLoading beer information into instantiated tree from workbooks..')
    tree = loadTree(tree)
    return tree

# option 6
# function to add items to each category in the tree
# usually the leaf nodes of a tree
def scrapeCategoryItems(tree, url):

    print('\nGathering item information from website ' + url + '..')
    tree = startGetCategoryItems(tree, url)
    print('\nGathering of item information Complete!')
    return tree


# option 7
# function used to run a list of manual edits necessary after scraping is complete
def manualEditsList(tree):
    print('\nBeginning Test')
    printManualEditsList(tree)
    print('\nTest Completed')
                        
#*******************************************************************************************************
# main function    
def main():

    # our tree object where we append the nodes and their respective data values.
    BeerCategoryTree = BeerCategoryClass.BeerCategory()

    # THIS ONLY WORKS FOR HEB.COM At the moment
    # page we will be visiting to build our tree
    beerURL = 'https://www.beeradvocate.com'
    # Grocery Name
    beerName = 'Beers'
    operationChoice = -1

    while(operationChoice != 0):
        if(operationChoice == 1):
            BeerCategoryTree = buildCategoryTree(beerURL, beerName)
            beerURL = 'https://www.beeradvocate.com'
            
        elif(operationChoice == 2):
            printTree(BeerCategoryTree)
            
        elif(operationChoice == 3):
            saveToWorkbook(BeerCategoryTree, beerName)
            
        elif(operationChoice == 4):
            BeerCategoryTree = loadFromWorkbook()
            
        elif(operationChoice == 5):
            BeerCategoryTree = loadFromWorkbook(BeerCategoryTree)
            
        elif(operationChoice == 6):
            BeerCategoryTree = scrapeCategoryItems(BeerCategoryTree, beerURL)
            
            
    #    elif(operationChoice == 7):
        
        operationChoice = treeMenuOptions()  

    exit()
        
        
main()
