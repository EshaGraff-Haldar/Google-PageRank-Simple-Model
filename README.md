Google PageRank is an algorithm that was used by Google to determine the relative importance of webpages in a network.
It looks at how webpages link together by recording which webpages have URLs or links to other webpages.
A higher number of inbound links to a webpage, can mean that the webpage is more important.


It is one of many different types of centrality algorithms: this specific method uses Markov Chains and similar methods can be used to find the most important nodes in many other different types of networks too. ie user networks on social media platforms


The "google pagerank.py" file is an intuitive Monte Carlo simulation of how PageRank works.
It simulates a web user crawling through the internet and clicking on pages at random. This is repeated 10,000,000 times.
Inevitably we may return to some webpages more than others; this signifies that there are lots of links (or connections) to these webpages.
We look at the relative number of visits to each webpage and then determine which are more important based on how much "time" we spend in each.

However, not all webpages have outbound links; additionally, some webpages are located within an echo chamber and loop may be entirely disconnected from other parts of the network.
To account for this, 15% of the time (or also when there are no outbound links), we choose a webpage at random to jump to, ensuring we do not remain stuck in an echo chamber and will get around to looking at all (or most) webpages.


The "matrix_pagerank.py" is the real method which PageRank uses. This is because random walks through the network are highly inefficient, taking lots of iterations and are not always accurate.
In this file, we compile all possible transitions from one webpage to another webpage into a square matrix. This is the Markov Chain State Transition Matrix. I used a sparse matrix purely because it is more efficient for large matrices.
To account for echo chambers, we use a "dampening factor" or "jump" which is typically around 85%, 15% (as used in Monte Carlo simulation earlier).

We represent this with a formula:

a = 0.85
Google matrix = a*(Transition Matrix) + (1-a)/Size of Matrix * (Matrix of all ones)

For Markov Chains like this, when this matrix is raised to a large power n, each row in the Markov Chain will eventually converge to an identical row vector. This is the stationary distribution, and represents the probability of a random user finding themselves on this webpage at any point in time during their "infinitely long crawl through the network". The higher the probability, the more important the page.
