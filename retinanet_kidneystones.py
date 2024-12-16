# -*- coding: utf-8 -*-
"""Retinanet- KidneyStones

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19MuBEzTIOmmMwzY7a6KILavhQu-rhReB
"""

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES
# TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'kidney-stone-images:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F3636344%2F6319067%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240403%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240403T093215Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3Dd7dabebedab8fb760f7898868ced885d291172ce94ed8bce80b6ae8bd1ceab173686f8124ef6ba0d24cc5040c3c6aaeab367bc46408bb4b9aad0ef248319f9579cc9763fc27528d10f1661a3aa602f51282bb16abf29d217449b265a4a1add0a876abce7478ba66ebca290561c95f2cef36bae3eb22b088050262e365d1599dc471a05b7ab657bc1d77cda9514ed3737fa5cbd76b10fe2c196ae1e8667eb0055f5662d07a062f378c4b41188aa547de72cceb327feb838f041c463c71625b32bf717a4696d70b9253ede0b6ecc540503b97f802b90d310bcf8558e7f40269eb41cc415257cc478331dfc9fc4f51dcd4c271bb6554ebc35fbe74f45fdb7818d42'

KAGGLE_INPUT_PATH='/content/drive/MyDrive/Colab Notebooks/kidney'
# KAGGLE_WORKING_PATH='/kaggle/working'
# KAGGLE_SYMLINK='kaggle'

# !umount /kaggle/input/ 2> /dev/null
# shutil.rmtree('/kaggle/input', ignore_errors=True)
# os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
# os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

# try:
#   os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
# except FileExistsError:
#   pass
# try:
#   os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
# except FileExistsError:
#   pass

# for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
#     directory, download_url_encoded = data_source_mapping.split(':')
#     download_url = unquote(download_url_encoded)
#     filename = urlparse(download_url).path
#     destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
#     try:
#         with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
#             total_length = fileres.headers['content-length']
#             print(f'Downloading {directory}, {total_length} bytes compressed')
#             dl = 0
#             data = fileres.read(CHUNK_SIZE)
#             while len(data) > 0:
#                 dl += len(data)
#                 tfile.write(data)
#                 done = int(50 * dl / int(total_length))
#                 sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
#                 sys.stdout.flush()
#                 data = fileres.read(CHUNK_SIZE)
#             if filename.endswith('.zip'):
#               with ZipFile(tfile) as zfile:
#                 zfile.extractall(destination_path)
#             else:
#               with tarfile.open(tfile.name) as tarfile:
#                 tarfile.extractall(destination_path)
#             print(f'\nDownloaded and uncompressed: {directory}')
#     except HTTPError as e:
#         print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
#         continue
#     except OSError as e:
#         print(f'Failed to load {download_url} to path {destination_path}')
#         continue

# print('Data source import complete.')

from google.colab import drive
drive.mount('/content/drive')

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/content/drive/MyDrive/Colab Notebooks/'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

"""Using the object detection template link: https://www.kaggle.com/code/parthasarathyca/fasterrcnn"""

import random
from PIL import Image, ImageDraw
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import torch
import torchvision
from torchvision import transforms as T
# from torchvision.models.detection. faster_rcnn import FastRCNNPredictor

# converting yolo darknet normalized labels to CoCo format x,y,w,h

def yolo_to_coco(x_cen_norm,y_cen_norm,width_norm,height_norm,image_width,image_height):
    box_width=width_norm*image_width
    box_height=height_norm*image_height
    box_center_x=((2*x_cen_norm*image_width)-box_width)/2
    box_center_y=((2*y_cen_norm*image_height)-box_height)/2
    return int(box_center_x),int(box_center_y),int(box_width),int(box_height)

"""Using only train folder"""

