from cv_image_suit.utils.normal_utils import models_config
import json

class config:
    """Public cv_image_suit utilities.
    This module is used as a shortcut to access all the symbols. Those symbols was
    exposed under train engine and predict engine.
    """
    def __init__(self,filename):
        self.filename =filename

    def load_data(self):
        with open(self.filename,'r') as f:
              params = json.load(f)
        return params

    def load_pred_data(self):
        with open("Config_Layer/pred_configs.json",'r') as f:
              params = json.load(f)
        return params

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


    def configureModel(self, params):
        self.pram = self.load_data()
        self.mc = models_config.modellconfig(self.pram)
        CONFIG = {
            'MODEL_OBJ' : self.mc.return_model(),
            'MODEL_NAME' : params['MODEL_NAME'],
            'EPOCHS' : params['EPOCHS'],
            'OPTIMIZER' : params['OPTIMIZER'],
            'FREEZE_ALL' : params['FREEZE_ALL'],
            'FREEZE_TILL' : params['FREEZE_TILL'],
            'RESUME' : params['RESUME']
        }

        return CONFIG