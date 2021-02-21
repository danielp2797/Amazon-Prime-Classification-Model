# Amazon-Prime-Classification-Model
In this project, I try to classify Amazon shop products into Prime or not Prime. Mainly I focused on the search "Boxing Fighting Gloves" because I am a boxing fan, but the results should be easy to generalize to other products (this project can be seen as a benchmark). The goal is to help small sellers in order to decide, given a search result, if they should offer the Prime option based on some relevant features.

# 1. Insights about the search "Boxing Fighting Gloves"

## 1.1 Which categories have the companies chosen to sell their product in the key words "boxing fighting gloves"?
<p align="center">
<a href="url"><img src="https://github.com/danielp2797/Amazon-Prime-Classification-Model/blob/main/notebooks/figures/categories.png" align="center" height="400" width="600" ></a>
</p>

## 1.2 Are the products segmented for different targets and which are these segments?
<p align="center">
<a href="url"><img src="https://github.com/danielp2797/Amazon-Prime-Classification-Model/blob/main/notebooks/figures/segments.png" align="center" height="400" width="600" ></a>
</p>

## 1.3 Which are the main brands selling boxing gloves on Amazon, and which "market share" they have?
<p align="center">
<a href="url"><img src="https://github.com/danielp2797/Amazon-Prime-Classification-Model/blob/main/notebooks/figures/main_brands.png" align="center" height="400" width="600" ></a>
</p>

# 2. Amazon Prime option analysis
Now let's focus on the Amazon Prime option and its relation with different product features.

## 2.1 How many brands offer the Amazon Prime option?
<p align="center">
<a href="url"><img src="https://github.com/danielp2797/Amazon-Prime-Classification-Model/blob/main/notebooks/figures/prime-prop.png" align="center" height="400" width="600" ></a>
</p>

We can see that, approximately, the half part of the sellers offer the prime option.
## 2.2 Is the price related to the prime option?
<p align="center">
<a href="url"><img src="https://github.com/danielp2797/Amazon-Prime-Classification-Model/blob/main/notebooks/figures/price-prime.png" align="center" height="400" width="600" ></a>
</p>
We can see that the higher price, the more proportion of prime option products we find. We notice that between 0 and 20 pounds, it is usual not to find prime options, and between 20 and infinite, it is usually the opposite.

## 2.3 Has the position in the category rank an impact on the number of prime products?
<p align="center">
<a href="url"><img src="https://github.com/danielp2797/Amazon-Prime-Classification-Model/blob/main/notebooks/figures/position-prime.png" align="center" height="400" width="600" ></a>
</p>
We can see that the higher the category rank, the less proportion of prime option products we find.

## 2.4 Do the sponsored products sell more in prime option than no sponsored?
<p align="center">
<a href="url"><img src="https://github.com/danielp2797/Amazon-Prime-Classification-Model/blob/main/notebooks/figures/sponsored-prime.png" align="center" height="400" width="600" ></a>
</p>
We can see that sponsored products are more likely to offer the prime option.

## 2.5 Has the product score an impact on the number of prime products?
<p align="center">
<a href="url"><img src="https://github.com/danielp2797/Amazon-Prime-Classification-Model/blob/main/notebooks/figures/rating-prime.png" align="center" height="400" width="600" ></a>
</p>
We can see that the products with low scores usually offer their products with the prime option. Probably it is due to they are trying to be competitive against the products with the best scores but without the prime option.

## 2.6 Exploratory conclusions
We can conclude some important facts such as:

1. There is no evidence of any structural error during the web scraping process.
2. The search "boxing fighting gloves" drives the customer into a shop which is:
- fragmented from the competition point of view.
- focused on three target clients: general public (56%), kids (21%), and professional (21%)
- based on three main Amazon subcategories: Boxing Training Gloves (56%), Boxing Fighting Gloves (23%), and Training Gloves (10%).
3. We found four features that can explain the presence of the prime option and can be used to classify products in prime and not prime option:
- Product price (integer)
- Category rank position (integer)
- Sponsored Product (bool)
- Product score (float, one decimal)

# 3. Feature engineering

We will simplify the mentioned features to be used in the model.

## 3.1 Price interval
During the exploratory analysis, we saw that the price conditioned the number of prime products. We will simplify the feature into boolean. We will assume a price bin between twenty and infinite pounds and another price bin between zero and 19.99 pounds. As we can see, the feature "price_bool" catches the essence of the price-prime relation.
<p align="center">
<a href="url"><img src="https://github.com/danielp2797/Amazon-Prime-Classification-Model/blob/main/notebooks/figures/price_bool.png" align="center" height="400" width="600" ></a>
</p>

