from cv_image_suit.utils.normal_utils.config import config
import tensorflow as tf
from tensorflow.keras import models
import os
from cv_image_suit.Logging_Layer.logger import App_Logger
from cv_image_suit.Exception_Layer.exception import GenericException
import sys

class modell:
    def __init__(self):
        self.confige = config("Config_Layer/configs.json")
        self.logger = App_Logger()

    def get_model(self):
        """The logic for loading pretrain model.

         Args:
          MODEL_OBJ: Model object

        Returns:
          It returns keras model objcet

        """
        try:
            self.param = self.confige.load_data()
            self.config_model = self.confige.configureModel(self.param)
            self.config_data = self.confige.configureData(self.param)
            model =  self.config_model['MODEL_OBJ']
            print("Detected pretrain model!!")
            return model

        except Exception as e:
            exception = GenericException(
                "Failed during training in module [{0}] class [{1}] method[{2}]"
                    .format(self.__module__, modell.__name__,
                            self.get_model.__name__))
            file = open("Logs/logs.txt", 'a+')
            exception_msg = exception.error_message_detail(str(e), sys)
            self.logger.log(file, "Exception occured %s " % exception_msg)
            file.close()
            raise Exception(exception_msg)


    def model_preparation(self,model):
        try:
            print('Preparing model...')
            if self.config_model['RESUME'] == "True":
                model = tf.keras.models.load_model(os.getcwd()+"/Checkpoint/Model_ckpt.h5")
                return model
            else:
                if self.config_model['FREEZE_ALL'] == 'True':
                    print('Freezing all...')
                    for layer in model.layers:
                        layer.trainable = False

                    # Add custom layers
                    flatten_layer = tf.keras.layers.Flatten()

                    if self.config_data['CLASSES'] > 2:
                        print('Adding softmax...')
                        prediction = tf.keras.layers.Dense(
                            units=self.config_data['CLASSES'],
                            activation="softmax"
                        )  # (flatten_in)

                        full_model = models.Sequential([
                            model,
                            flatten_layer,
                            prediction
                        ])

                        full_model.compile(
                            optimizer=self.config_model['OPTIMIZER'],
                            loss="sparse_categorical_crossentropy",
                            metrics=["accuracy"]
                        )
                        print('Model loaded!!')

                        return full_model

                    else:
                        print('Adding sigmoid...')
                        prediction = tf.keras.layers.Dense(
                            units=1,
                            activation="sigmoid"
                        )  # (flatten_in)

                        full_model = models.Sequential([
                            model,
                            flatten_layer,
                            prediction
                        ])

                        full_model.compile(
                            optimizer=self.config_model['OPTIMIZER'],
                            loss="binary_crossentropy",
                            metrics=["accuracy"]
                        )

                        print('Model loaded!!')

                        return full_model

                else:

                    for layer in model.layers[:self.config_model['FREEZE_TILL']]:
                        layer.trainable = False
                    for layer in model.layers[self.config_model['FREEZE_TILL']:]:
                        layer.trainable = True

                    # Add custom layers
                    flatten_layer = tf.keras.layers.Flatten()  # (model.output)

                    if self.config_data['CLASSES'] > 2:
                        prediction = tf.keras.layers.Dense(
                            units=self.config_data['CLASSES'],
                            activation="softmax"
                        )  # (flatten_in)

                        full_model = models.Sequential([
                            model,
                            flatten_layer,
                            prediction
                        ])

                        full_model.compile(
                            optimizer=self.config_model['OPTIMIZER'],
                            loss="sparse_categorical_crossentropy",
                            metrics=["accuracy"]
                        )
                        print('Model loaded!!')

                        return full_model

                    else:
                        prediction = tf.keras.layers.Dense(
                            units=1,
                            activation="sigmoid"
                        )  # (flatten_in)

                        full_model = models.Sequential([
                            model,
                            flatten_layer,
                            prediction
                        ])

                        full_model.compile(
                            optimizer=self.config_model['OPTIMIZER'],
                            loss="binary_crossentropy",
                            metrics=["accuracy"]
                        )

                        print('Model loaded!!')

                        return full_model
        except Exception as e:
            exception = GenericException(
                "Failed during training in module [{0}] class [{1}] method[{2}]"
                    .format(self.__module__, modell.__name__,
                            self.get_model.__name__))
            file = open("Logs/logs.txt", 'a+')
            exception_msg = exception.error_message_detail(str(e), sys)
            self.logger.log(file, "Exception occured %s " % exception_msg)
            file.close()
            raise Exception(exception_msg)

    def load_pretrain_model(self):

        """The logic for loading pretrain model.

         Args:
          MODEL_OBJ: Model object

        Returns:
          It returns keras model objcet

        """
        try:
            model = self.get_model()
            model = self.model_preparation(model)
            return model
        except Exception as e:
            exception = GenericException(
                "Failed during training in module [{0}] class [{1}] method[{2}]"
                    .format(self.__module__, modell.__name__,
                            self.get_model.__name__))
            file = open("Logs/logs.txt", 'a+')
            exception_msg = exception.error_message_detail(str(e), sys)
            self.logger.log(file, "Exception occured %s " % exception_msg)
            file.close()
            raise Exception(exception_msg)











