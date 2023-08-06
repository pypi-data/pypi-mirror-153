from tensorflow.keras.applications import Xception,VGG16,VGG19,ResNet50,ResNet101,ResNet152,ResNet50V2,ResNet101V2
from tensorflow.keras.applications import ResNet152V2,InceptionV3,MobileNet,MobileNetV2,DenseNet121,DenseNet169
from tensorflow.keras.applications import DenseNet201,NASNetMobile,EfficientNetB0,EfficientNetB1,EfficientNetB2
from tensorflow.keras.applications.inception_resnet_v2 import InceptionResNetV2
from tensorflow.keras.applications.efficientnet import EfficientNetB3, EfficientNetB4, EfficientNetB5, \
    EfficientNetB6, EfficientNetB7
from tensorflow.keras.applications.nasnet import NASNetLarge
from cv_image_suit.Logging_Layer.logger import App_Logger
from cv_image_suit.Exception_Layer.exception import GenericException
import sys

class modellconfig:
    def __init__(self,model_name):
        self.x = model_name['MODEL_OBJ']
        self.logger = App_Logger()

    def return_model(self,param,img_iteration=1,batch_iteration=1,opt_iteration=1):
        try:
            self.params = param
            data_config = self.params
            sizes = data_config['IMAGE_SIZE'].split(',')
            size = [int(j) for j in sizes]
            temp = len(size)-1
            ch = size[temp]
            core_model = []
            if isinstance(self.x, list):
                print("list")
            else:
                self.x = [self.x]
            for i in range(img_iteration):
                for j in range(batch_iteration):
                    for k in range(opt_iteration):
                        for model_name in self.x:
                            print(model_name)
                            if model_name == 'Xception':
                                print("Loading Xception..")
                                core_model.append(Xception(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'VGG16':
                                print("Loading VGG16..")
                                core_model.append(VGG16(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'VGG19':
                                print("Loading VGG19..")
                                core_model.append(VGG19(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'ResNet50':
                                print("Loading ResNet50..")
                                core_model.append(ResNet50(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'ResNet101':
                                print("Loading ResNet101..")
                                core_model.append(ResNet101(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'ResNet152':
                                print("Loading ResNet152..")
                                core_model.append(ResNet152(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'ResNet50V2':
                                print("Loading ResNet50V2..")
                                core_model.append(ResNet50V2(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'ResNet101V2':
                                print("Loading ResNet101V2..")
                                core_model.append(ResNet101V2(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'ResNet152V2':
                                print("Loading ResNet152V2..")
                                core_model.append(ResNet152V2(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'InceptionV3':
                                print("Loading InceptionV3..")
                                core_model.append(InceptionV3(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'InceptionResNetV2':
                                print("Loading InceptionResNetV2..")
                                core_model.append(InceptionResNetV2(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))


                            elif model_name == 'MobileNet':
                                print("Loading MobileNet..")
                                core_model.append(MobileNet(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'MobileNetV2':
                                print("Loading MobileNetV2..")
                                core_model.append(MobileNetV2(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'DenseNet121':
                                print("Loading DenseNet121..")
                                core_model.append(DenseNet121(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'DenseNet169':
                                print("Loading DenseNet169..")
                                core_model.append(DenseNet169(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'DenseNet201':
                                print("Loading DenseNet201..")
                                core_model.append(DenseNet201(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'NASNetMobile':
                                print("Loading NASNetMobile..")
                                core_model.append(NASNetMobile(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'NASNetLarge':
                                print("Loading NASNetLarge..")
                                core_model.append(NASNetLarge(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'EfficientNetB0':
                                print("Loading EfficientNetB0..")
                                core_model.append(EfficientNetB0(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'EfficientNetB1':
                                print("Loading EfficientNetB1..")
                                core_model.append(EfficientNetB1(include_top=False,weights="imagenet",input_shape=(size[i],size[i],ch)))

                            elif model_name == 'EfficientNetB2':
                                print("Loading EfficientNetB2..")
                                core_model.append(EfficientNetB2(include_top=False, weights="imagenet", input_shape=(size[i],size[i],ch)))

                            elif model_name == 'EfficientNetB3':
                                print("Loading EfficientNetB3..")
                                core_model.append(EfficientNetB3(include_top=False, weights="imagenet", input_shape=(size[i],size[i],ch)))

                            elif model_name == 'EfficientNetB4':
                                print("Loading EfficientNetB4..")
                                core_model.append(EfficientNetB4(include_top=False, weights="imagenet", input_shape=(size[i],size[i],ch)))

                            elif model_name == 'EfficientNetB5':
                                print("Loading EfficientNetB5..")
                                core_model.append(EfficientNetB5(include_top=False, weights="imagenet", input_shape=(size[i],size[i],ch)))

                            elif model_name == 'EfficientNetB6':
                                print("Loading EfficientNetB6..")
                                core_model.append(EfficientNetB6(include_top=False, weights="imagenet", input_shape=(size[i],size[i],ch)))

                            elif model_name == 'EfficientNetB7':
                                print("Loading EfficientNetB7..")
                                core_model.append(EfficientNetB7(include_top=False, weights="imagenet", input_shape=(size[i],size[i],ch)))

            return core_model
        except Exception as e:
            exception = GenericException(
                "Failed during training in module [{0}] class [{1}] method[{2}]"
                .format(self.__module__, modellconfig.__name__,
                         self.return_model.__name__))
            file = open("Logs/logs.txt", 'a+')
            exception_msg = exception.error_message_detail(str(e), sys)
            self.logger.log(file, "Exception occured %s " % exception_msg)
            file.close()
            raise Exception(exception_msg)

