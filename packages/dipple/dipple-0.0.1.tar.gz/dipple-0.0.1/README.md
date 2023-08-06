
![Logo](https://github.com/wallik2/dipple/blob/main/logo.jpg?raw=true)

# dipple: deep but simple to build..

[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/wallik2/dipple/blob/main/LICENSE) [![Git](https://img.shields.io/github/forks/wallik2/dipple)](https://github.com/wallik2/dipple) [![Discord](https://img.shields.io/discord/911220061287616594)](https://discord.gg/XS8Znh7HPs)

## what is it?
<b>Dipple</b> is a Python package which mainly provide a simple way to build neural network architecture. This package is very useful for a Data scientist beginner who aim to build Logistic, Shallow, or Deep L-layer Neural network with a few line of codes only

We turn deep into dip to make it look more simple

## Requirement
Python 3.7 +

## Installation
```sh
pip install dipple
```

## Quick Start

#### 1. Import the dataset

```sh
import pandas as pd

# Import Data
url = 'https://raw.githubusercontent.com/wallik2/toy_dataset/main/churn_small3.csv'
df = pd.read_csv(url)

# Split to X,Y
X = df[['tenure'	,'TotalCharges'	,'PaperlessBilling']]
Y = df[['Churn']]
```

```sh
display(X.head(3))
```
|    | tenure | TotalCharges | PaperlessBilling |
| ------ | ------ | ------ | ------ |
| | 1 | 29.85 | 1 |
| | 34 | 1889.50 | 0 |
| | 2 | 108.15 | 1 |


```sh
display(Y.head(3))
```
| | Churn | 
| ------ | ------ |
| | 0 |
| | 0 |
| | 1 |

#### 2. Construct the neural network architecture and fit

With the version 0.0.1, dipple can only build Neural network architecture with the following simple hyperparameter setting for Binary classification

- `Number of Layers (L)` ---- The number of hidden and output layers 
- `A Sequence of the Number of Units (n_unit)` ---- A sequence of number of unit(s) from input layer to output layer
- `Learning rate (lr)` ---- An initial learning rate which indicated how the parameter Weight and Bias are updated
- `forward_activation_function` ---- The activation function for forward propagation model (Only ReLU, LeakyReLU, Tanh were available)
- `backward_activation_function`---- The activation function for backward propagation model (Only ReLU, LeakyReLU, Tanh were available)

dipple implements a sigmoid function as activation function for output layer. In this version, you cannot change it.


![Discord](https://i.ibb.co/HDGJbKJ/ss.png)

Let's say we construct the neural network architecture lke the above figure, or Deep `5`-layers Neural networks with the number of unit `8,6,4,2,1` respectively. Both activation functions for forward and backward are `ReLU`, the initial learning rate is `0.00001`
```sh
# Design the Neural network architecture setting
hyperparam = {"L" : 5,
              "n_unit" : [3,8,6,4,2,1],
              "lr" : 1e-5,
              "forward_activation_function" : 'ReLU',
              "backward_activation_function" : 'ReLU'}
```

Once we got the hyperparameter, we can start building by dipple by the following commands. 
```sh
from dipple.BinaryDeepNeuralNetwork import Binary_Deep_L_Layer
model = Binary_Deep_L_Layer(hyperparam)
model.fit(X,Y,Epochs=100000)
```

When we run the above command, you will start to get the output like the following.  case. It will tell the cost function for every 1000 epochs until epoch 100000 for this case.

```
Output : 
> Epoch 0/100000 : ===Cost=== : 1.3092259528752233
> Epoch 1000/100000 : ===Cost=== : 1.18264973341166
> Epoch 2000/100000 : ===Cost=== : 1.0948250491187088
> Epoch 3000/100000 : ===Cost=== : 1.028352257196818
> Epoch 4000/100000 : ===Cost=== : 0.975404404481697
> Epoch 5000/100000 : ===Cost=== : 0.9317897592718797
> Epoch 6000/100000 : ===Cost=== : 0.8950027214519832
                          .
                          .
                          .
                          .
Epoch 98000/100000 : ===Cost=== : 0.5787674005831676
Epoch 99000/100000 : ===Cost=== : 0.5787628642486251
```


Once the model was fitted, we could now obtain the updated parameter or weight and bias for each layer by running the following command

```sh
model.param
```

#### 3. Predict 
To predict, we have two ways to do it
1. ```predict_proba``` : Although it's binary classification, the actual output that the model return is probability.
```sh
model.predict_proba(X)
```
```
Output:
> array([[0.26752663, 0.26704064, 0.26750622, ..., 0.26744317, 0.26745458, 0.26575378]])
```

2. ```predict``` : Unlike predict_proba where it requires threshold to choose the label for it. If the probability is higher than or equal to the threshold, it will be assign as positive label (default threshold is 0.5)

```sh
model.predict(X)
```
```
Output:
> array([[0, 0, 0, ..., 0, 0, 0]])
```

## Dependencies
our package dipple implements by these packages with the following versions

| Dependency | Version |
| ------ | ------ |
| numpy | 1.21.6 |
| pandas | 1.3.5 |
| matplotlib | 3.2.2 |



## License

- [MIT]




[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [MIT]: <https://github.com/wallik2/dipple/blob/main/LICENSE>

