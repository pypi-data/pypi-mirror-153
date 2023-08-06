import json

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
        self.model_name = model_name['MODEL_OBJ']
        self.logger = App_Logger()

    def configureData(self,params):
            SIZE = params['IMAGE_SIZE'].split(',')
            h = int(SIZE[0])
            w = int(SIZE[1])
            c = int(SIZE[2])
            IMAGE_SIZE = h, w, c
            CONFIG = {
                'TRAIN_DATA_DIR' : params['TRAIN_DATA_DIR'],
                'VALID_DATA_DIR' : params['VALID_DATA_DIR'],
                'AUGMENTATION': params['AUGMENTATION'],
                'CLASSES' : params['CLASSES'],
                'IMAGE_SIZE' : IMAGE_SIZE,
                'BATCH_SIZE' : params['BATCH_SIZE'],
            }

            return CONFIG

    def return_model(self):
        try:
            with open("Config_Layer/configs.json", 'r') as f:
                self.params = json.load(f)

            data_config = self.configureData(self.params)

            if self.model_name == 'Xception':
                print("Loading Xception..")
                core_model = Xception(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'VGG16':
                print("Loading VGG16..")
                core_model = VGG16(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'VGG19':
                print("Loading VGG19..")
                core_model = VGG19(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'ResNet50':
                print("Loading ResNet50..")
                core_model = ResNet50(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'ResNet101':
                print("Loading ResNet101..")
                core_model = ResNet101(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'ResNet152':
                print("Loading ResNet152..")
                core_model = ResNet152(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'ResNet50V2':
                print("Loading ResNet50V2..")
                core_model = ResNet50V2(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'ResNet101V2':
                print("Loading ResNet101V2..")
                core_model = ResNet101V2(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'ResNet152V2':
                print("Loading ResNet152V2..")
                core_model = ResNet152V2(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'InceptionV3':
                print("Loading InceptionV3..")
                core_model = InceptionV3(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'InceptionResNetV2':
                print("Loading InceptionResNetV2..")
                core_model = InceptionResNetV2(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])


            elif self.model_name == 'MobileNet':
                print("Loading MobileNet..")
                core_model = MobileNet(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'MobileNetV2':
                print("Loading MobileNetV2..")
                core_model = MobileNetV2(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'DenseNet121':
                print("Loading DenseNet121..")
                core_model = DenseNet121(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'DenseNet169':
                print("Loading DenseNet169..")
                core_model = DenseNet169(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'DenseNet201':
                print("Loading DenseNet201..")
                core_model = DenseNet201(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'NASNetMobile':
                print("Loading NASNetMobile..")
                core_model = NASNetMobile(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'NASNetLarge':
                print("Loading NASNetLarge..")
                core_model = NASNetLarge(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'EfficientNetB0':
                print("Loading EfficientNetB0..")
                core_model = EfficientNetB0(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'EfficientNetB1':
                print("Loading EfficientNetB1..")
                core_model = EfficientNetB1(include_top=False,weights="imagenet",input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'EfficientNetB2':
                print("Loading EfficientNetB2..")
                core_model = EfficientNetB2(include_top=False, weights="imagenet", input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'EfficientNetB3':
                print("Loading EfficientNetB3..")
                core_model = EfficientNetB3(include_top=False, weights="imagenet", input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'EfficientNetB4':
                print("Loading EfficientNetB4..")
                core_model = EfficientNetB4(include_top=False, weights="imagenet", input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'EfficientNetB5':
                print("Loading EfficientNetB5..")
                core_model = EfficientNetB5(include_top=False, weights="imagenet", input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'EfficientNetB6':
                print("Loading EfficientNetB6..")
                core_model = EfficientNetB6(include_top=False, weights="imagenet", input_shape=data_config['IMAGE_SIZE'])

            elif self.model_name == 'EfficientNetB7':
                print("Loading EfficientNetB7..")
                core_model = EfficientNetB7(include_top=False, weights="imagenet", input_shape=data_config['IMAGE_SIZE'])

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

