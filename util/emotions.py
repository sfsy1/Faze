import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
from torch.autograd import Variable

import transforms as transforms
from skimage import io
from skimage.transform import resize
from models import vgg

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
    
def get_emotion(current_face, gray):
    """
    inputs:
    current_face: (xmin, ymin, w, h)
    gray: grayscale frame
    
    outputs:
    emotion: from -1 to 1, 1 being most positive, -1 being most negative
    """
    cut_size = 44
    transform_test = transforms.Compose([
        transforms.TenCrop(cut_size),
        transforms.Lambda(lambda crops: torch.stack([transforms.ToTensor()(crop) for crop in crops])),
    ])   
    
    # crop face from grayscale frame
    xmin = current_face[0]
    xmax = current_face[0] + current_face[2]
    ymin = current_face[1]
    ymax = current_face[1] + current_face[3]
    face = gray[ymin:ymax,xmin:xmax]
    
    # resize and transform
    face = (resize(face, (48,48), mode='symmetric')*255).astype('uint8')
    img = face[:, :, np.newaxis]
    img = np.concatenate((img, img, img), axis=2)
    img = Image.fromarray(img)
    inputs = transform_test(img)

    class_names = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    
    # set device, load model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    net = vgg.VGG('VGG19')
    checkpoint = torch.load('PrivateTest_model.t7')
    net.load_state_dict(checkpoint['net'])
    net.to(device)
    net.eval()

    ncrops, c, h, w = np.shape(inputs)

    inputs = inputs.view(-1, c, h, w)
    inputs = inputs.to(device)
    with torch.no_grad():
        inputs = Variable(inputs)
    outputs = net(inputs)
    outputs_avg = outputs.view(ncrops, -1).mean(0)  # avg over crops
    weights = np.array([-0.4,-0.1,-0.1,0.8,-0.4,0.2])
    score = F.softmax(outputs_avg, dim=0)
    emotion_score = np.sum(score.cpu().detach().numpy()[:6]**0.5*weights)
    

    return emotion_score