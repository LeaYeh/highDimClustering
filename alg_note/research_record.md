## Challenge ##

An emerging trend is that new applications tend to generate data 
in very **high dimensions** for which traditional methodologies of cluster analysis 
do not work well. Remedies include dimension reduction(PCA, SOMs) and feature  
transformation, but it is a challenge to develop effective instantiations of 
these remedies in the high-dimensional clustering setting.

## PCA ##

PCA is _not_ a clustering method and also _not_ necessarily a method primrily.
Many research use it to reduce dimensionality but it might not be bset as it 
is a **linear** and **parametric**, **nonlinear** and **nonparametric** method 
should not be ignored.

> **Drawbacks**: </br>
> Only preserves large pairwise distances between the points.
> Meaning points which are *far apart in **high-dimensional space** would also appear 
> far apart in **low-dimensional subspace***.

Consider the following dataset:
![dataset](http://i.stack.imgur.com/RHRlB.png)

---

PC1 axis is maximizing the variance of the projection. So in this case it will 
obviously go diagonally from lower-left to upper-right corner:
![dataset-PCA](http://i.stack.imgur.com/oLlEF.png)

## [t-SNE](http://lvdmaaten.github.io/tsne/)  ##

t-SNE is _not_ a clustering technique. It can be used to embed high-dimensional 
data into low dimensions.

## References ##

#### [useful] ####


#### [record] ####

[1] [Random Projection for High Dimensional Data Clustering](https://www.aaai.org/Papers/ICML/2003/ICML03-027.pdf)

[2] [A Single-Pass Algorithm for Efficiently Recovering Sparse Cluster Centers of High-dimensional Data](http://jmlr.org/proceedings/papers/v32/yib14.pdf)

[3] [Visualizing Data using t-SNE](http://lvdmaaten.github.io/publications/papers/JMLR_2008.pdf)
> **Abstract** </br>
> t-SNE is *not* a clustering technique. It can be used to embed high-dimensional 
> data into low dimensions, e.g., 2D for human-intuitive visualization.

[4] [Accelerating t-SNE using Tree-Based Algorithms](http://lvdmaaten.github.io/publications/papers/JMLR_2014.pdf)
([video](https://www.youtube.com/watch?v=RJVL80Gg3lA&list=UUtXKDgv1AVoG88PLl8nGXmw))

[5] [Clustering of the Self-Organizing Map (SOM)](http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=846731)

[6] [Cluster Forests](http://static.googleusercontent.com/media/research.google.com/zh-TW//pubs/archive/41339.pdf)
> **Abstract** </br> 
> inspiration from Random Forests (classification), CF randomly probes a 
high-dimensional data cloud to obtain “good local clusterings” and then aggregates 
via spectral clustering to obtain cluster assignments for the whole dataset. </br>
> The main approaches to aggregation of clustering instances are the *coassociation method*
> and the *hyper-graph method*.
> </br> `CF is based on co-association, specifically using spectral clustering for aggregation.`
> *Computational Statistics and Data Analysis, vol. 66 (2013), pp. 178-192* </br>


#### [info from webside] ####

[] http://stats.stackexchange.com/questions/176672/what-is-meant-by-pca-preserving-only-large-pairwise-distances

## Footnote ##

- CF = Cluster Forest
- RF = Random Forest
- 

<!-- [problem]
how to decide # of sub tree?
how to aggregates votes?
if sub tree is binary decision, how to decide? threshold at each feature?

[?] letting τ denote the number of consecutive unsuccessful attempts in expanding 
the clustering vector f˜.

-->

<!-- [keyword]
feature selection
random forest
cluster quality measure kappa
-->

<!--
RF is a supervised learning methodology and as such there is a clear goal
to achieve.

treating clustering as an optimization problem under an explicitly defined cost
criterion.

Algorithm 1 is called `feature competition`
It aims to provide a good initialization for the growth of a clustering vector.


-->

