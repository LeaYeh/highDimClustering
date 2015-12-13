## t-distributed Stochastic Neighbor Embedding (t-SNE) ##

### Abstract ###
**main idea**  
找到與高維度上分佈差異最小的低維度分布
> t-Distributed stochastic neighbor embedding (t-SNE) minimizes the divergence 
between two distributions

* 高維度上以高斯分布建機率模型; 低維度上則以 t-distributions。
* t-distributions 適合樣本數較少的情況(<30)，而 t-SNE 以 local structure 建機率
模型，故樣本數會變小。
  * ?: 高維也用 local structure 減少計算量，樣本數不也會變小?
  * ?: 為什麼要加入機率模型計算相似度?
> The affinities in the original space are represented by **Gaussian joint 
probabilities** and the affinities in the embedded space are represented by 
**Student’s t-distributions**.

?????
> t-SNE will focus on the local structure of the data and will tend to extract 
clustered local groups of samples as highlighted on the S-curve example.

以 KL 計算兩分布的相似度，並以梯度方向找出 local minimal
> The Kullback-Leibler (KL) divergence of the joint probabilities in the original 
space and the embedded space will be minimized by gradient descent.

-----

**The disadvantages to using t-SNE are roughly:**  
* t-SNE is computationally expensive, and can take several hours on million-sample 
datasets where PCA will finish in seconds or minutes.
* The Barnes-Hut t-SNE method is limited to two or three dimensional embeddings.
* The algorithm is stochastic and multiple restarts with different seeds can yield 
different embeddings. However, it is perfectly legitimate to pick the the embedding 
with the least error.
* Global structure is not explicitly preserved. This is problem is mitigated by 
initializing points with PCA (using init=’pca’).


### Refences ###
* How to choose the right estimator? ([link])



-----
[link]: http://scikit-learn.org/stable/tutorial/machine_learning_map/
