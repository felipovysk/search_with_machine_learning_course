1. For classifying product names to categories:

    a. What precision (P@1) were you able to achieve?

        0.972

    b. What fastText parameters did you use?

        -wordNgrams 2 -lr 1.0 -epoch 25

    c. How did you transform the product names?

        I removed repeated spaces, put everything in lowercase, removed non-alphanumeric characters and applied a default english stemmer.

    d. How did you prune infrequent category labels, and how did that affect your precision?

        By removing any and all categories that did not have more than 499 products; it got a bump of over 50% in precision, going from ~0.62 to ~0.97.

2. For deriving synonyms from content:

    a. What were the results for your best model in the tokens used for evaluation?

        Nintendo got matches with both wii and ds, which were nintendo's primary consoles back at the time; ps2 matched with various consoles from that time, prioritizing Sony ones. For bad results, leather did not return any meaningful synonyms, and neither did holidays (its top synonym was "thankyou" (?)).

    b. What fastText parameters did you use?

        -minCount 20 -epoch 25

    c. How did you transform the product names?

        By doing the same thing as was done for classification. This approach was not the best, since there were a lot of synonyms unrelated to the query word. (see 2.a.)

3. For integrating synonyms with search:

    a. How did you transform the product names (if different than previously)?

        The transformation was the same. However, I also tried without using a stemmer, but the results were much worse.

    b. What threshold score did you use?

        0.8, since there were many, many unrelated words in the 0.7s; this made it so that some good synonyms did not make the cut, such as iphone <-> apple

    c. Were you able to find the additional results by matching synonyms?

        Yes, but not on all example queries. On nespresso, since it wasn't in the top 1k most frequent words, it did not get into the synonym list, and thus, it was forced to remain on 8 results.