import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import os
import cv2
import matplotlib.pyplot as plt
data=pd.DataFrame(columns=['image_id','class_id','x_min','y_min','x_max','y_max'])
labels_path='/content/drive/MyDrive/Colab Notebooks/kidney/train/labels'
train_path='/content/drive/MyDrive/Colab Notebooks/kidney/train/images'
for k in os.listdir(train_path):
    img=cv2.imread(train_path+"/"+k)
    label=pd.read_csv(labels_path+"/"+k.replace(".jpg",'.txt'), delim_whitespace=True, names=['class_id','x_min','y_min','x_max','y_max'],header=None)
    for i in range(len(label)):
        x,y,w,h=yolo_to_coco(label['x_min'][i],label['y_min'][i],label['x_max'][i],label['y_max'][i],img.shape[1],img.shape[0])
        label['x_min'][i]=x
        label['y_min'][i]=y

        label['x_max'][i]=x+w
        label['y_max'][i]=y+h
        label['class_id'][i]=1
    label['image_id']=k
    data=pd.concat([data,label])

data

data.reset_index(drop=True,inplace=True)

data

unique_imgs=data.image_id.unique()

unique_imgs

import torch
from torchvision import transforms as T

class CustDat(torch.utils.data.Dataset):
  def __init__(self, df, unique_imgs, indices):
    self.df = df
    self.unique_imgs = unique_imgs
    self.indices= indices

  def __len__(self):
    return len(self.indices)

  def __getitem__(self, idx):
    image_name= self.unique_imgs[self.indices[idx]]
    boxes= self.df[self.df.image_id == image_name].values[:, 2:].astype("float")
    img = Image.open("/content/drive/MyDrive/Colab Notebooks/kidney/train/images/" + image_name ).convert('RGB')
    labels = torch.ones((boxes.shape[0]), dtype = torch.int64)
    target ={}
    target["boxes"] = torch.tensor (boxes)
    target["label"] = labels
    return T.ToTensor() (img), target

from sklearn.model_selection import train_test_split
train_inds,val_inds=train_test_split(range(unique_imgs.shape[0]),test_size=0.2)

unique_imgs[val_inds]

def custom_collate(data):
  return data

train_dl=torch.utils.data.DataLoader(CustDat(data,unique_imgs,train_inds),
                                     batch_size=8,
                                     shuffle=True,
                                     collate_fn=custom_collate,
                                     pin_memory=True if torch.cuda.is_available() else False)

val_dl=torch.utils.data.DataLoader(CustDat(data,unique_imgs,val_inds),
                                     batch_size=8,
                                     shuffle=True,
                                     collate_fn=custom_collate,
                                     pin_memory=True if torch.cuda.is_available() else False)

import torchvision
from torchvision.models.detection import retinanet_resnet50_fpn

model = torchvision.models.detection.retinanet_resnet50_fpn(pretrained = True)
num_classes = 2
# get number of input features and anchor boxed for the classifier
in_features = model.head.classification_head.conv[0].out_channels
num_anchors = model.head.classification_head.num_anchors

# replace the pre-trained head with a new one
model.head = torchvision.models.detection.retinanet.RetinaNetHead(in_features, num_anchors, num_classes)

import torch
import torchvision

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
device

optimizer= torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9, weight_decay=0.0005)
num_epochs=1

from PIL import Image
model.to(device)
for epochs in range (num_epochs):
    epoch_loss = 0
    best_metric = float('inf')
    best_epoch = -1

    for data in train_dl:
        imgs = []
        targets = []
        for d in data:
            imgs.append(d[0].to(device))
            targ= {}
            targ["boxes"] = d[1]["boxes"].to(device)
            targ["labels"] = d[1]["label"].to(device)
            targets.append(targ)
        loss_dict = model(imgs, targets)
        loss = sum(v for v in loss_dict.values())
        epoch_loss += loss.cpu().detach().numpy()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if epoch_loss < best_metric:
        # Update the best metric and best epoch
            best_metric = epoch_loss
            best_epoch = epochs
            # Save the model with the current best performance
            torch.save(model.state_dict(), "best_model.pth")
    print(epoch_loss)

model.eval()
data=iter(val_dl).__next__()

from IPython.display import display
from PIL import Image, ImageDraw

from torchvision.ops import box_iou

