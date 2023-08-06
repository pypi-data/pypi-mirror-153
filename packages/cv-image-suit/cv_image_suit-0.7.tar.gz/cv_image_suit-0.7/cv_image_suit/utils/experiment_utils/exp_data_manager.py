from cv_image_suit.com_in_ineuron_ai_utils.utils import batch_validate
from cv_image_suit.utils.experiment_utils.exp_config import config
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from cv_image_suit.Logging_Layer.logger import App_Logger
from cv_image_suit.Exception_Layer.exception import GenericException
import sys

class datamanage:
    def __init__(self):
        self.confige = config("Config_Layer/experiment_inputs_configs.json")
        self.logger = App_Logger()

    def train_valid_generator(self,iteration=1,batch_iteration=1):

        '''
        This function generates train & valid data from images path,
        it also performs data augmentation.
        :return object of data:
        '''

        try:
            training_set=[]
            valid_set=[]
            class_mode = ""
            self.param = self.confige.load_data()
            self.config_data = self.confige.configureData(self.param)
            percentage = 100.0 - float(self.config_data['PERCENT_DATA'])
            percent = float(percentage / 100)
            sizes = self.config_data['IMAGE_SIZE']
            size = [int(j) for j in sizes]
            batch_size = self.config_data['BATCH_SIZE']

            print("batch Info-------------------")
            print(batch_iteration)
            #print(allowed_batch)

            allowed_batch = batch_validate(self.config_data['TRAIN_DATA_DIR'], self.config_data['VALID_DATA_DIR'], self.config_data['PERCENT_DATA'])

            for i in range(iteration):
                for j in range(batch_iteration):
                    if batch_size [j] > allowed_batch:
                        break
                    if self.config_data['CLASSES'] > 2:
                        class_mode = "sparse"
                    else:
                        class_mode = "binary"
                    if self.config_data['AUGMENTATION'] == 'True':
                        print("Augmetation applied!")
                        train_datagen = ImageDataGenerator(rescale=1. / 255,
                                                           shear_range=0.2,
                                                           zoom_range=0.2,
                                                           horizontal_flip=True,
                                                           validation_split=percent)

                        valid_datagen = ImageDataGenerator(rescale=1. / 255,
                                                           validation_split=percent)

                        train_set = train_datagen.flow_from_directory(
                            directory= self.config_data['TRAIN_DATA_DIR'],
                            target_size=(size[i],size[i]),
                            batch_size=int(batch_size[j]),
                            class_mode=class_mode,
                            subset='training')

                        val_set = valid_datagen.flow_from_directory(
                            directory=self.config_data['VALID_DATA_DIR'],
                            target_size=(size[i],size[i]),
                            batch_size=int(batch_size[j]),
                            class_mode=class_mode,
                            subset='training')
                        training_set.append(train_set)
                        valid_set.append(val_set)
                        #return training_set, valid_set

                    else:
                        train_datagen = ImageDataGenerator(rescale=1. / 255,validation_split=percent)
                        valid_datagen = ImageDataGenerator(rescale=1. / 255,validation_split=percent)

                        train_set = train_datagen.flow_from_directory(
                            directory=self.config_data['TRAIN_DATA_DIR'],
                            target_size=(size[i],size[i]),
                            batch_size=int(batch_size[j]),
                            class_mode=class_mode,
                            subset='training')

                        val_set = valid_datagen.flow_from_directory(
                            directory=self.config_data['VALID_DATA_DIR'],
                            target_size=(size[i],size[i]),
                            batch_size=int(batch_size[j]),
                            class_mode=class_mode,
                            subset='training')
                        training_set.append(train_set)
                        valid_set.append(val_set)
                        #return training_set, valid_set
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








