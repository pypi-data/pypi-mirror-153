# Copyright 2022 Tobias Höfer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
"""Implements a flat and non-flat tf variant of morphologial rank filters."""
import numpy
import tensorflow as tf


def rankop(img: numpy.ndarray,
           se: numpy.ndarray,
           rank: numpy.ndarray,
           padding: str = "SYMMETRIC",
           flat_se: bool = True) -> numpy.ndarray:
    """Implements a flat and non-flat tf variant of morphologial rank filters.

    Example usage:

    img = np.random.rand(28, 28)


    # Standard use case.
    # 4er se
    kernel = np.array([[0,1,0], [1,1,1], [0,1,0]], dtype=np.uint8)
    # 5 possible ranks from flat se, choose first rank (erosion).
    ranks = np.array([1,0,0,0,0])

    rankop(img, kernel, ranks)


    # 3rd rank.
    # 8er se
    kernel = np.array([[1,1,1], [1,1,1], [1,1,1]], dtype=np.uint8)
    # 9 possible ranks from flat se, choose 3rd rank.
    ranks = np.array([0,0,1,0,0,0,0,0,0])

    rankop(img, kernel, ranks)


    # Mixed ranks.
    # 8er se
    kernel = np.array([[1,1,1], [1,1,1], [1,1,1]], dtype=np.uint8)
    # 9 possible ranks from flat se, choose soft ranks.
    ranks = np.array([0.2,0,0,0,0,0,0,0,0.8])

    rankop(img, kernel, ranks)


    # Interprets zero as values using a non-flat se.
    # non-flat se
    kernel = np.array([[0.3,1.0,0.3], [0.8,1,0.8], [0.19,1,0.19]], dtype=np.float32)
    # 9 possible ranks from flat se, choose last rank (dilation).
    ranks = np.array([0,0,0,0,0,0,0,0,1])

    rankop(img, kernel, ranks, flat_se=False)


    # Interprets zeros in as boolean types using a non-flat se.
    # non-flat se wit
    kernel = np.array([[0.3,0.0,0.3], [0.8,0.0,0.8], [0.19,1.0,0.19]], dtype=np.float32)
    # 7 possible ranks from se (2 excluding zeros), choose middle rank (median).
    ranks = np.array([0,0,0,1,0,0,0])

    rankop(img, kernel, ranks, flat_se=False)




    Args:
        img (np.array): A grayscale/binary image without batch or channel dim,
            e.g. shape (28,28).
        se (np.array): Structuring element or kernel as a 2d numpy array,
            e.g. shape (3,3). Supports non-flat structuring elements with
            floating point values.
        rank (np.array): A 1d rank vector. Length is determined by se and mode.
            Using a non-flat 3x3 se, this operation supports 9 different ranks
            including soft ranks. If mode Flat is active and your se contains
            zeros (False), shrink the rank vector by 1 for every zero set.
        padding (str, optional): Padding to be used, defaults to SYMMETRIC. Also
            supports VALID and SAME.
        flat_se (bool, optional): Choose between FLAT (True) or NON-FLAT (False).
            FLAT interprets zero values as boolean False type and excludes these
            pixel from calculations, which is the most common use case. NON-FLAT
            mode allows the elements of an se to accept zero values.


    Returns:
        numpy.ndarray: A 2d processed image.
    """
    epsilon = 0.001
    img_h = img.shape[0]
    img_w = img.shape[1]
    se_h = se.shape[0]
    se_w = se.shape[1]
    # channel dim of se
    se_in_ch = 1
    se_out_ch = 1
    # Add batch dim & ch dim
    img = tf.expand_dims(tf.expand_dims(img, axis=0), axis=-1)
    batch_dim = 1

    se = tf.cast(se, tf.float32)
    rank = tf.cast(rank, tf.float32)

    if padding == "VALID" or padding == "SAME":
        # TF functionality
        padded_img = img
    else:
        # Custom padding
        h_pad = tf.math.ceil(tf.cast((se_h / 2) - 1, tf.float16))
        w_pad = tf.math.ceil(tf.cast((se_h / 2) - 1, tf.float16))
        paddings = [[0, 0], [h_pad, h_pad], [w_pad, w_pad], [0, 0]]
        padded_img = tf.cast(tf.pad(img, paddings, padding), tf.float32)

    # Returns a 4-D Tensor of the same type as the input. Extracted batches
    # are stacked in the last dimension.
    # [Batch, inputs_width, inputs_height, batches]
    if padding == "SAME":
        image_patches = tf.image.extract_patches(padded_img,
                                                 sizes=[1, se_h, se_w, 1],
                                                 strides=[1, 1, 1, 1],
                                                 rates=[1, 1, 1, 1],
                                                 padding="SAME")
    else:
        image_patches = tf.image.extract_patches(padded_img,
                                                 sizes=[1, se_h, se_w, 1],
                                                 strides=[1, 1, 1, 1],
                                                 rates=[1, 1, 1, 1],
                                                 padding="VALID")

    # Trick: im2col (vectorize convolution)
    shape = tf.convert_to_tensor(
        [batch_dim, 1, img_h * img_w, se_h * se_w * se_in_ch])
    image_patches = tf.reshape(image_patches, shape)

    # Reshape structuring element to vector.
    # (1, 1, se_h*se_w*se_in_ch, se_out_ch)
    se = tf.reshape(se, [1, 1, se_h * se_w * se_in_ch, se_out_ch])
    # (1, se_out_ch, 1, se_h*se_w*se_in_ch)
    se = tf.transpose(se, [0, 3, 1, 2])

    # Copy se for every tensor in a given batch.
    # (batch, se_out_ch, 1, se_h*se_w*se_in_ch)
    se = tf.tile(se, [batch_dim, 1, 1, 1])

    # Element-wise multiplication of patches and se.
    non_sorted_list = tf.multiply(se, image_patches + epsilon)

    if flat_se:
        # Filter non zero values.
        # indices of non zero values.
        zero = tf.constant(0, dtype=tf.float32)
        mask = tf.not_equal(non_sorted_list, zero)
        # Correction
        non_sorted_list = tf.subtract(non_sorted_list, se * epsilon)
        non_sorted_list = tf.ragged.boolean_mask(non_sorted_list,
                                                 mask).to_tensor()
    else:
        # Correction
        non_sorted_list = tf.subtract(non_sorted_list, se * epsilon)

    # Sort.
    sorted_list = tf.sort(non_sorted_list, axis=-1, direction="ASCENDING")

    # Multiply rank probabilities with sorted list. Only element at given
    # rank is active.
    ranks = rank

    if flat_se:
        ranks = tf.reshape(ranks, [1, 1, se_out_ch, len(rank) * se_in_ch])
    else:
        ranks = tf.reshape(ranks, [1, 1, se_out_ch, se_h * se_w * se_in_ch])

    ranks = tf.transpose(ranks, [0, 2, 1, 3])
    ranks = tf.tile(ranks, [batch_dim, 1, 1, 1])
    mul_2 = tf.multiply(sorted_list, ranks)

    # Compute sum over rank * SL(se * patch).
    # (batch, out_ch, img_h*img_w, 1)
    result = tf.reduce_sum(mul_2, 3, keepdims=True)
    result = tf.transpose(result, [0, 3, 2, 1])
    # Reshape results
    result = tf.reshape(result,
                        [batch_dim, img.shape[1], img.shape[2], se_out_ch])
    result = tf.squeeze(result).numpy()
    return result