def compute_ap(gt_boxes, gt_labels, pred_boxes, pred_scores, iou_threshold=0.45, class_label=1, device='cpu'):


    # Sort predictions by score
    sort_idx = torch.argsort(pred_scores, descending=True)
    pred_boxes = pred_boxes[sort_idx]
    pred_scores = pred_scores[sort_idx]

    # Compute IoU between predicted and ground truth boxes
    iou = box_iou(pred_boxes, gt_boxes)

    # Find the best matching ground truth box for each prediction
    match_idx = iou.argmax(dim=1)
    match_iou = iou[range(iou.shape[0]), match_idx]

    # Initialize true positive and false positive arrays
    tp = torch.zeros_like(pred_scores)
    fp = torch.zeros_like(pred_scores)

    # Keep track of which ground truth boxes have already been matched
    matched = torch.zeros(gt_boxes.shape[0], dtype=torch.bool)

    # Loop over predictions
    for i in range(pred_scores.shape[0]):
        # If the prediction matches a ground truth box with IoU above the threshold
        if match_iou[i] >= iou_threshold:
            # If the ground truth box has not already been matched
            if not matched[match_idx[i]]:
                # True positive
                tp[i] = 1
                matched[match_idx[i]] = True
            else:
                # False positive (duplicate detection)
                fp[i] = 1
        else:
            # False positive
            fp[i] = 1

    # Compute precision and recall
    tp_cumsum = tp.cumsum(dim=0)
    fp_cumsum = fp.cumsum(dim=0)
    precision = tp_cumsum / (tp_cumsum + fp_cumsum)
    recall = tp_cumsum / gt_boxes.shape[0]

    # Add start and end points to precision-recall curve
    precision = torch.cat([torch.tensor([1.], device=device), precision, torch.tensor([0.], device=device)])
    recall = torch.cat([torch.tensor([0.], device=device), recall, torch.tensor([1.], device=device)])

    # Compute average precision as the area under the precision-recall curve
    ap = -torch.trapz(precision, recall)

    return ap

def disp_imgs(dl):
    for data in dl:
        length = len(data)
        i=0
        for i in range (len(data)):
            imgs = data[i][0]
            targets = data[i][1]
            boxes = targets['boxes']
            boxes = boxes.type(torch.int)
            labels = targets['label']
            i+=1

            output = model([imgs.to(device)])
    #         print(i," - ",output)
            out_bbox = output[0]["boxes"]
    #         print("out_bbox"," - ",out_bbox)
            out_scores = output[0]["scores"]
            keep = torchvision.ops.nms(out_bbox, out_scores, 0.45)
            im = (imgs.permute(1, 2, 0).cpu().detach().numpy() * 255).astype('uint8')
            vsample = Image.fromarray(im)
            draw = ImageDraw.Draw(vsample)
            for box in out_bbox[keep]:
                draw.rectangle(list(box), fill=None, outline="red")
            display(vsample)

    ap = compute_ap(boxes.to(device), labels.to(device), out_bbox.to(device), out_scores.to(device), class_label=1, device=device)

    print("mAP = ",ap)

disp_imgs(val_dl)

"""# Grad - CAM"""

import os

os.environ["KERAS_BACKEND"] = "tensorflow"

import numpy as np
import tensorflow as tf
import keras

# Display
from IPython.display import Image, display
import matplotlib as mpl
import matplotlib.pyplot as plt

model_builder = keras.applications.xception.Xception
img_size = (299, 299)
preprocess_input = keras.applications.xception.preprocess_input
decode_predictions = keras.applications.xception.decode_predictions

last_conv_layer_name = "block14_sepconv2_act"

# The local path to our target image
img_path = "/content/drive/MyDrive/Colab Notebooks/kidney/train/images/1-3-46-670589-33-1-63700700749865510700001-5062181202000819812_png_jpg.rf.269520bcaab75e008e00f57f3fa98851.jpg"

display(Image(img_path))

def get_img_array(img_path, size):
    # `img` is a PIL image of size 299x299
    img = keras.utils.load_img(img_path, target_size=size)
    # `array` is a float32 Numpy array of shape (299, 299, 3)
    array = keras.utils.img_to_array(img)
    # We add a dimension to transform our array into a "batch"
    # of size (1, 299, 299, 3)
    array = np.expand_dims(array, axis=0)
    return array