## 3.2 Position in category rank standarization
We are going to standarize the position in category due to the high range of values [396 , 943348]. If we use this transformation, the optimization algorithms will perform better in a soft space than in a large and empty one.

## 3.3 Rating into integer
Initially, the rating is between zero and five with one decimal (ex: 4.2, 3.8, etc.). We will transform the feature into an integer such that: Rating ---> 10 x Rating. This transformation allows better interpretability in terms of unitary increments than the float version.

# 4. Model definition

We will use just the products in the three main categories: "Boxing Training Gloves", "Boxing Fight Gloves", "Training Gloves". The other categories usually correspond to products that are not boxing gloves, for example, MMA gloves or boxing bandages.

As a benchmark model, I propose to use the Logistic Regression with the sigmoid kernel (Logit). As a scoring metric, we will use the accuracy as usual. As a threshold for the predicted probabilities, we will use 0.5, but we will discuss this choice later.

The result is summarized in the following table.
```
Logit Regression Results                           
==============================================================================
Dep. Variable:           prime_option   No. Observations:                  254
Model:                          Logit   Df Residuals:                      251
Method:                           MLE   Df Model:                            2
Date:                Sun, 21 Feb 2021   Pseudo R-squ.:                  0.4731
Time:                        01:21:24   Log-Likelihood:                -92.666
converged:                       True   LL-Null:                       -175.86
Covariance Type:            nonrobust   LLR p-value:                 7.380e-37
======================================================================================
                         coef    std err          z      P>|z|      [0.025      0.975]
--------------------------------------------------------------------------------------
price_bool             3.9740      0.412      9.635      0.000       3.166       4.782
position_cat_stand    -1.2465      0.304     -4.097      0.000      -1.843      -0.650
rating_mult           -0.0523      0.007     -7.738      0.000      -0.066      -0.039
======================================================================================
```
We can see that the LLR p-value is low enough to assume that the features explain the target feature better than a constant model. The Pseudo R-squared is not too much high but enough to consider the model as acceptable if we consider that our sample is very small.

In general, the marginal p-values are zero, so no features coefficient is zero.

We could interpret the model as follows:
1. If a product price is in [20, inf], then it is more likely to sell with the prime option.
2. The higher the position in the category rank is, the less likely they to sell with the prime option.
3. The higher the rating is, the less likely to sell with the prime option.

In order to get an insight about the predictive power we can see below the result of a cross validation.

<p align="center">
<a href="url"><img src="https://github.com/danielp2797/Amazon-Prime-Classification-Model/blob/main/notebooks/figures/cv-result.png" align="center" height="300" width="800" ></a>
</p>

We can see that the model does not seem to depend on the sample because the scores look similar in both training and test sets, so there is no strong evidence of overfitting.

```
                  Confussion Matrix 

                  pred          False  True 
                  prime_option              
                  False           117     15
                  True             19    103

                    Classification Report

              precision    recall  f1-score   support
       ===============================================
       False       0.86      0.89      0.87       132
        True       0.87      0.84      0.86       122
       ===============================================
    accuracy                           0.87       254
   macro avg       0.87      0.87      0.87       254
weighted avg       0.87      0.87      0.87       254
```
We can see that 87% of Prime products have been well classified, and 86% of no prime products have been well classified. The errors are not unbalanced because the recalls are similar.

# 5. Conclusion
In overall the Logistic Regression can classify Boxing Gloves products into Prime or not Prime option in the Amazon's shop with an accuracy and recall around 86% which means that 86 out 100 times, it will lead us to the correct decission.

# 6. Model's Threshold discussion

Let's say that the Amazon Prime option has a cost of c > 0 by month, and the opportunity cost by purchase (the customer does not buy the product because it is not in Prime option) is c' > 0. How could we say in order to the costs if the model still being acceptable?

We should consider three cases:

1. c'>c, in this case, the seller would want to sell in Amazon Prime option even the cost of Amazon Prime because the opportunity cost of no selling is greater than the Amazon subscription. In this case, we should define the threshold close to 0 in order to ensure that the False Negatives (products that are wrong classified in no Prime) are as less as possible.
2. c'<c, this case is the opposite of the above one and the threshold should be close to 1.
3. c' approximate equal to c, in this case, does not matter the costs, and the threshold is set up at 0.5 by definition, that usually means balanced classification errors.

# 7. Limitations and future points of improvement

It is well known that Amazon shows the results that best match the customer profile. For this reason, I used a neutral browser during the scraping. In addition, it is a dynamic shop in constant change, then, the results today could not be accurate tomorrow. For this reason, the entire process is implemented to run in less than an hour.

Secondly, one of the model features is the price bin of the product. This feature could change across product types. In the case of boxing gloves is [20, inf]. But, for other products, this interval can be different and should be researched particularly.
