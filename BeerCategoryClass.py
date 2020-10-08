# Beer Category Class, this is where 

import BeerClass

class BeerCategory:
    
    def __init__(self):
        # this node's data:
        self.__categoryName = ''
        self.__categoryKey = -1
        self.__categoryParent = None
        self.__categoryParentKey = -1
        self.__categoryDescription = ''
        self.__categoryMinABV = 0.0
        self.__categoryMaxABV = 0.0
        self.__categoryMinIBU = 0.0
        self.__categoryMaxIBU = 0.0
        self.__category_href = ''
        self.__categoryBeers = []   # a list of BeerClass objects, up to 100 per category
        self.__subCategories = []
        self.__subCategoriesExist = False
        self.__CategoryManualEditFlag = False

# this node's data setters and adders:

    def setCategoryName(self, name):
        self.__categoryName = name
        
    def setCategoryKey(self, key):
        self.__categoryKey = key
        
    def setCategoryParent(self, parent):
        self.__categoryParent = parent
        
    def setCategoryParentKey(self, pKey):
        self.__categoryParentKey = pKey

    def setCategoryDescription(self, desc):
        self.__categoryDescription = desc

    def setCategoryMinABV(self, ABV):
        self.__categoryMinABV = ABV

    def setCategoryMaxABV(self, ABV):
        self.__categoryMaxABV

    def setCategoryMinIBU(self, IBU):
        self.__categoryMinIBU = IBU

    def setCategoryMaxIBU(self, IBU):
        self.__categoryMaxIBU

    def setCategory_href(self, href):
        self.__category_href = href
        
    def addCategoryBeer(self, item):
        self.__categoryBeers.append(item)
        
    def addSubCategory(self, subCat):
        self.__subCategories.append(subCat) # appends a child node to the dictionary

    def setSubCategoriesExist(self, exist):
        self.__subCategoriesExist = exist

    def setCategoryManualEditFlag(self, flag):
        self.__CategoryManualEditFlag = flag


# this node's data getters:

    def getCategoryName(self):
        return self.__categoryName

    def getCategoryKey(self):
        return self.__categoryKey
    
    def getCategoryParent(self):
        return self.__categoryParent
    
    def getCategoryParentKey(self):
        return self.__categoryParentKey

    def getCategoryDescription(self):
        return self.__categoryDescription

    def getCategoryMinABV(self):
        return self.__categoryMinABV

    def getCategoryMaxABV(self):
        return self.__categoryMaxABV

    def getCategoryMinIBU(self):
        return self.__categoryMinIBU

    def getCategoryMaxIBU(self):
        return self.__categoryMaxIBU

    def getCategory_href(self):
        return self.__category_href
        
    def getCategoryBeers(self):
        return self.__categoryBeers

    def getCategoryItemsCount(self):
        return len(self.__categoryItems)
        
    def getSubCategories(self):
        return self.__subCategories
    
    def doSubCategoriesExist(self):
        return self.__subCategoriesExist

    def getCategoryManualEditFlag(self):
        return self.__CategoryManualEditFlag
