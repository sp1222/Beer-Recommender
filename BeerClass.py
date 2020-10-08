# Beer Class, will hold information pertaining to individual beers

class Beer:

    def __init__(self):
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

    # setters
    def setBeerName(self, name):
        self.__beerName = name

    def setBeerKey(self, key):
        self.__beerKey = key
        
    def setBeerStyle(self, style):
        self.__beerStyle = style

    def setBeerBrewery(self, brewery):
        self.__beerBrewery = brewery
        
    def setBeerCategoryKey(self, key):
        self.__beerCategoryKey = key
        
    def setBeerABV(self, abv):
        self.__beerABV = abv

    def setBeerAverageRating(self, aveRate):
        self.__beerAverageRating = aveRate

    def setBeerNumberOfRatings(self, numRatings):
        self.__beerNumberOfRatings = numRatings

    def setBeerDescription(self, desc):
        self.__beerDescription = desc

    def setBeerMinIBU(self, minIBU):
        self.__beerMinIBU = minIBU

    def setBeerMaxIBU(self, maxIBU):
        self.__beerMaxIBU = maxIBU

    def addBeerReviewsFullContent(self, content):
        self.__beerReviewsFullContent.append(content)

    def setBeerManualEditFlag(self, flag):
        self.__beerManualEditFlag = flag

    # getters
    def getBeerName(self):
        return self.__beerName

    def getBeerKey(self):
        return self.__beerKey

    def getBeerStyle(self):
        return self.__beerStyle

    def getBeerBrewery(self):
        return self.__beerBrewery

    def getBeerCategoryKey(self):
        return self.__beerCategoryKey

    def getBeerABV(self):
        return self.__beerABV

    def getBeerAverageRating(self):
        return self.__beerAverageRating

    def getBeerNumberOfRatings(self):
        return self.__beerNumberOfRatings

    def getBeerDescription(self):
        return self.__beerDescription

    def getBeerMinIBU(self):
        return self.__beerMinIBU

    def getBeerMaxIBU(self):
        return self.__beerMaxIBU
    
    def getBeerReviewsFullContent(self):
        return self.__beerReviewsFullContent

    def getBeerManualEditFlag(self):
        return self.__beerManualEditFlag
        