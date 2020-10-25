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


        # this is for an expanded vision
        # 0 Astringency
        # 1 Body
        # 2 Alcohol
        # 3 Bitter
        # 4 Sweet
        # 5 Sour
        # 6 Salty
        # 7 Dark Fruits
        # 8 Citrus Fruits
        # 9 Tropical Fruits
        # 10 Vegetable
        # 11 Hoppy
        # 12 Herbal
        # 13 Floral
        # 14 Smoke and Heat
        # 15 Spices
        # 16 Malty
        # 17 Richness
        # 18 Yeast

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

    def setBeerWordCount(self, wordCount):
        self.__beerWordCount = wordCount

    def setBeerFeaturesMatrix(self, features):
        self.__beerFeaturesMatrix = features

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

    def getBeerWordCount(self):
        return self.__beerWordCount

    def getBeerFeaturesMatrix(self):
        return self.__beerFeaturesMatrix
