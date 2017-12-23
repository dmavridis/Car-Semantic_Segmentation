import os.path
import tensorflow as tf
import helper
import warnings
from distutils.version import LooseVersion
import project_tests as tests
import sys

# Check TensorFlow Version
assert LooseVersion(tf.__version__) >= LooseVersion('1.0'), 'Please use TensorFlow version 1.0 or newer.  You are using {}'.format(tf.__version__)
print('TensorFlow Version: {}'.format(tf.__version__))

# Check for a GPU
if not tf.test.gpu_device_name():
    warnings.warn('No GPU found. Please use a GPU to train your neural network.')
else:
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))


def load_vgg(sess, vgg_path):
    """
    Load Pretrained VGG Model into TensorFlow.
    :param sess: TensorFlow Session
    :param vgg_path: Path to vgg folder, containing "variables/" and "saved_model.pb"
    :return: Tuple of Tensors from VGG model (image_input, keep_prob, layer3_out, layer4_out, layer7_out)
    """
    # TODO: Implement function
    #   Use tf.saved_model.loader.load to load the model and weights
    vgg_tag = 'vgg16'
    vgg_input_tensor_name = 'image_input:0'
    vgg_keep_prob_tensor_name = 'keep_prob:0'
    vgg_layer3_out_tensor_name = 'layer3_out:0'
    vgg_layer4_out_tensor_name = 'layer4_out:0'
    vgg_layer7_out_tensor_name = 'layer7_out:0'

    graph = tf.saved_model.loader.load(sess, [vgg_tag], vgg_path)

    image_input = sess.graph.get_tensor_by_name(vgg_input_tensor_name)
    keep_prob = sess.graph.get_tensor_by_name(vgg_keep_prob_tensor_name)
    layer3 = sess.graph.get_tensor_by_name(vgg_layer3_out_tensor_name)
    layer4 = sess.graph.get_tensor_by_name(vgg_layer4_out_tensor_name)   
    layer7 = sess.graph.get_tensor_by_name(vgg_layer7_out_tensor_name)
      
    return image_input, keep_prob, layer3, layer4, layer7

tests.test_load_vgg(load_vgg, tf)


def layers(vgg_layer3_out, vgg_layer4_out, vgg_layer7_out, num_classes):
    """
    Create the layers for a fully convolutional network.  Build skip-layers using the vgg layers.
    :param vgg_layer7_out: TF Tensor for VGG Layer 3 output
    :param vgg_layer4_out: TF Tensor for VGG Layer 4 output
    :param vgg_layer3_out: TF Tensor for VGG Layer 7 output
    :param num_classes: Number of classes to classify
    :return: The Tensor for the last layer of output
    """
    # TODO: Implement function
    
    # Processing the vgg layer 7 output
    conv_1x1 = tf.layers.conv2d(vgg_layer7_out, num_classes, 1, padding='same', 
                                kernel_regularizer=tf.contrib.layers.l2_regularizer(1e-3),
                                kernel_initializer=tf.contrib.layers.xavier_initializer_conv2d())
    
    fcn_1 = tf.layers.conv2d_transpose(conv_1x1, num_classes, 4, 2, padding='same', 
                                kernel_regularizer=tf.contrib.layers.l2_regularizer(1e-3),
                                kernel_initializer=tf.contrib.layers.xavier_initializer_conv2d())

    # processing the the vgg layer 4 output
    conv_1x1 = tf.layers.conv2d(vgg_layer4_out, num_classes, 1, padding='same', 
                                kernel_regularizer=tf.contrib.layers.l2_regularizer(1e-3),
                                kernel_initializer=tf.contrib.layers.xavier_initializer_conv2d())

    fcn_1 = tf.add(conv_1x1, fcn_1)
    
    fcn_2 = tf.layers.conv2d_transpose(fcn_1, num_classes, 4, 2, padding='same', 
                                kernel_regularizer=tf.contrib.layers.l2_regularizer(1e-3),
                                kernel_initializer=tf.contrib.layers.xavier_initializer_conv2d())
    
    conv_1x1 = tf.layers.conv2d(vgg_layer3_out, num_classes, 1, padding='same', 
                                kernel_regularizer=tf.contrib.layers.l2_regularizer(1e-3),
                                kernel_initializer=tf.contrib.layers.xavier_initializer_conv2d())
    
    fcn_3 = tf.add(fcn_2, conv_1x1)
    
    output = tf.layers.conv2d_transpose(fcn_3, num_classes, 16, 8, padding='same', 
                                kernel_regularizer=tf.contrib.layers.l2_regularizer(1e-3),
                                kernel_initializer=tf.contrib.layers.xavier_initializer_conv2d())
    
    return output

tests.test_layers(layers)


