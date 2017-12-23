# Semantic Segmentation Project

In this project, a fully convolutional neural network (FCN), based on a pretrained VGG-16 network,  is used to identify the road pixels on images originated from a car camera. It is crucial therefore for the network to provide spatial information of the road.

The network is developed and trained in Tensoflow. 

## Approach
The project template is divided in units that can be independently tested and are the following:

- __load_vgg__ : loads the vgg-16 model and output individual layer for constructing the decoder of the fcn
- __layers__ : the actual fcn network
- __optimize__ : defines the loss and optimizer operations
- __train_nn__: training of the network

## FCN architecture
The architecture is following the approach of the [paper from Berkelay](https://people.eecs.berkeley.edu/~jonlong/long_shelhamer_fcn.pdf)

Initially, layer-7 of the pretrained vgg is converted to 1x1 convolution and then upsampled by a factor of 2, using 4 kernels.
Layer-4 is undergoing the same 1x1 convultuion and added to the previous derived layer. The combined layer is further upsampled by 2.
Same process is followed for leyer 3, being 1x1 convolved and added to the previous combined layer. The last layer is upscaled by 8 using a kernal of size 16 and the output size is matching the input image size. 

## Training
The hyperparamaters used have been chosen and optimized through extensive training  are the following:
- `AdamOptimizer`
- `epochs = 10`
- `learning rate = 0.0005`
- `batch size = 1` (more would exhaust the resources)

The output log is the following and the trained model reaches a cross-entropy error <15%

## Optional work
The trained model was also applied to a video. The video is the one used for vehicle detection in Term 1. I had to resize to 160x576 as Tensorflow was giving a dimension mismatch by 1px. Anyway, the concept does not change. Although the video is not perfect, it is able to seperate the road from cars when they appear. 


## Deliverables
- `helper.py`
- `main.py`
- `project_tests.py`
- Newest inference images from `runs` folder

## Resources
- Udacity forum
- Deep Learning with TensorFlow