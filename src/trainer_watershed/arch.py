import tensorflow as tf
from tensorflow.python.estimator.model_fn import ModeKeys as Modes
import src.lib.tfops as tfops

def simple(features, mode, hparams, scope='simple_network'):
    """Returns a simple network architecture.

    conv[5,5,32] -> Dense -> Dropout -> deconv[5,5,2]

    Parameters
    ----------
    features : Tensor
        4D Tensor where the first dimension is the batch size, then height, width
        and channels
    mode : tensorflow.python.estimator.model_fn.ModeKeys
        Class that contains the current mode
    scope : str, optional
        The scope to use for this architecture

    Returns
    -------
    Tensor op
        Return the final tensor operation (logits), from the network
    """
    with tf.variable_scope(scope):
        is_training = mode == Modes.TRAIN

        # Input Layer
        net = [features]

        # Convolutional Layer #1
        net.append(tf.layers.conv2d(inputs=net[-1],
                                    filters=32,
                                    kernel_size=[5, 5],
                                    strides=(2, 2),
                                    padding="same",
                                    name="conv_1_1",
                                    activation=tf.nn.relu))

        net.append(tf.layers.batch_normalization(net[-1], training=is_training))

        # Fully connected layer
        net.append(tf.layers.dense(inputs=net[-1], units=16, activation=tf.nn.relu))

        # Dropout
        net.append(tf.layers.dropout(inputs=net[-1], rate=0.4, training=is_training))

        # Deconv
        net.append(tfops.deconv2d_resize(inputs=net[-1],
                                         filters=16,
                                         kernel_size=[5, 5],
                                         padding="same",
                                         activation=tf.nn.relu))

        return net[-1]


def medium(features, mode, hparams, scope='medium_network'):
    """Returns a simple network architecture.

    conv[5,5,32] -> Dense -> Dropout -> deconv[5,5,2]

    Parameters
    ----------
    features : Tensor
        4D Tensor where the first dimension is the batch size, then height, width
        and channels
    mode : tensorflow.python.estimator.model_fn.ModeKeys
        Class that contains the current mode
    scope : str, optional
        The scope to use for this architecture

    Returns
    -------
    Tensor op
        Return the final tensor operation (logits), from the network
    """
    with tf.variable_scope(scope):
        is_training = mode == Modes.TRAIN

        # Input Layer
        net = [features]

        # Convolutional Layer #1
        net.append(tf.layers.conv2d(inputs=net[-1],
                                    filters=32,
                                    kernel_size=[7, 7],
                                    strides=(2, 2),
                                    padding="same",
                                    name="conv_1_1",
                                    activation=tf.nn.relu))
        net.append(tf.layers.batch_normalization(net[-1], training=is_training))

        net.append(tf.layers.conv2d(inputs=net[-1],
                                    filters=32,
                                    kernel_size=[5, 5],
                                    strides=(2, 2),
                                    padding="same",
                                    name="conv_1_2",
                                    activation=tf.nn.relu))
        net.append(tf.layers.batch_normalization(net[-1], training=is_training))

        net.append(tf.layers.conv2d(inputs=net[-1],
                                    filters=32,
                                    kernel_size=[3, 3],
                                    strides=(2, 2),
                                    padding="same",
                                    name="conv_1_3",
                                    activation=tf.nn.relu))

        net.append(tf.layers.batch_normalization(net[-1], training=is_training))

        # Fully connected layer
        net.append(tf.layers.dense(inputs=net[-1], units=14, activation=tf.nn.relu))
        net.append(tf.layers.batch_normalization(net[-1], training=is_training))

        # Deconv
        with tf.variable_scope('Deoder'):
            with tf.variable_scope('Resize_1'):
                net.append(tfops.deconv2d_resize(inputs=net[-1],
                                                 filters=16,
                                                 kernel_size=[3, 3],
                                                 padding="same",
                                                 activation=tf.nn.relu))
                net.append(tf.layers.batch_normalization(net[-1], training=is_training))

            with tf.variable_scope('Resize_2'):
                net.append(tfops.deconv2d_resize(inputs=net[-1],
                                                 filters=16,
                                                 kernel_size=[5, 5],
                                                 padding="same",
                                                 activation=tf.nn.relu))
                net.append(tf.layers.batch_normalization(net[-1], training=is_training))

            with tf.variable_scope('Resize_3'):
                net.append(tfops.deconv2d_resize(inputs=net[-1],
                                                 filters=16,
                                                 kernel_size=[7, 7],
                                                 padding="same"))

        return net[-1]


if __name__ == "__main__":
    input_tensor = tf.placeholder(dtype=tf.float32, shape=(5, 512, 512, 3))
    result = medium(input_tensor, Modes.TRAIN, [])
    print(result)