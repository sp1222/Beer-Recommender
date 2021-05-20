''' BeerCategoryClass.py

Class designed to represent the beer style/category object.

Attributes
------------
__categoryName : str
    name of the style/category

__categoryKey : int
    unique key of the style/category

__categoryParent : BeerCategory
    pointer to parent style/category object

__categoryParentKey : int
    parent style/category's unique key

__categoryDescription : str
    description of the style/category

__categoryMinABV : double
    minimum alcohol by volume provided by beer in style/category

__categoryMaxABV : double
    maximum alcohol by volume provided by beer in style/category

__categoryMinIBU : int
    minimum International Bitterness Unit of beer in style/category    

__categoryMaxIBU : int
    maximum International Bitterness Unit of beer in style/category

__category_href : str
    the href extension to go to the style/category's website

__categoryBeers : list[Beer objects]
    list of beer objects available in style/category

__subCategories : list[BeerCategory]
    pointer to sub styles/categories if any

__subCategoriesExist : bool
    indicates if there are sub styles/categories

__categoryWordCount : dict
    dictionary of acceptable words found in beer object's reveiw and their respective word counts.    

__categoryFeaturesMatrix : list
    features matrix that defines the style/category's flavor profiles defined by beer objects    


'''

# Beer Category Class, this is where 

import BeerClass

class BeerCategory:
    ''' Beer Style/Category Class '''
    
    def __init__(self):
        ''' Initialize object's attributes '''
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
        self.__categoryWordCount = None
        self.__categoryFeaturesMatrix = [] # indexes 0 through 18 will be different features of the beer
        
        # 0 Astringency
        # 1 Body
        # 2 Alcohol
        # 3 Bitter
        # 4 Sweet
        # 5 Sour
        # 6 Salty
        # 7 Fruits
        # 8 Hoppy
        # 9 Spices
        # 10 Malty
        
# this node's data setters and adders:

    def setCategoryName(self, name):
        ''' Set the name of the style/category '''
        self.__categoryName = name
        
    def setCategoryKey(self, key):
        ''' Set the key of the style/category '''
        self.__categoryKey = key
        
    def setCategoryParent(self, parent):
        ''' Set the parent object of the style/category '''
        self.__categoryParent = parent
        
    def setCategoryParentKey(self, pKey):
        ''' Set the parent object's key of the style/category '''
        self.__categoryParentKey = pKey

    def setCategoryDescription(self, desc):
        ''' Set the description of the style/category '''
        self.__categoryDescription = desc

    def setCategoryMinABV(self, ABV):
        ''' Set the minimum alcohol by volume of the style/category '''
        self.__categoryMinABV = ABV

    def setCategoryMaxABV(self, ABV):
        ''' Set the maximum alcohol by volume of the style/category '''
        self.__categoryMaxABV = ABV

    def setCategoryMinIBU(self, IBU):
        ''' Set the minimum International Bitterness Unit of the style/category '''
        self.__categoryMinIBU = IBU

    def setCategoryMaxIBU(self, IBU):
        ''' Set the maximum International Bitterness Unit of the style/category '''
        self.__categoryMaxIBU = IBU

    def setCategory_href(self, href):
        ''' Set the href extension of the style/category '''
        self.__category_href = href
        
    def addCategoryBeer(self, item):
        ''' Add a beer object to the list of beers in the style/category '''
        self.__categoryBeers.append(item)
        
    def addSubCategory(self, subCat):
        ''' Add a sub style/category to the list of the style/category '''
        self.__subCategories.append(subCat) # appends a child node to the dictionary

    def setSubCategoriesExist(self, exist):
        ''' Set to True/False if a sub style/category of the style/category exists '''
        self.__subCategoriesExist = exist

    def setCategoryFeaturesMatrix(self, features):
        ''' Set the style/category's features matrix as defined by the beers contained in style/category '''
        self.__categoryFeaturesMatrix = features

# this node's data getters:

    def getCategoryName(self):
        ''' return the name of the style/category '''
        return self.__categoryName

    def getCategoryKey(self):
        ''' return the key of the style/category '''
        return self.__categoryKey
    
    def getCategoryParent(self):
        ''' return the pointer to parent object of the style/category '''
        return self.__categoryParent
    
    def getCategoryParentKey(self):
        ''' return the parent object's key of the style/category '''
        return self.__categoryParentKey

    def getCategoryDescription(self):
        ''' return the description of the style/category '''
        return self.__categoryDescription

    def getCategoryMinABV(self):
        ''' return the minimum alcohol by volume of the style/category '''
        return self.__categoryMinABV

    def getCategoryMaxABV(self):
        ''' return the maximum alcohol by volume of the style/category '''
        return self.__categoryMaxABV

    def getCategoryMinIBU(self):
        ''' return the minimum International Bitterness Unit of the style/category '''
        return self.__categoryMinIBU

    def getCategoryMaxIBU(self):
        ''' return the maximum International Bitterness Unit of the style/category '''
        return self.__categoryMaxIBU

    def getCategory_href(self):
        ''' return the href extension of the style/category '''
        return self.__category_href
        
    def getCategoryBeers(self):
        ''' return the list of beer objects of the style/category '''
        return self.__categoryBeers
        
    def getSubCategories(self):
        ''' return the list of sub styles/categories of the style/category '''
        return self.__subCategories
    
    def doSubCategoriesExist(self):
        ''' returns True/False if sub styles/categories exist '''
        return self.__subCategoriesExist

    def getCategoryFeaturesMatrix(self):
        ''' return the features matrix of the style/category '''
        return self.__categoryFeaturesMatrix