def optimize(nn_last_layer, correct_label, learning_rate, num_classes):
    """
    Build the TensorFLow loss and optimizer operations.
    :param nn_last_layer: TF Tensor of the last layer in the neural network
    :param correct_label: TF Placeholder for the correct label image
    :param learning_rate: TF Placeholder for the learning rate
    :param num_classes: Number of classes to classify
    :return: Tuple of (logits, train_op, cross_entropy_loss)
    """
    # TODO: Implement function
    logits = tf.reshape(nn_last_layer, (-1, num_classes))
    cross_entropy_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=correct_label))*100
    train_op = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy_loss)
    
    print('Built loss and optimizer operations') 
    
    return logits, train_op, cross_entropy_loss    
 
tests.test_optimize(optimize)


def train_nn(sess, epochs, batch_size, get_batches_fn, train_op, cross_entropy_loss, input_image,
             correct_label, keep_prob, learning_rate):
    """
    Train neural network and print out the loss during training.
    :param sess: TF Session
    :param epochs: Number of epochs
    :param batch_size: Batch size
    :param get_batches_fn: Function to get batches of training data.  Call using get_batches_fn(batch_size)
    :param train_op: TF Operation to train the neural network
    :param cross_entropy_loss: TF Tensor for the amount of loss
    :param input_image: TF Placeholder for input images
    :param correct_label: TF Placeholder for label images
    :param keep_prob: TF Placeholder for dropout keep probability
    :param learning_rate: TF Placeholder for learning rate
    """
    # TODO: Implement function
    
    
    
    sess.run(tf.global_variables_initializer())    
    print("Initialized variables")
    print("Starting training ...")
    
    # dummy run to get the amount of training images
    batch_runs = 0
    for _,_ in get_batches_fn(batch_size):
        batch_runs += 1

    # training
    for epoch in range(epochs):
        print("Running epoch ", epoch)
        # Loop over all batches
        idx = 0
        for image, label in get_batches_fn(batch_size):
            idx += 1
            pct = (idx+1)*10/batch_runs
            
            _, cost = sess.run([train_op, cross_entropy_loss], 
                            feed_dict={input_image: image, correct_label: label,
                                             keep_prob:  0.5, learning_rate: 0.0001})

            
            print('Epoch ', epoch, ' [', int(pct)*"#", (10-int(pct))*'.', '] ', 'Entropy Loss [%] {:.2f}'.format(cost), end="\r")

        print("Final epoch entropy Loss {:.2f}".format(cost), 20*' ')
#        train_losses.append(cost)
tests.test_train_nn(train_nn)


def run():
    num_classes = 2
    image_shape = (160, 576)
    data_dir = './data'
    runs_dir = './runs'
    tests.test_for_kitti_dataset(data_dir)

    epochs = 10
    batch_size = 1

    # Download pretrained vgg model
    helper.maybe_download_pretrained_vgg(data_dir)

    # OPTIONAL: Train and Inference on the cityscapes dataset instead of the Kitti dataset.
    # You'll need a GPU with at least 10 teraFLOPS to train on.
    #  https://www.cityscapes-dataset.com/

    with tf.Session() as sess:
        # Path to vgg model
        vgg_path = os.path.join(data_dir, 'vgg')
        # Create function to get batches
        get_batches_fn = helper.gen_batch_function(os.path.join(data_dir, 'data_road/training'), image_shape)

        correct_label = tf.placeholder(tf.float32)
        learning_rate = tf.placeholder(tf.float32)
        keep_prob = tf.placeholder(tf.float32)

        # OPTIONAL: Augment Images for better results
        #  https://datascience.stackexchange.com/questions/5224/how-to-prepare-augment-images-for-neural-network

        # TODO: Build NN using load_vgg, layers, and optimize function
        image_input, keep_prob, vgg_layer3_out, vgg_layer4_out, vgg_layer7_out = load_vgg(sess,vgg_path)
        nn_last_layer = layers(vgg_layer3_out, vgg_layer4_out, vgg_layer7_out, num_classes)  
        logits, optimizer, cost = optimize(nn_last_layer, correct_label, learning_rate, num_classes)
        
        # TODO: Train NN using the train_nn function
        train_nn(sess, epochs, batch_size, get_batches_fn, optimizer, cost, image_input, correct_label, keep_prob, learning_rate) 
        # TODO: Save inference data using helper.save_inference_samples
        helper.save_inference_samples(runs_dir, data_dir, sess, image_shape, logits, keep_prob, image_input)

        # OPTIONAL: Apply the trained model to a video
        # video_path = './runs/resized.mp4'
        # video_shape = (160, 576)
        # helper.save_video(video_path, sess, video_shape, logits, keep_prob, image_input)

if __name__ == '__main__':
    run()
