import sys
from os import listdir
import numpy as np
import pandas
from tensorflow.keras.models import load_model

from cv_image_suit.com_in_ineuron_ai_utils.utils import decodeImage, encodeImageIntoBase64
from cv_image_suit.utils.normal_utils import data_manager
from cv_image_suit.utils.normal_utils.config import config
from cv_image_suit.Exception_Layer.exception import GenericException
from cv_image_suit.Logging_Layer.logger import App_Logger
class tfpredict:
    def __init__(self,filename, pred_dir=None):
        self.filename =filename
        self.confige = config("Config_Layer/configs.json")
        self.dm = data_manager.datamanage()
        self.logger = App_Logger()
        self.pred_dir = pred_dir
    def predictiontf(self):
        try:
            self.param = self.confige.load_data()
            self.config_model = self.confige.load_pred_data()
            self.data_config = self.confige.configureData(self.param)

            # load model
            model_path = f"New_trained_model/{self.config_model['MODEL_NAME']}"
            print('Loading...', model_path)
            model = load_model(model_path)

            # summarize model
            #model.summary()

            names = self.dm.class_name()
            class_names = list(names.keys())
            if self.config_model['PRED_TYPE'] == 'Single Prediction':
                imagename = self.filename
                predict = self.dm.manage_input_data(imagename)
                if self.data_config['CLASSES'] > 2:
                    result = model.predict(predict/255)
                    results = np.argmax(result)
                    return [{ "image_class" : str(class_names[results])}]
                else:
                    result = model.predict(predict/255)
                    predicted_classes = [1 * (x[0] >= 0.5) for x in result]
                    return [{ "image_class" : str(class_names[predicted_classes[0]])}]
            else:
                predictions=[]
                img_names=[]
                for x in listdir(self.pred_dir):
                    x_encode = encodeImageIntoBase64(self.pred_dir+'/'+x)
                    decodeImage(x_encode, self.filename)
                    predict = self.dm.manage_input_data(self.filename)
                    if self.data_config['CLASSES'] > 2:
                        result = model.predict(predict/255)
                        results = np.argmax(result)
                        predictions.append(str(class_names[results]))
                        img_names.append(str(x))

                        #return [{ "image_class" : str(class_names[results])}]
                    else:
                        result = model.predict(predict/255)
                        predicted_classes = [1 * (x[0] >= 0.5) for x in result]
                        predictions.append(str(class_names[predicted_classes[0]]))
                        img_names.append(str(x))
                        #return [{ "image_class" : str(class_names[predicted_classes[0]])}]
                result_dataframe = pandas.DataFrame(list(zip(img_names,predictions)), columns=['Image', 'Predictions'])
                path = "Prediction_Output_File/"
                result_dataframe.to_csv(path + "Predictions.csv", header=True, mode='w')
                return path + "Predictions.csv"
        except Exception as e:
            exception = GenericException(
                "Failed during training in module [{0}] class [{1}] method[{2}]"
                .format(self.__module__, tfpredict.__name__,
                         self.predictiontf.__name__))
            file = open("Logs/logs.txt", 'a+')
            exception_msg = exception.error_message_detail(str(e), sys)
            self.logger.log(file, "Exception occured %s " % exception_msg)
            file.close()
            raise Exception(exception_msg)





