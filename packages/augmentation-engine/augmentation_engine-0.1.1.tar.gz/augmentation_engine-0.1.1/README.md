# Torch Compatible Augmentation Engine For Solar Filaments v0.0.1

### An ML-Ready Filament Augmentation Toolkit with Labeled Magnetic Helicity Sign

##### *ABSTRACT*
A halo Coronal Mass Ejection can have a devastating impact on Earth by causing damage to satellites and electrical transmission line facilities and disrupting radio transmissions. To predict the orientation of the magnetic field (and therefore the occurrence of a geomagnetic storm) associated with an occurring CME, filaments' sign of magnetic helicity can be used. This would allow us to predict a geomagnetic storm.

With the deluge of image data produced by ground-based and space-borne observatories and the unprecedented success of computer vision algorithms in detecting and classifying objects (events) on images, identification of filaments' chirality appears to be a well-fitted problem in this domain. To be more specific, Deep Learning algorithms with a Convolutional Neural Network (CNN) backbone are made to attack this very type of problem. The only challenge is that these supervised algorithms are data-hungry; their large number of model parameters demand millions of labeled instances to learn. Datasets of filaments with manually identified chirality, however, are costly to be built. This scarcity exists primarily because of the tedious task of data annotation, especially that identification of filaments' chirality requires domain expertise. In response, we created a pipeline for the augmentation of filaments based on the existing and labeled instances. This Python toolkit provides a resource of unlimited augmented (new) filaments with labeled magnetic helicity signs. Using an existing dataset of H-alpha based manually-labeled filaments as input seeds, collected from August 2000 to 2016 from the big bear solar observatory (BBSO) full-disk solar images, we augment new filament instances by passing labeled filaments through a pipeline of chirality-preserving transformation functions. This augmentation engine is fully compatible with PyTorch, a popular library for deep learning and generates the data based on users requirement.


