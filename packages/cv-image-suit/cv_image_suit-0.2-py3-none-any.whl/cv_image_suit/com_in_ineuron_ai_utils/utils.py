import base64
import numpy
from os import listdir

def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())


def batch_validate(train_dir,valid_dir,percent):
    train_dir = train_dir
    val_dir = valid_dir

    number_of_samples=[]
    for i in listdir(train_dir):
        j = len(listdir(train_dir+'/'+i))
        number_of_samples.append(j)

    for i in listdir(val_dir):
        j = len(listdir(val_dir+'/'+i))
        number_of_samples.append(j)

    minimum_samples = numpy.min(number_of_samples)
    print("min samples ---------------")
    print(number_of_samples)
    print(minimum_samples)
    res = float(minimum_samples) * float(percent)
    print(res)
    batch = numpy.math.ceil(res/100)
    return batch