from kgraph import DataIter
from kgraph import Predict
from kgraph import FB15k237



data = FB15k237()


train_data = data.train

print(train_data.shape)

valid_data = data.valid

print(valid_data.shape)

test_data = data.test

print(test_data.shape)












