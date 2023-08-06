[![DOI](https://zenodo.org/badge/328248499.svg)](https://zenodo.org/badge/latestdoi/328248499)

# BO4ML: Bayesian Optimization library Automated machine learning 

Copyright (C) 2021 [ECOLE Project](https://ecole-itn.eu/), [NACO Group](https://naco.liacs.nl/)

### Contact us

Duc Anh Nguyen

Email:d-dot-a-dot-nguyen-at-liacs-dot-leidenuniv-dot-nl

Website: [ecole-itn.eu](https://ecole-itn.eu/)
## Installation
### Requirements

As requirements  mentioned in `requirements.txt`, [hyperopt](https://github.com/hyperopt/hyperopt) as build dependencies:

```shell
pip install hyperopt
```
### Installation

You could either install the stable version on `pypi`:

```shell
pip install BO4ML
```

Or, take the lastest version from github:

```shell
pip install git+https://github.com/ECOLE-ITN/NguyenSSCI2021.git
```
--
```shell
git clone https://github.com/ECOLE-ITN/NguyenSSCI2021.git
cd NguyenSSCI2021 && python setup.py install --user
```

## Example
Define a Seach space
```python
from BanditOpt.BO4ML import ConfigSpace, ConditionalSpace, AlgorithmChoice, CategoricalParam, IntegerParam, FloatParam, Forbidden
seed=1 #Set random_state
search_space = ConfigSpace()
# Define Search Space
#Eandom_seed uses for all operators
random_seed=CategoricalParam(seed,"random_state")

#1st Operator: Resampling technique
smo_type = AlgorithmChoice([['NO'], ['SMOTE', 'BorderlineSMOTE']
            , ['SMOTEENN', 'SMOTETomek'],['NearMiss', 'TomekLinks']], 'resampler')
#2nd Operator: Classifier

alg_namestr = AlgorithmChoice(["SVM", "RF"], "alg_namestr")
# Define Search Space for Support Vector Machine
kernel = CategoricalParam(["linear", "rbf", "poly", "sigmoid"], "kernel")
C = FloatParam([1e-2, 100], "C")
degree = IntegerParam([1, 5], 'degree')
coef0 = FloatParam([0.0, 10.0], 'coef0')
gamma = FloatParam([0, 20], 'gamma')
# Define Search Space for Random Forest
n_estimators = IntegerParam([5, 100], "n_estimators")
criterion = CategoricalParam(["gini", "entropy"], "criterion")
max_depth = IntegerParam([10, 200], "max_depth")
max_features = CategoricalParam(['auto', 'sqrt', 'log2'], "max_features")
# Add Search space to Configuraion Space
search_space.add_multiparameter([smo_type,alg_namestr, kernel, C, degree, coef0, gamma
                                    , n_estimators, criterion, max_depth, max_features])
# Define conditional Space
con = ConditionalSpace("conditional")
con.addMutilConditional([kernel, C, degree, coef0, gamma,random_seed], alg_namestr, "SVM")
con.addMutilConditional([n_estimators, criterion, max_depth, max_features,random_seed], alg_namestr, ["RF"])
con.addMutilConditional([random_seed],smo_type,['SMOTE', 'BorderlineSMOTE','SMOTEENN', 'SMOTETomek'])
# Define infeasible space (if any)
#forb = Forbidden()
#forb.addForbidden(abc,["A","C","D"],alg_namestr,"SVM")
```
Load iris data
```python
from sklearn import datasets
iris = datasets.load_iris()
X = iris.data
y = iris.target
```
Define an objective function which returns a real-value
```python
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
import numpy as np
try:
    import imblearn
except ModuleNotFoundError:
    !pip install imbalanced-learn
from imblearn.over_sampling import SMOTE, BorderlineSMOTE
from imblearn.under_sampling import NearMiss, TomekLinks
from imblearn.combine import SMOTEENN, SMOTETomek
from sklearn.metrics import accuracy_score

def obj_func(params):    
    global X,y, prefix, seed,iteration  
    iteration+=1
    params = {k: params[k] for k in params if params[k]}
    
    rparams = params.pop('resampler')
    resampler=rparams.pop(prefix)
    if (resampler == 'SMOTE'):
        smo = SMOTE(**rparams)
    elif (resampler == 'BorderlineSMOTE'):
        smo = BorderlineSMOTE(**rparams)
    elif (resampler == 'BorderlineSMOTE'):
        smo = BorderlineSMOTE(**rparams)
    elif (resampler == 'SMOTEENN'):
        smo = SMOTEENN(**rparams)
    elif (resampler == 'SMOTETomek'):
        smo = SMOTETomek(**rparams)
    elif (resampler == 'NearMiss'):
        smo = NearMiss(**rparams)
    elif (resampler == 'TomekLinks'):
        smo = TomekLinks(**rparams)
    
    cparams = params['alg_namestr']
    params.pop("alg_namestr", None)  
    classifier=cparams.pop('name')
    if (classifier == 'SVM'):
        clf = SVC(**params, random_state=seed)
    elif (classifier == 'RF'):
        clf = RandomForestClassifier(**params, random_state=seed)    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)
    if (resampler== "NO"):
            X_smo_train, y_smo_train=X_train, y_train
    else:
        X_smo_train, y_smo_train=smo.fit_resample(X_train, y_train)
    y_test_pred = clf.fit(X_smo_train, y_smo_train).predict(X_test)

    score = accuracy_score(y_test,y_test_pred)
    print('..iteration:',iteration,' -- accuracy_score', score)
    return {'loss':-score, 'status': STATUS_OK }

```
Optimizing ...
```python

from BanditOpt.BO4ML import BO4ML
### Optimizing ...
prefix='name'
iteration=0
opt = BO4ML(search_space, obj_func, 
            conditional=con, #conditional 
            isFair=True,
            #forbidden=forb, #No infeasible space defined in this example
            HPOopitmizer='hpo', #use hyperopt
            max_eval=50, verbose=True, #number of evaluations
            n_init_sample=10, #number of init sample 
            hpo_algo="tpe", #tpe, rand, atpe, anneal
            SearchType="full",# set "full" to use our sampling approach. Otherwise, the original library to be used
            random_seed=seed,hpo_prefix=prefix,
            ifAllSolution=True
            )
best_param, min_value, listofTrial, eval_count = opt.run()
print('=== best param:',best_param)
print('=== Best accuracy_score:',-min_value)
#listofTrial: see hyperopt document for ``trails''
```
## Citation
### Paper Reference

Duc Anh Nguyen, Anna V. Kononova, Stefan Menzel, Bernhard Sendhoff and Thomas Bäck. Efficient AutoML via Combinational Sampling. IEEE Symposium Series on Computational Intelligence (IEEE SSCI 2021)

### BibTex Reference
    @INPROCEEDINGS{9660073,
    author={Nguyen, Duc Anh and Kononova, Anna V. and Menzel, Stefan and Sendhoff, Bernhard and Back, Thomas},
    booktitle={2021 IEEE Symposium Series on Computational Intelligence (SSCI)},
    title={Efficient AutoML via Combinational Sampling}, `\
    year={2021},
    pages={01-10},
    doi={10.1109/SSCI50451.2021.9660073}}
  
## Acknowledgment

This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 766186 (ECOLE).
