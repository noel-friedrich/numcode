# importing libs

print("Importing Libraries...")

import numpy as np
import torch, random
import torch.nn as nn
import torch.optim as optim

from loaddata import input_data as human_inputs
from loaddata import num_to_inputs



# loading data

print(f"loading {len(human_inputs)} numbers...")

random.shuffle(human_inputs)
num_test_inputs = 50

test_human_inputs, human_inputs = human_inputs[:num_test_inputs], human_inputs[num_test_inputs:]

X_raw_values = human_inputs
Y_raw_values = [[0, 1] for _ in range(len(human_inputs))]

def random_number(length=8):
    return "".join([random.choice("0123456789") for i in range(length)])  

num_random_values = len(human_inputs) * 5
for i in range(num_random_values):
    X_raw_values.append(num_to_inputs(random_number()))
    Y_raw_values.append([1, 0])

X = torch.tensor(X_raw_values, dtype=torch.float32)
Y = torch.tensor(Y_raw_values, dtype=torch.float32)



# training model

print("training model...")

class NumberClassifier(nn.Module):

    def __init__(self):
        super().__init__()
        self.hidden1 = nn.Linear(80, 64)
        self.act1 = nn.ReLU()
        self.hidden2 = nn.Linear(64, 32)
        self.act2 = nn.ReLU()
        self.hidden3 = nn.Linear(32, 32)
        self.act3 = nn.ReLU()
        self.output = nn.Linear(32, 2)
        self.act_output = nn.Sigmoid()

    def forward(self, x):
        x = self.act1(self.hidden1(x))
        x = self.act2(self.hidden2(x))
        x = self.act3(self.hidden3(x))
        x = self.act_output(self.output(x))
        return x
    
model = NumberClassifier()

loss_fn = nn.BCELoss()  # binary cross entropy
optimizer = optim.Adam(model.parameters(), lr=0.001)

n_epochs = 1000
batch_size = 10
 
for epoch in range(n_epochs):
    for i in range(0, len(X), batch_size):
        xbatch = X[i:i+batch_size]
        y_pred = model(xbatch)
        ybatch = Y[i:i+batch_size]
        loss = loss_fn(y_pred, ybatch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f'Finished epoch {epoch}, latest loss {loss}')

def analyse(inputs):
    if isinstance(inputs, str):
        inputs = num_to_inputs(inputs)
    tensors = torch.tensor(inputs, dtype=torch.float32)
    y_out = model(tensors)
    values = [round(t.item(), 2) for t in list(y_out)]
    return (values[1] / sum(values)) >= 0.0001

# testing

def run_tests(inputs, outcome):
    successful_tests = 0

    for test_input in inputs:
        if analyse(test_input) == outcome:
            successful_tests += 1

    return successful_tests / len(inputs)

human_accuracy = run_tests(test_human_inputs, True)
random_accuracy = run_tests([random_number() for i in range(1000)], False)

print(f"{human_accuracy=}\n{random_accuracy=}")

yes = input("Do you want to export the model? (y/n)")
if yes.lower() == "yes" or yes.lower() == "y":
    dummy_input = torch.zeros(80, dtype=torch.float32)
    model.eval()
    filename = "trained_network1.onnx"
    torch.onnx.export(
        model,
        dummy_input,
        filename,
        export_params=True,
        opset_version=11,
        output_names=["out"],
        input_names=["in"])
    print(f"exported as {filename}")
else:
    print("Did not export.")