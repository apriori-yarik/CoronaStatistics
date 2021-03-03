import os
import shutil
import random
import torch
import torchvision
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from CoronaStatistics.settings import MEDIA_ROOT


loader = torchvision.transforms.Compose([torchvision.transforms.Resize(size = (300,300)),
                                        torchvision.transforms.ToTensor(),
                                        torchvision.transforms.Normalize([0.485,0.456,0.406], [0.229, 0.224, 0.225])])

model = torch.load('coronastats/nn/model1.pth')

def image_loader(image_name):
	image = Image.open(image_name).convert('RGB')
	image = loader(image).float()
	image = image.unsqueeze(0)
	return image

def evaluate(image):
	model.eval()
	data = image
	output = model(data)
	prediction = torch.argmax(output)
	print(output)
	sm = torch.nn.Softmax()
	probabilities = sm(output)
	print(probabilities) 
	covid_prob = probabilities[0][2].item()
	pneumonia_prob = probabilities[0][1].item()
	normal_prob = probabilities[0][0].item()
	return prediction, normal_prob, pneumonia_prob, covid_prob

def handler(image_name):
	path = str(MEDIA_ROOT) + '/' + image_name
	image = image_loader(path)
	return evaluate(image)