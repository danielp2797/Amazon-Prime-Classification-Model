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