* [Pypi License](./LICENSE)
* [Source Code](https://bitbucket.org/gsudmlab/augmentation_engine/src/master/)
* [Documenatation](./docs/_build/html/index.html)
* [Demo Code](./demo.ipynb)

#### Requirements
*  Python >= 3.6
*  For a list of all required packages, see [requirements.txt](./requirements.txt).

#### Linux/Mac/Windows OS: Installation
---


```python
pip install augmentation_engine
```

    Requirement already satisfied: augmentation_engine in d:\gsu_assignments\semester_2\dl\augmentation_engine (0.0.1)
    Requirement already satisfied: sortedcontainers in c:\users\shreejaa talla\pycharmprojects\bbso_fa\venv\lib\site-packages (from augmentation_engine) (2.4.0)
    Requirement already satisfied: opencv_python in c:\users\shreejaa talla\pycharmprojects\bbso_fa\venv\lib\site-packages (from augmentation_engine) (4.5.3.56)
    Requirement already satisfied: torchvision in c:\users\shreejaa talla\pycharmprojects\bbso_fa\venv\lib\site-packages (from augmentation_engine) (0.10.0)
    Requirement already satisfied: pillow in c:\users\shreejaa talla\pycharmprojects\bbso_fa\venv\lib\site-packages (from augmentation_engine) (8.3.2)
    Requirement already satisfied: numpy>=1.17.3 in c:\users\shreejaa talla\pycharmprojects\bbso_fa\venv\lib\site-packages (from opencv_python->augmentation_engine) (1.21.2)
    Requirement already satisfied: torch==1.9.0 in c:\users\shreejaa talla\pycharmprojects\bbso_fa\venv\lib\site-packages (from torchvision->augmentation_engine) (1.9.0)
    Requirement already satisfied: typing-extensions in c:\users\shreejaa talla\pycharmprojects\bbso_fa\venv\lib\site-packages (from torch==1.9.0->torchvision->augmentation_engine) (3.10.0.2)
    Note: you may need to restart the kernel to use updated packages.
    

### Import Required Libraries 


```python
import os
from torchvision import transforms
import matplotlib.pyplot as plt

from filament_augmentation.loader.filament_dataloader import FilamentDataLoader
from filament_augmentation.generator.filament_dataset import FilamentDataset
from filament_augmentation.metadata.filament_metadata import FilamentMetadata
```

**To find out the number of left, right and unidentified chiralities for an interval of time.**
- The code snippet below gives the *chirality distribution*, i.e., the distribution of left, right and unidentified chiralities for an interval of time from "2015-08-01 17:36:15" to "2015-08-09 18:15:17".
- Here the petdata has big bear space observatory(BBSO) full disk solar images from (01-09) aug 2015.
- The format for start and end time should be YYYY-MM-DD HH:MM:SS.
- The ann_file or annotation file is a H-alpha based manually labelled filaments in a json file comes with petdata.


```python
__file__ = 'augmentation_process.ipynb'
bbso_json = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'petdata', 'bbso_json_data','2015_chir_data.json'))
filamentInfo = FilamentMetadata(ann_file = bbso_json, start_time = '2015-08-01 00:00:15',
                                    end_time = '2015-08-30 23:59:59')
filamentInfo.get_chirality_distribution()
```




    (22, 30, 186)



- In order to generate extra filaments for left, right or unidentified chirality by either balancing the data or getting them in required ratios to train them using an ML algorithm. A filament dataset class should be initialized which is quite similar to that of pytorch dataset class.
- The transform list should be list of torchvision [transformations](https://pytorch.org/vision/0.8/transforms.html) 
- Filament ratio is tuple variable that takes (L,R,U).

### Initializing Filament dataset 
To initialize filament dataset class follow parameters are required:
- bbso_path - BBSO full disk H-alpha solar images comes with petdata, path of the folder.
- ann_file - a H-alpha based manually labelled filaments in a json file comes with petdata.
- The format for start and end time should be YYYY-MM-DD HH:MM:SS.


```python
bbso_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'petdata', '2015'))
dataset = FilamentDataset(bbso_path = bbso_path, ann_file = bbso_json, 
                          start_time = "2015-08-01 17:36:15", end_time = "2015-08-09 17:36:15")
```

    loading annotations into memory...
    Done (t=0.07s)
    creating index...
    index created!
    

### Setup transformations for data augmentation

The transformations function can be refered from [torchvision transforms](https://pytorch.org/vision/0.8/transforms.html)
- Here transforms variable should have list of torchvision transforms functions as shown below: 


```python
transforms1 = [
    transforms.ColorJitter(brightness=(0.25,1.25), contrast=(0.25,2.00), saturation=(0.25,2.25)),
    transforms.RandomRotation(15,expand=False,fill=110)
]
```

### Initializing data loader
- dataset = object of filament dataset class.
- batch_size = number of filaments to be generated per batch.
- filament_ratio = tuple of three values, i.e., ratios of left, right and unidentified chirality to be generated in each batch.
- n_batchs = number of batchs.
- transforms = list of torchvision transformations functions
- image_dim = image dimensions if image dimension is -1 then image will not be resize, i.e., output is original image size.


```python
data_loader = FilamentDataLoader(dataset = dataset,batch_size = 3 , filament_ratio = (1, 1, 1),n_batchs = 10, 
                                 transforms = transforms1, image_dim = 224)
```

#### How to generate 3 filament images for every batch with ratio of left as 1, right chirality as 1 and unidentified as 1 for 10 batches with original image dimension and display the images?


```python
data_loader = FilamentDataLoader(dataset = dataset,batch_size = 3 , filament_ratio = (1, 1, 1),
                                 n_batchs = 10, transforms = transforms1, image_dim = -1)
```

#### Batch -1 augmented filament images and their following labels (1=R, 0= U, -1=L)


```python
for original_imgs, transformed_imgs, labels in data_loader:
    for org_img, img, label in zip(original_imgs ,transformed_imgs, labels):
        print("Original image")
        plt.imshow(org_img, cmap='gray')
        plt.show()
        print("Transformed image")
        plt.imshow(img, cmap='gray')
        plt.show()
        print("Label",label)
    break
```

    Original image
    


    
![png](document_images/output_18_1.png)
    


    Transformed image
    


    
![png](document_images/output_18_3.png)
    


    Label 0
    Original image
    


    
![png](document_images/output_18_5.png)
    


    Transformed image
    


    
![png](document_images/output_18_7.png)
    


    Label 1
    Original image
    


    
![png](document_images/output_18_9.png)
    


    Transformed image
    


    
![png](document_images/output_18_11.png)
    


    Label -1
    

#### How to generate 12  filament images for every batch with ratio of left as 2, right chirality as 3  and unidentified as 1 for 5 batches with image dimension of 224x224 ?


```python
data_loader = FilamentDataLoader(dataset = dataset,batch_size = 12 , filament_ratio = (2, 3, 1),
                                 n_batchs = 5, transforms = transforms1, image_dim = 224)
```


```python
for _, imgs, labels in data_loader:
    print("size of images ",imgs.shape)
    print("labels for each batch ",labels)
```

    size of images  torch.Size([12, 224, 224])
    labels for each batch  tensor([[-1],
            [-1],
            [ 1],
            [-1],
            [ 0],
            [ 1],
            [-1],
            [ 1],
            [ 1],
            [ 1],
            [ 0],
            [ 1]])
    size of images  torch.Size([12, 224, 224])
    labels for each batch  tensor([[ 0],
            [ 1],
            [-1],
            [-1],
            [ 1],
            [-1],
            [ 1],
            [ 1],
            [ 0],
            [-1],
            [ 1],
            [ 1]])
    size of images  torch.Size([12, 224, 224])
    labels for each batch  tensor([[ 1],
            [ 1],
            [ 1],
            [ 0],
            [-1],
            [ 1],
            [-1],
            [ 0],
            [-1],
            [ 1],
            [-1],
            [ 1]])
    size of images  torch.Size([12, 224, 224])
    labels for each batch  tensor([[-1],
            [-1],
            [ 1],
            [ 1],
            [ 1],
            [ 0],
            [ 1],
            [-1],
            [-1],
            [ 1],
            [ 1],
            [ 0]])
    size of images  torch.Size([12, 224, 224])
    labels for each batch  tensor([[ 1],
            [ 1],
            [-1],
            [ 1],
            [-1],
            [ 0],
            [ 1],
            [ 0],
            [ 1],
            [-1],
            [-1],
            [ 1]])
    

#### How to generate 10 filament images for every batch only for left and right chirality for 5 batches with image dimension of 224x224 ?
- In order to remove one type of chiraity, filament ratio, i.e., tuple(L, R, U):   
    - if L=0 that means left chirality is eliminated. Similarly, this applies to other types as well.


```python
data_loader = FilamentDataLoader(dataset = dataset,batch_size = 10 , filament_ratio = (1, 1, 0),
                                 n_batchs = 5, transforms = transforms1, image_dim = 224)
```


```python
for _, imgs, labels in data_loader:
    print("size of images ",imgs.shape)
    print("labels for each batch ",labels)
```

    size of images  torch.Size([10, 224, 224])
    labels for each batch  tensor([[-1],
            [-1],
            [ 1],
            [ 1],
            [ 1],
            [-1],
            [ 1],
            [-1],
            [-1],
            [ 1]])
    size of images  torch.Size([10, 224, 224])
    labels for each batch  tensor([[ 1],
            [-1],
            [-1],
            [ 1],
            [-1],
            [-1],
            [ 1],
            [ 1],
            [ 1],
            [-1]])
    size of images  torch.Size([10, 224, 224])
    labels for each batch  tensor([[ 1],
            [ 1],
            [ 1],
            [ 1],
            [-1],
            [ 1],
            [-1],
            [-1],
            [-1],
            [-1]])
    size of images  torch.Size([10, 224, 224])
    labels for each batch  tensor([[ 1],
            [ 1],
            [-1],
            [-1],
            [ 1],
            [-1],
            [-1],
            [ 1],
            [-1],
            [ 1]])
    size of images  torch.Size([10, 224, 224])
    labels for each batch  tensor([[-1],
            [-1],
            [-1],
            [ 1],
            [ 1],
            [ 1],
            [-1],
            [ 1],
            [-1],
            [ 1]])
    
