''' BeerClass.py

Class designed to represent a Beer object.

Attributes
------------
__beerName : str
    name of the beer
    
__beerKey : int
    designated unique key of the beer
    
__beerStyle : str
    style of the beer
    
__beerBrewery : str
    brewery the beer was made at
    
__beerCategoryKey : int
    designated unique key of the beer's style
    
__beerABV : double
    alcohol by volumn of the beer
    
__beerAverageRating : double
    average rating value
    
__beerDescription : str
    description of the beer
    
__beerMinIBU : int
    minimum International Bitterness Unit given by style
    
__beerMaxIBU : int
    maximum International Bitterness Unit given by style
    
__beerReviewsFullContent : list
    list of available beer reviews
    
__beerManualEditFlag : bool
    flag to notify the user an error in data collection has occured
    
__beerWordCount : dict
    dictionary of acceptable words found in reveiw and their respective word counts.
    
__beerFeaturesMatrix : list
    features matrix that defines the beer's flavor profiles.

'''

# Beer Class, will hold information pertaining to individual beers
class Beer:
    ''' Beer Class '''
    def __init__(self):
        ''' Initialize object's attributes '''
        self.__beerName = ''
        self.__beerKey = -1      # a unique key to reference this beer
        self.__beerStyle = ''
        self.__beerBrewery = ''
        self.__beerCategoryKey = 0
        self.__beerABV = ''
        self.__beerAverageRating = 0.0
        self.__beerDescription = ''     # this is where we will find flavor profile key words
        self.__beerMinIBU = 0      # will likely have to get this from the category..
        self.__beerMaxIBU = 0
        self.__beerReviewsFullContent = []
        self.__beerManualEditFlag = False
        self.__beerWordCount = None
        self.__beerFeaturesMatrix = [] # indexes 0 through 18 will be different features of the beer

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

    # setters
    def setBeerName(self, name):
        ''' Set the name of the object '''
        self.__beerName = name

    def setBeerKey(self, key):
        ''' Set the key of the object '''
        self.__beerKey = key
        
    def setBeerStyle(self, style):
        ''' Set the style of the object '''
        self.__beerStyle = style

    def setBeerBrewery(self, brewery):
        ''' Set the brewery of the object '''
        self.__beerBrewery = brewery
        
    def setBeerCategoryKey(self, key):
        ''' Set the style key of the object '''
        self.__beerCategoryKey = key
        
    def setBeerABV(self, abv):
        ''' Set the alcohol by volume of the object '''
        self.__beerABV = abv

    def setBeerAverageRating(self, aveRate):
        ''' Set the average rating of the object '''
        self.__beerAverageRating = aveRate

    def setBeerNumberOfRatings(self, numRatings):
        ''' Set the number of ratings of the object '''
        self.__beerNumberOfRatings = numRatings

    def setBeerDescription(self, desc):
        ''' Set the description of the object '''
        self.__beerDescription = desc

    def setBeerMinIBU(self, minIBU):
        ''' Set the minimum Interlational Bitterness Unit of the object '''
        self.__beerMinIBU = minIBU

    def setBeerMaxIBU(self, maxIBU):
        ''' Set the maximum Interlational Bitterness Unit of the object '''
        self.__beerMaxIBU = maxIBU

    def addBeerReviewsFullContent(self, content):
        ''' Set the complete review content of the object '''
        self.__beerReviewsFullContent.append(content)

    def setBeerManualEditFlag(self, flag):
        ''' Set the flag of the object to notify the user an edit needs to be made'''
        self.__beerManualEditFlag = flag

    def setBeerWordCount(self, wordCount):
        ''' Set the word counts of the object '''
        self.__beerWordCount = wordCount

    def setBeerFeaturesMatrix(self, features):
        ''' Set the features matrix of the object as a list '''
        self.__beerFeaturesMatrix = features

    # getters
    def getBeerName(self):
        ''' returns the name of the object '''
        return self.__beerName

    def getBeerKey(self):
        ''' returns the key of the object '''
        return self.__beerKey

    def getBeerStyle(self):
        ''' returns the style of the object '''
        return self.__beerStyle

    def getBeerBrewery(self):
        ''' returns the brewery of the object '''
        return self.__beerBrewery

    def getBeerCategoryKey(self):
        ''' returns the style key of the object '''
        return self.__beerCategoryKey

    def getBeerABV(self):
        ''' returns the alcohol by volume of the object '''
        return self.__beerABV

    def getBeerAverageRating(self):
        ''' returns the average rating of the object '''
        return self.__beerAverageRating

    def getBeerNumberOfRatings(self):
        ''' returns the number of ratings of the object '''
        return self.__beerNumberOfRatings

    def getBeerDescription(self):
        ''' returns the description of the object '''
        return self.__beerDescription

    def getBeerMinIBU(self):
        ''' returns the minimum International Bitterness Unit of the object '''
        return self.__beerMinIBU

    def getBeerMaxIBU(self):
        ''' returns the maximum International Bitterness Unit of the object '''
        return self.__beerMaxIBU
    
    def getBeerReviewsFullContent(self):
        ''' returns the complete review content of the object '''
        return self.__beerReviewsFullContent

    def getBeerManualEditFlag(self):
        ''' returns true if the user needs to make an edit of the object '''
        return self.__beerManualEditFlag

    def getBeerWordCount(self):
        ''' returns the word counts of the object '''
        return self.__beerWordCount

    def getBeerFeaturesMatrix(self):
        ''' returns the features matrix of the object as a list '''
        return self.__beerFeaturesMatrix
