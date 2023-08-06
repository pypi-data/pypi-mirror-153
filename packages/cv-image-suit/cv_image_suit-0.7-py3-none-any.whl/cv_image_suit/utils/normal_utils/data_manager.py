from cv_image_suit.utils.normal_utils.config import config
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import numpy as np
from cv_image_suit.Logging_Layer.logger import App_Logger
from cv_image_suit.Exception_Layer.exception import GenericException
import sys

class datamanage:
    def __init__(self):
        self.confige = config("Config_Layer/configs.json")
        self.logger = App_Logger()

    def train_valid_generator(self):

        '''
        This function generates train & valid data from images path,
        it also performs data augmentation.
        :return object of data:
        '''

        try:
            class_mode = ""
            self.param = self.confige.load_data()
            self.config_data = self.confige.configureData(self.param)
            if self.config_data['CLASSES'] > 2:
                class_mode = "sparse"
            else:
                class_mode = "binary"
            if self.config_data['AUGMENTATION'] == 'True':
                print("Augmetation applied!")
                train_datagen = ImageDataGenerator(rescale=1. / 255,
                                                   shear_range=0.2,
                                                   zoom_range=0.2,
                                                   horizontal_flip=True)

                valid_datagen = ImageDataGenerator(rescale=1. / 255)

                training_set = train_datagen.flow_from_directory(
                    directory= self.config_data['TRAIN_DATA_DIR'],
                    target_size=self.config_data['IMAGE_SIZE'][:-1],
                    batch_size=self.config_data['BATCH_SIZE'],
                    class_mode=class_mode)

                valid_set = valid_datagen.flow_from_directory(
                    directory=self.config_data['VALID_DATA_DIR'],
                    target_size=self.config_data['IMAGE_SIZE'][:-1],
                    batch_size=self.config_data['BATCH_SIZE'],
                    class_mode=class_mode)

                return training_set, valid_set

            else:
                train_datagen = ImageDataGenerator(rescale=1. / 255)
                valid_datagen = ImageDataGenerator(rescale=1. / 255)

                training_set = train_datagen.flow_from_directory(
                    directory=self.config_data['TRAIN_DATA_DIR'],
                    target_size=self.config_data['IMAGE_SIZE'][:-1],
                    batch_size=self.config_data['BATCH_SIZE'],
                    class_mode=class_mode)

                valid_set = valid_datagen.flow_from_directory(
                    directory=self.config_data['VALID_DATA_DIR'],
                    target_size=self.config_data['IMAGE_SIZE'][:-1],
                    batch_size=self.config_data['BATCH_SIZE'],
                    class_mode=class_mode)

                return training_set, valid_set
        except Exception as e:
            exception = GenericException(
                "Failed during training in module [{0}] class [{1}] method[{2}]"
                .format(self.__module__, datamanage.__name__,
                         self.train_valid_generator.__name__))
            file = open("Logs/logs.txt", 'a+')
            exception_msg = exception.error_message_detail(str(e), sys)
            self.logger.log(file, "Exception occured %s " % exception_msg)
            file.close()


    def class_name(self):
        try:
            train, valid = self.train_valid_generator()
            return train.class_indices
        except Exception as e:
            exception = GenericException(
                "Failed during training in module [{0}] class [{1}] method[{2}]"
                .format(self.__module__, datamanage.__name__,
                         self.train_valid_generator.__name__))
            file = open("Logs/logs.txt", 'a+')
            exception_msg = exception.error_message_detail(str(e), sys)
            self.logger.log(file, "Exception occured %s " % exception_msg)
            file.close()


    def manage_input_data(self,INPUT_IMAGE):
        '''
        This function takes an new raw image & convert the image
        into nd array with respect to training images dimention.
        :param INPUT_IMAGE:
        :return nd array:
        '''
        try:
            self.param = self.confige.load_data()
            self.config_data = self.confige.configureData(self.param)
            INPUT_IMG = INPUT_IMAGE
            test_image = image.load_img(INPUT_IMG, target_size= self.config_data['IMAGE_SIZE'][:-1])
            test_image = image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis=0)

            return test_image
        except Exception as e:
            exception = GenericException(
                "Failed during training in module [{0}] class [{1}] method[{2}]"
                    .format(self.__module__, datamanage.__name__,
                            self.train_valid_generator.__name__))
            file = open("Logs/logs.txt", 'a+')
            exception_msg = exception.error_message_detail(str(e), sys)
            self.logger.log(file, "Exception occured %s " % exception_msg)
            file.close()