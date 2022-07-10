1. For query classification:

    a. How many unique categories did you see in your rolled up training data when you set the minimum number of queries per category to 1000? To 10000?

        category count for threshold = 1000: 387
        category count for threshold = 10000: 69

    b. What were the best values you achieved for R@1, R@3, and R@5?

        10000 threshold; running fasttext, train size is 178169
        testing @1, test size is 178169
        N	178169
        P@1	0.615
        R@1	0.615
        testing @3, test size is 178169
        N	178169
        P@3	0.271
        R@3	0.813
        testing @5, test size is 178169
        N	178169
        P@5	0.174
        R@5	0.87

        10000 threshold; running fasttext with -lr 0.4 -epoch 10, train size is 178169
        testing @1, test size is 178169
        N	178169
        P@1	0.616
        R@1	0.616
        testing @3, test size is 178169
        N	178169
        P@3	0.271
        R@3	0.812
        testing @5, test size is 178169
        N	178169
        P@5	0.174
        R@5	0.868

        It's interesting to note that increasing epochs OR learning rate did not improve at all recall (even reducing it for R@5).

2. For integrating query classification with search:
    
    a. Give 2 or 3 examples of queries where you saw a dramatic positive change in the results because of filtering.

        For the query "apple laptop", the top result of the search went from a MacBook sleeve, to a MacBook Pro, which is the actual expected result for this search. The top category from the classifier, pcmcat247400050001, was enough for clearing the 0.75 threshold.

        For the query "game console", the top result went from a ethernet switch to an Xbox console. The needed categories for clearing the threshold were ["abcat0700000", "abcat0707000", "abcat0701001", "abcat0703001"].

    b. Give 2 or 3 examples of queries where filtering hurt the results, either because the classifier was wrong or for some other reason.

        The query "game controller" returns, predominantly, game consoles, and not controllers. The identified categories were ["abcat0700000", "abcat0715001"].

        The query "orange headphones" was unable to return any orange headphones, only of other colors. The identified categories were ["pcmcat144700050004", "abcat0204000", "abcat0700000", "abcat0811002"].