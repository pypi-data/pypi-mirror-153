import json

from cv_image_suit.utils.experiment_utils.exp_config import config
import tensorflow as tf
from tensorflow.keras import models
from cv_image_suit.utils.experiment_utils import exp_models_config
from cv_image_suit.Logging_Layer.logger import App_Logger
from cv_image_suit.Exception_Layer.exception import GenericException
import sys

class modell:
    def __init__(self):
        self.confige = config("Config_Layer/experiment_inputs_configs.json")
        self.logger = App_Logger()


    def get_model(self,phase,img_iteration=1,batch_iteration=1,opt_iteration=1):
        """The logic for loading pretrain model.

         Args:
          MODEL_OBJ: Model object

        Returns:
          It returns keras model objcet

        """
        try:

            self.param = self.confige.load_data()
            if phase == "IMAGE_SIZE":
                size = self.param['IMAGE_SIZE'].split(',')
                img_iteration = len(size) - 1
                with open("Config_Layer/experiment_result.json", "r") as f:
                    jason_param = json.load(f)
                    f.close()
                self.mc = exp_models_config.modellconfig(jason_param)
            elif phase == "BATCH_SIZE":
                with open("Config_Layer/experiment_result.json", "r") as f:
                    jason_param = json.load(f)
                    f.close()
                self.mc = exp_models_config.modellconfig(jason_param)
            elif phase == "OPTIMIZER":
                with open("Config_Layer/experiment_result.json", "r") as f:
                    jason_param = json.load(f)
                    f.close()
                self.mc = exp_models_config.modellconfig(jason_param)
            else:
                self.mc = exp_models_config.modellconfig(self.param)
            self.config_model = self.confige.configureModel(self.param)
            self.model = self.mc.return_model(self.param,img_iteration,batch_iteration,opt_iteration)
            self.config_data = self.confige.configureData(self.param)
            model = self.model
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
            final_models = []
            i=0
            opt=self.config_model['OPTIMIZER']
            if isinstance(opt, list):
                print("list")
            else:
                opt = [opt]
            for x in model:
                print('Preparing model...')
                if self.config_model['FREEZE_ALL'] == 'True':
                    print('Freezing all...')
                    for layer in x.layers:
                        layer.trainable = False

                    # Add custom layers
                    flatten_layer = tf.keras.layers.Flatten()

                    if self.config_data['CLASSES'] > 2:
                        print('Adding softmax...')
                        prediction = tf.keras.layers.Dense(
                            units=self.config_data['CLASSES'],
                            activation="softmax"
                        )#(flatten_in)

                        full_model = models.Sequential([
                                        x,
                                        flatten_layer,
                                        prediction
                                    ])

                        full_model.compile(
                            optimizer=opt[i],
                            loss="sparse_categorical_crossentropy",
                            metrics=["accuracy"]
                        )
                        print('Model loaded!!')

                        final_models.append(full_model)
                        i=i+1
                    else:
                        print('Adding sigmoid...')
                        prediction = tf.keras.layers.Dense(
                            units=1,
                            activation="sigmoid"
                        )#(flatten_in)

                        full_model = models.Sequential([
                                        x,
                                        flatten_layer,
                                        prediction
                                    ])

                        full_model.compile(
                            optimizer=opt[i],
                            loss="binary_crossentropy",
                            metrics=["accuracy"]
                        )

                        print('Model loaded!!')

                        final_models.append(full_model)
                        i=i+1

                else:

                    for layer in x.layers[:self.config_model['FREEZE_TILL']]:
                        layer.trainable = False
                    for layer in x.layers[self.config_model['FREEZE_TILL']:]:
                        layer.trainable = True

                        # Add custom layers
                    flatten_layer = tf.keras.layers.Flatten()#(model.output)

                    if self.config_data['CLASSES'] > 2:
                        prediction = tf.keras.layers.Dense(
                            units=self.config_data['CLASSES'],
                            activation="softmax"
                        )#(flatten_in)

                        full_model = models.Sequential([
                            x,
                            flatten_layer,
                            prediction
                        ])

                        full_model.compile(
                            optimizer=opt[i],
                            loss="sparse_categorical_crossentropy",
                            metrics=["accuracy"]
                        )
                        print('Model loaded!!')

                        final_models.append(full_model)
                        i=i+1

                    else:
                        prediction = tf.keras.layers.Dense(
                            units=1,
                            activation="sigmoid"
                        )#(flatten_in)

                        full_model = models.Sequential([
                            x,
                            flatten_layer,
                            prediction
                        ])

                        full_model.compile(
                            optimizer=opt[i],
                            loss="binary_crossentropy",
                            metrics=["accuracy"]
                        )

                        print('Model loaded!!')

                        final_models.append(full_model)
                        i=i+1
            return final_models
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


    def load_pretrain_model(self,phase,img_iteration=1,batch_iteration=1,opt_iteration=1):

        """The logic for loading pretrain model.

         Args:
          MODEL_OBJ: Model object

        Returns:
          It returns keras model objcet

        """
        try:
            model = self.get_model(phase,img_iteration,batch_iteration,opt_iteration)
            models = self.model_preparation(model)
            return models
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












