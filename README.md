# Beer-Recommender

This is a project that utilizes K Nearest Neighbors to classify and recommend a beer based on a user input.

The first part of this project is building beer profiles using keywords from each beer's reviews found on BeerAdvocate.com.  
Information for each beer is scraped and stored into .xlsx files, including but not limited to name, brewery, an assigned key, reviews and word counts of all words found in the reviews.
The information collected are from each of the 112 styles of beer, the top 50 beers reviewed from each style, and the first 25 reviews from each beer.
From the word counts are what is used to define the features of a beer.
The features of a beer are defined as follows:
Astringency, Body, Alcohol, Bitter, Sweet, Sour, Salty, Fruity, Hoppy, Spiced, Malty

The definitions of these features come from the total word counts collected from the reviews.  
If a word appeared in a review of a beer, it added 1 to the feature the word defined for that beer.

As a review system, I partially rely on the idea that people describe what they do experience as opposed to what they do not experience.
For example, one may leave a review stating a stout they drank 'is viscuous and dark' rather than 'is not dry and not light'.

Once I have a definition of features, I used the K-Nearest Neighbors algorithm implementing Euclidean Distance to determine how to classify an input, and make b number of recommendations based on the input.

For the classification of a user input, the first step was to optimize my K values.  After training, my K values were in a range from 1 to 12.  
Using the optimized K values the KNN algorithm will classify a user input for each optimized K value.

The recommendation is no different, in that it simply asks the user for b number of recommendations based on an input and returns b nearest neighbors as a recommendation.

The follow are steps I would like to take on the project given time to do so:
- Refactor code: separate data collection from ML techniques, create classes for each ML technique to be used
- Implement other ML techniques: K-Means Clustering is a first to come to mind.
- Collect all beer data from BeerAdvocate.com, implement a way for a user to choose a beer from the collection to use as an input.