def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    # First, we create a model that maps the input image to the activations
    # of the last conv layer as well as the output predictions
    grad_model = keras.models.Model(
        model.inputs, [model.get_layer(last_conv_layer_name).output, model.output]
    )

    # Then, we compute the gradient of the top predicted class for our input image
    # with respect to the activations of the last conv layer
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    # This is the gradient of the output neuron (top predicted or chosen)
    # with regard to the output feature map of the last conv layer
    grads = tape.gradient(class_channel, last_conv_layer_output)

    # This is a vector where each entry is the mean intensity of the gradient
    # over a specific feature map channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # We multiply each channel in the feature map array
    # by "how important this channel is" with regard to the top predicted class
    # then sum all the channels to obtain the heatmap class activation
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # For visualization purpose, we will also normalize the heatmap between 0 & 1
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

# Prepare image
img_array = preprocess_input(get_img_array(img_path, size=img_size))

# Make model
model = model_builder(weights="imagenet")

# Remove last layer's softmax
model.layers[-1].activation = None

# Print what the top predicted class is
preds = model.predict(img_array)
print("Predicted:", decode_predictions(preds, top=1)[0])

# Generate class activation heatmap
heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer_name)

# Display heatmap
plt.matshow(heatmap)
plt.show()

def save_and_display_gradcam(img_path, heatmap, cam_path="cam.jpg", alpha=0.4):
    # Load the original image
    img = keras.utils.load_img(img_path)
    img = keras.utils.img_to_array(img)

    # Rescale heatmap to a range 0-255
    heatmap = np.uint8(255 * heatmap)

    # Use jet colormap to colorize heatmap
    jet = mpl.colormaps["jet"]

    # Use RGB values of the colormap
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    # Create an image with RGB colorized heatmap
    jet_heatmap = keras.utils.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
    jet_heatmap = keras.utils.img_to_array(jet_heatmap)

    # Superimpose the heatmap on original image
    superimposed_img = jet_heatmap * alpha + img
    superimposed_img = keras.utils.array_to_img(superimposed_img)

    # Save the superimposed image
    superimposed_img.save(cam_path)

    # Display Grad CAM
    display(Image(cam_path))


save_and_display_gradcam(img_path, heatmap)

!pip install shap

import shap
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import torch
from torchvision import transforms
from torchvision.models.detection import retinanet_resnet50_fpn

# Load the RetinaNet model
# Load the RetinaNet model
model = retinanet_resnet50_fpn(pretrained=False)
model_url = "https://download.pytorch.org/models/retinanet_resnet50_fpn_coco-eeacb38b.pth"
model.load_state_dict(torch.hub.load_state_dict_from_url(model_url))

# Load an image for explanation
img_path = "/content/drive/MyDrive/Colab Notebooks/kidney/train/images/1-3-46-670589-33-1-63700700750188529100001-5659992199131706929_png_jpg.rf.20fb68d8630e3526b4e7e5c8198277cc.jpg"
img = Image.open(img_path).convert("RGB")
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])
x = transform(img)
x = x.unsqueeze(0)  # Add batch dimension
x_flat = x.view(1, -1)  # Reshape for shap

# Define a function to get model predictions
def predict_fn(x):
    with torch.no_grad():
        preds = model(x)
        return preds

# Create an explainer using Kernel SHAP
explainer = shap.Explainer(predict_fn, x_flat)

# Generate SHAP values for the image
shap_values = explainer.shap_values(x_flat)

# Visualize the SHAP values
shap.image_plot(shap_values, -x, labels=["background", "kidney"])

plt.show()

import matplotlib.pyplot as plt
epoch_loss_list = [213.54210302986456,191.81681774160666,163.59763762292891,120.99282209912434,106.8335493175419,97.37472624247036,85.51734119858487,80.76760588493973,75.26479238944766,70.43824974339843,66.03609898404844,64.15554798970993,63.26974362786797,58.53673945871292,57.48723498169284,56.37970553020324,55.42832836767869,52.49533310036713,50.67499489083402,49.243698616665306,45.39930147859836,43.216552978594244,43.553158618912896,42.5152371328703,41.88570300539316]
epochs = [i+1 for i in range(len(epoch_loss_list))]  # Generate epochs dynamically based on the length of epoch_loss_list
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Loss Curve")
plt.plot(epochs, epoch_loss_list)
plt.show()