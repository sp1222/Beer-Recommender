# Beer-Recommender

This is a project that utilizes K Nearest Neighbors to classify and recommend a beer based on a user input (which is currently static).

The first part of this project is building beer profiles using keywords from each beer's reviews found on BeerAdvocate.com.  
Information for each beer is scraped and stored , including but not limited to name, brewery, an assigned key, reviews and word counts of all words found in the reviews.
The information collected are from each of the 112 styles of beer, the top 50 beers reviewed from each style, and the first (up to) 25 reviews available from each beer.

The word counts are what is used to define the features of a beer.
The features of a beer are defined as follows:
Astringency, Body, Alcohol, Bitter, Sweet, Sour, Salty, Fruity, Hoppy, Spiced, Malty

The definitions of these features come from the word counts collected from the reviews.  
If a word appeared in a review of a beer, it adds 1 to the feature the word defines for that beer.

As a review system, it is assumed that people describe what they do experience as opposed to what they do not experience.
For example, one may leave a review stating a stout they drank 'is viscuous and dark' rather than 'is not dry and not light'.

Once the features are defined, I used the K-Nearest Neighbors algorithm implementing Euclidean Distance to determine how to classify an input, and make b number of recommendations based on the input.

For the classification of a user input, the first step was to optimize the K values.  After training, the K values were in a range from 1 to 12.  
Using the optimized K values the KNN algorithm will classify a user input for each optimized K value.

The recommendation is no different, in that it simply asks the user for b number of recommendations based on an input and returns b nearest neighbors as a recommendation.

Notes to self:
- Refactor code: separate data collection from ML techniques, create classes for each ML technique to be used
- Implement other ML techniques: K-Means Clustering is a first to come to mind.
- Collect all beer data from BeerAdvocate.com, implementation for a user to choose a beer from the collection to use as an input.

