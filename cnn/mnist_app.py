# coding:utf-8

import tensorflow as tf
import numpy as np
from PIL import Image
import mnist_lenet5_backward as mnist_backward
import mnist_lenet5_forward as mnist_forward
from result import Result
import os

logPath = "log/"

def restore_model(testPicArr):
    with tf.Graph().as_default() as tg:
        x = tf.placeholder(tf.float32, [
            1,
            mnist_forward.IMAGE_SIZE,
            mnist_forward.IMAGE_SIZE,
            mnist_forward.NUM_CHANNELS])
        y = mnist_forward.forward(x, False, None)
        # 输出节点的卷积值
        # preValue =y# tf.argmax(y,1)
        preValue = tf.nn.softmax(y)

        variable_averages = tf.train.ExponentialMovingAverage(mnist_backward.MOVING_AVERAGE_DECAY)
        variables_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver(variables_to_restore)

        with tf.Session() as sess:
            # mnist_backward.MODEL_SAVE_PATH
            ckpt = tf.train.get_checkpoint_state('D:/PythonIDE/pythonProgram/AI-Practice-Tensorflow-Notes-master/lenet5/model/')

            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
                # reshaped_x = np.reshape(mnist.test.images, (
                #     mnist.test.num_examples,
                #     mnist_lenet5_forward.IMAGE_SIZE,
                #     mnist_lenet5_forward.IMAGE_SIZE,
                #     mnist_lenet5_forward.NUM_CHANNELS))
                # accuracy_score = sess.run(accuracy, feed_dict={x: reshaped_x, y_: mnist.test.labels})
                testPicArr =np.resize(testPicArr,(1,28,28,1))
                preValue = sess.run(preValue, feed_dict={x: testPicArr})
                return preValue
            else:
                print("No checkpoint file found")
                return -1

# 二值化函数
def pre_pic(picName):
    img = Image.open(picName)
    reIm = img.resize((28, 28), Image.ANTIALIAS)
    im_arr = np.array(reIm.convert('L'))
    threshold = 50  #阙值
    for i in range(28):
        for j in range(28):
            im_arr[i][j] = 255 - im_arr[i][j]
            if (im_arr[i][j] < threshold):
                im_arr[i][j] = 0
            else:
                im_arr[i][j] = 255
    nm_arr = im_arr.reshape([1, 784])
    nm_arr = nm_arr.astype(np.float32)
    img = np.multiply(nm_arr, 1.0 / 255.0)
    # print(img
    return img

def application(picPath):
    # 判断是否能打开
    # print("picPath",picPath)
    if os.path.exists(picPath):
        # print("picPathyes", )
        testPicArr = pre_pic(picPath)  # 预处理，二值化图片
        preValue = restore_model(testPicArr)  # 神经网络识别
        # print(preValue)  # 输出节点卷积值
        # 取输出节点卷积值的逆序前3位
        dic = {i : preValue[0][i] for i in range(len(preValue[0]))}
        a1 = sorted(dic.items(), key=lambda x: x[1], reverse=True)
        # print("a1")
        # print(a1)
        jresult = Result("true",None,None,None,picPath)
        for i in range(20):
            jresult.matrix[i][0]=a1[i][0]
            jresult.matrix[i][1] = a1[i][1]
        # print("jresult.matrix")
        # print(jresult.tostring())
    else:
        jresult = Result("false", None, None,'reg error',picPath)
    return jresult

def main():
    jr = application("F:/PseudoDesktop/GANtest/4.jpg",0)
    jr = application("F:/PseudoDesktop/GANtest/5.jpg", 1)
#    print(jr.tostring())


if __name__ == '__main__':
    main()
