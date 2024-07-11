# eg-on-smoothing
This is the official code for the paper [Effects of Exponential Gaussian Distribution on (Double Sampling) Randomized Smoothing](https://arxiv.org/abs/2406.02309). This repo is built on the basis of [DSRS's repo](https://github.com/llylly/DSRS), extending its function to support exponential Gaussian distributions, implementing sampling and certification algorithms for empirical results, and providing scripts to reproduce the core theoretical results of our work. Below are the guidelines for using this repo.

## 1. Preparations
### a. Dependencies and datasets
Anaconda environment setting: Python 3.8.13, torch 1.11.0+cu115, torchvision 0.12.0+cu115. The dependencies can be simply installed by running 
```
pip install -r requirements.txt
```
CIFAR-10 and ImageNet can be configured as usual. This repo **does not** need their training sets. 
### b. Pretrained models
All the pretrained models used in this paper can be found at https://figshare.com/articles/software/Pretrained_Models_for_DSRS/21313548 (From the repo of DSRS). By default, all the pretrained models are saved in ``/models``. In all the scripts, ``[model]`` should be set to the actual name used.

### c. Tips and tricks
Here are some important details on reproducing or using this repo.

- Scripts for ESG and EGG are provided in every step, but they are separate and there is no order between them. 
- To observe the effect of the exponent, we fix the base classifier for each experimental group instead of training models for each distribution.
- Parameters ``sigma`` and ``eta`` should always be consistent when sampling and certifying. To obtain better experimental results, the parameter ``sigma`` of the base classifier should ideally be the same as the first two. All the ``sigma`` are fixed when performing experiments on different $\eta$.

## 2. Sampling procedures
### a. Sampling for DSRS
The sampling procedures for DSRS include sampling by smoothing distributions $\mathcal{P}$ and their supplementary distribution $\mathcal{Q}$ (in this paper, their truncated counterparts). First, run the sampling script for distribution $\mathcal{P}$:

``` 
python sampler.py cifar10/imagenet [model] 0.25/0/50/1.00 1.0/2.0/4.0/8.0 --disttype exponential-standard-gaussian --N 50000 --alpha 0.0005 --skip 10/50 --batch 400

python sampler.py cifar10/imagenet [model] 0.25/0/50/1.00 0.25/0.50/1.0/2.0/4.0/8.0 --disttype exponential-general-gaussian --k 1530/75260 --N 50000 --alpha 0.0005 --skip 10/50 --batch 400
``` 

Then run the script for distribution $\mathcal{Q}$:
```
python sampler.py cifar10/imagenet [model] 0.25/0/50/1.00 1.0/2.0/4.0/8.0 --disttype exponential-standard-gaussian --N 50000 --alpha 0.0005 --skip 10/50 --batch 400

python sampler.py cifar10/imagenet [model] 0.25/0/50/1.00 0.25/0.50/1.0/2.0/4.0/8.0 --disttype exponential-general-gaussian --k 1530/75260 --N 50000 --alpha 0.0005 --skip 10/50 --batch 400 --th x+ --exth 
```
The sampling script for the distribution $\mathcal{Q}$ should be run after finishing the sampling for the smoothing distribution, because the threshold parameter $T$ of distribution  $\mathcal{Q}$ is determined by the sampling results of distribution $\mathcal{P}$. All the sampling results are saved in ``/data`` by default.

### b. Sampling for baselines (Neyman-Pearson certification)
 (If only the DSRS results are needed, this step is not necessary.)
 
The DSRS certification takes 50000 samplings for distribution $\mathcal{P}$ and 50000 samplings for distribution $\mathcal{Q}$. For fair comparisons, we take the Neyman-Pearson certification as the baseline, which takes 100000 samplings for distribution $\mathcal{P}$. Sampling by running
```
python sampler.py cifar10/imagenet [model] 0.25/0/50/1.00 1.0/2.0/4.0/8.0 --disttype exponential-standard-gaussian --N 100000 --alpha 0.001 --skip 10 --batch 400

python sampler.py cifar10/imagenet [model] 0.25/0/50/1.00 0.25/0.50/1.0/2.0/4.0/8.0 --disttype exponential-general-gaussian --k 1530/75260 --N 100000 --alpha 0.001 --skip 10 --batch 400
```

## 3. Certification procedures
### a. Ceritification for DSRS
The certification scripts compute the certified radius from the sampling results of distributions $\mathcal{P}$ and $\mathcal{Q}$, where there are 2 steps. First, compute the certification for $\mathcal{P}$'s 50000 samplings. Then, compute the certification for $\mathcal{Q}$'s 50000 samplings on the basis of $\mathcal{P}$'s certification. That is, $\mathcal{Q}$'s certification should be computed after finishing $\mathcal{P}$'s certification because $\mathcal{P}$'s certification will be the starting point of $\mathcal{Q}$'s grid searching.

Scripts for step 1:
```
python main.py cifar10/imagenet origin [model] exponential-standard-gaussian 0.25/0.50/1.00 1.0/2.0/4.0/8.0 50000 0.0005 --workers 20 

python main.py cifar10/imagenet origin [model] exponential-general-gaussian --k 1530/75260 0.25/0.50/1.00 0.25/0.50/1.0/2.0/4.0/8.0 50000 0.0005 --workers 20
```
Scripts for step 2:
```
python main.py cifar10/imagenet improved [model] exponential-standard-gaussian-th 0.25/0.50/1.00 1.0/2.0/4.0/8.0 50000 0.0005 -b x+ --improve_unit 0.01 --exth --workers 20 

python main.py cifar10/imagenet improved [model] exponential-general-gaussian-th --k 1530/75260 0.25/0.50/1.00 0.25/0.50/1.0/2.0/4.0/8.0 50000 0.0005 -b x+ --improve_unit 0.01 --exth --workers 20
```
### b. certification for baselines  (Neyman-Pearson certification)
 (If only the DSRS results are needed, this step is not necessary.)
 This computation is based on the 100000 sampling results from 2b. Scripts:
 ```
python main.py cifar10/imagenet origin [model] exponential-standard-gaussian 0.25/0.50/1.00 1.0/2.0/4.0/8.0 100000 0.001 --workers 20 

python main.py cifar10/imagenet origin [model] exponential-general-gaussian --k 1530/75260 0.25/0.50/1.00 0.25/0.50/1.0/2.0/4.0/8.0 100000 0.001 --workers 20
```
## 4. Examples for the full DSRS procedure
ESG, CIFAR-10:
```
python sampler.py cifar10 models/new_cohen/cohen-cifar-1530-0.50.pth.tar 0.50 2.0 --disttype exponential-standard-gaussian --N 50000 --alpha 0.0005 --skip 10 --batch 400

python sampler.py cifar10 models/new_cohen/cohen-cifar-1530-0.50.pth.tar 0.50 2.0 --disttype exponential-standard-gaussian --N 50000 --alpha 0.0005 --skip 10 --batch 400 --th x+ --exth

python main.py cifar10 origin cohen-cifar-1530-0.50.pth.tar exponential-standard-gaussian 0.50 2.0 50000 0.0005 --workers 20 

python main.py cifar10 improved cohen-cifar-1530-0.50.pth.tar exponential-standard-gaussian-th 0.50 2.0 50000 0.0005 -b x+ --improve_unit 0.01 --exth --workers 20
```
EGG, CIFAR-10:
```
python sampler.py cifar10 models/new_cohen/cohen-cifar-1530-0.50.pth.tar 0.50 2.0 --disttype exponential-general-gaussian --k 1530 --N 50000 --alpha 0.0005 --skip 10 --batch 400

python sampler.py cifar10 models/new_cohen/cohen-cifar-1530-0.50.pth.tar 0.50 2.0 --disttype exponential-general-gaussian --k 1530 --N 50000 --alpha 0.0005 --skip 10 --batch 400 --th x+ --exth

python main.py cifar10 origin cohen-cifar-1530-0.50.pth.tar exponential-general-gaussian --k 1530 0.50 2.0 50000 0.0005 --workers 20 

python main.py cifar10 improved cohen-cifar-1530-0.50.pth.tar exponential-general-gaussian-th --k 1530 0.50 2.0 50000 0.0005 -b x+ --improve_unit 0.01 --exth --workers 20
```
When performing ImageNet experiments:

- ``k`` should be set to 75260.
- [model] should be set according to k.
- Parameter ``skip`` in sampling scripts should be set to 50.

## 5. Theoretical results
``theor/`` has codes for reproducing the theoretical results of the paper. Run 
```
python theor/prove_bound.py
```
to get Table 7 in the main body. Run
```
python theor/const_fac.py
```
to get Figure 3 in the main body.