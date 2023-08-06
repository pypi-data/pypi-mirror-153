import json
import sys

import numpy
import tensorflow as tf

from cv_image_suit.Exception_Layer.exception import GenericException
from cv_image_suit.utils.experiment_utils.exp_config import config
from cv_image_suit.utils.experiment_utils import exp_model, exp_callbacks, exp_data_manager
from cv_image_suit.Logging_Layer.logger import App_Logger

class modelfinder:
    def __init__(self,filename):
        self.filename = filename
        self.config = config(self.filename)
        self.call = exp_callbacks.callback()
        self.mod = exp_model.modell()
        self.dm = exp_data_manager.datamanage()
        self.logger = App_Logger()

    def find_model(self,phase,model_iteration=1):
        try:
            self.phase = phase
            param = self.config.load_data()

            final_data = self.config.configureData(param)
            batch_iteration = 0
            model_names = param['MODEL_OBJ']
            if not isinstance(model_names,list):
                model_names = [model_names]

            final_model_data = self.config.configureModel(param)
            self.log_dir = self.call.get_log_path()

            log_dir = self.log_dir
            tb_cb = tf.keras.callbacks.TensorBoard(log_dir=log_dir)
            call = [tb_cb]

            if self.phase == "BATCH_SIZE":
                temp = final_data['BATCH_SIZE']
                batch_iteration = len(temp)
                train_data, valid_data = self.dm.train_valid_generator(batch_iteration=batch_iteration)
                with open("Config_Layer/experiment_result.json", "r") as f:
                    json_obj = json.load(f)
                    f.close()
                model_names = json_obj["MODEL_OBJ"]
                model_names = [model_names]
                z = len(model_names) - 1
                batch_iteration = len(train_data)
                model_obj = self.mod.load_pretrain_model(self.phase,batch_iteration=batch_iteration)
                my_model = model_obj
                acc = self.find_batchsize(my_model, model_names, z, final_data, batch_iteration, final_model_data,
                                          train_data, valid_data, call)
                best_model = self.write_model_result(acc)
                return best_model
            elif self.phase == "IMAGE_SIZE":
                temp = final_data['IMAGE_SIZE']
                img_iteration = len(temp)-1
                train_data, valid_data = self.dm.train_valid_generator(img_iteration)
                with open("Config_Layer/experiment_result.json", "r") as f:
                    json_obj = json.load(f)
                    f.close()
                model_names=json_obj["MODEL_OBJ"]
                model_names=[model_names]
                z = len(model_names)-1
                model_obj = self.mod.load_pretrain_model(self.phase,img_iteration=img_iteration)
                my_model = model_obj
                acc = self.find_imagesize(my_model, model_names, z, phase, final_data, img_iteration, final_model_data,
                                          train_data, valid_data, call)
                best_model = self.write_model_result(acc)
                return best_model
            elif self.phase == "OPTIMIZER":
                train_data, valid_data = self.dm.train_valid_generator()
                with open("Config_Layer/experiment_result.json", "r") as f:
                    json_obj = json.load(f)
                    f.close()
                opt = final_model_data['OPTIMIZER']
                opt_iteration = len(opt)
                model_names=json_obj["MODEL_OBJ"]
                model_names=[model_names]
                z = len(model_names)-1
                model_obj = self.mod.load_pretrain_model(self.phase,opt_iteration=opt_iteration)
                my_model = model_obj
                acc = self.optimizer_find(my_model, model_names,z,opt,opt_iteration, final_model_data, train_data, valid_data, call)
                best_model = self.write_model_result(acc)
                return best_model
            else:
                img_iteration=1
                train_data, valid_data = self.dm.train_valid_generator(img_iteration)
                z = len(model_names) - 1
                model_obj = self.mod.load_pretrain_model(self.phase)
                my_model = model_obj
                acc = self.model_find(my_model, model_names, final_data, final_model_data, train_data, valid_data, call)
                best_model = self.write_model_result(acc)
                return best_model
        except Exception as e:
            exception = GenericException(
                "Failed during training in module [{0}] class [{1}] method[{2}]"
                .format(self.__module__, modelfinder.__name__,
                         self.find_model.__name__))
            file = open("Logs/logs.txt", 'a+')
            exception_msg = exception.error_message_detail(str(e), sys)
            self.logger.log(file, "Exception occured %s " % exception_msg)
            file.close()
            raise Exception(exception_msg)


    def model_find(self,my_model,model_names,final_data,final_model_data,train_data,valid_data,call):
        try:
            acc = {}
            i = 0
            image_size = final_data["IMAGE_SIZE"]
            temp = len(image_size)-1
            h = str(image_size[0])
            w = str(image_size[0])
            ch = str(image_size[temp])
            image_size = str(h+','+w+','+ch)

            steps_per_epoch = (train_data[0].samples // valid_data[0].batch_size)
            validation_steps = (train_data[0].samples // valid_data[0].batch_size)
            print(my_model)
            for x in my_model:
                history = x.fit(
                    train_data[0],
                    validation_data=valid_data[0],
                    epochs=final_model_data['EPOCHS'],
                    steps_per_epoch=steps_per_epoch,
                    validation_steps=validation_steps,
                    callbacks=call
                )
                val_acc = history.history['val_accuracy']
                res=0
                for val in val_acc:
                    res = res+val
                res = res/len(val_acc)
                acc[res]=[model_names[i], image_size, valid_data[0].batch_size,res]
                i = i + 1
            return acc
        except Exception as e:
            exception = GenericException(
                "Failed during training in module [{0}] class [{1}] method[{2}]"
                .format(self.__module__, modelfinder.__name__,
                         self.model_find.__name__))
            file = open("Logs/logs.txt", 'a+')
            exception_msg = exception.error_message_detail(str(e), sys)
            self.logger.log(file, "Exception occured %s " % exception_msg)
            file.close()


    def write_model_result(self,acc,opt = "Adam"):
        try:
            temp = []
            for res in acc.keys():
                temp.append(res)
            max_acc = numpy.max(temp)
            best_model = acc[max_acc]
            if self.phase == "OPTIMIZER":
                CONFIG = {"MODEL_OBJ": best_model[0],
                          "IMAGE_SIZE": best_model[1],
                          "BATCH_SIZE": best_model[2],
                          "VAL_ACC": best_model[3],
                          "OPTIMIZER": best_model[4]
                          }
            else:
                CONFIG = {"MODEL_OBJ": best_model[0],
                          "IMAGE_SIZE": best_model[1],
                          "BATCH_SIZE": best_model[2],
                          "VAL_ACC": best_model[3],
                          "OPTIMIZER": opt
                          }

            with open("Config_Layer/experiment_result.json", "w") as f:
                json.dump(CONFIG, f)
            return CONFIG
        except Exception as e:
            exception = GenericException(
                "Failed during training in module [{0}] class [{1}] method[{2}]"
                .format(self.__module__, modelfinder.__name__,
                         self.write_model_result.__name__))
            file = open("Logs/logs.txt", 'a+')
            exception_msg = exception.error_message_detail(str(e), sys)
            self.logger.log(file, "Exception occured %s " % exception_msg)
            file.close()


    def fetch_img_size(self):
        with open("Config_Layer/experiment_result.json", "r") as f:
            jason_obj = json.load(f)
            img_size = jason_obj["IMAGE_SIZE"]
            f.close()
        return img_size

    def fetch_batch(self):
        with open("Config_Layer/experiment_result.json", "r") as f:
            jason_obj = json.load(f)
            batch_size = jason_obj["BATCH_SIZE"]
            f.close()
        return batch_size

    def optimizer_find(self,my_model,model_names,z,opt,opt_iteration,final_model_data,train_data,valid_data,call):
        try:
            acc = {}
            image_size = self.fetch_img_size()
            batch = self.fetch_batch()
            steps_per_epoch = (train_data[0].samples // valid_data[0].batch_size)
            validation_steps = (train_data[0].samples // valid_data[0].batch_size)

            for k in range(opt_iteration):
                history = my_model[k].fit(
                    train_data[0],
                    validation_data=valid_data[0],
                    epochs=final_model_data['EPOCHS'],
                    steps_per_epoch=steps_per_epoch,
                    validation_steps=validation_steps,
                    callbacks=call
                )
                val_acc = history.history['val_accuracy']
                res=0
                for val in val_acc:
                    res = res+val
                res = res/len(val_acc)
                acc[res]=[model_names[z], str(image_size),batch,res,opt[k]]
            return acc
        except Exception as e:
            exception = GenericException(
                "Failed during training in module [{0}] class [{1}] method[{2}]"
                .format(self.__module__, modelfinder.__name__,
                         self.optimizer_find.__name__))
            file = open("Logs/logs.txt", 'a+')
            exception_msg = exception.error_message_detail(str(e), sys)
            self.logger.log(file, "Exception occured %s " % exception_msg)
            file.close()


    def find_batchsize(self,my_model,model_names,z,final_data,batch_iteration,final_model_data,train_data,valid_data,call):
        try:
            acc = {}
            batch_size = final_data["BATCH_SIZE"]
            image_size = self.fetch_img_size()
            for k in range(len(train_data)):
                steps_per_epoch = (train_data[k].samples // valid_data[k].batch_size)
                validation_steps = (train_data[k].samples // valid_data[k].batch_size)

                history = my_model[k].fit(
                    train_data[k],
                    validation_data=valid_data[k],
                    epochs=final_model_data['EPOCHS'],
                    steps_per_epoch=steps_per_epoch,
                    validation_steps=validation_steps,
                    callbacks=call
                )
                val_acc = history.history['val_accuracy']
                res=0
                for val in val_acc:
                    res = res+val
                res = res/len(val_acc)
                acc[res]=[model_names[z], str(image_size), batch_size[k],res]
            return acc
        except Exception as e:
            exception = GenericException(
                "Failed during training in module [{0}] class [{1}] method[{2}]"
                .format(self.__module__, modelfinder.__name__,
                         self.find_batchsize.__name__))
            file = open("Logs/logs.txt", 'a+')
            exception_msg = exception.error_message_detail(str(e), sys)
            self.logger.log(file, "Exception occured %s " % exception_msg)
            file.close()


    def find_imagesize(self,my_model,model_names,z,phase,final_data,img_iteration,final_model_data,train_data,valid_data,call):
        try:
            acc = {}
            i = 0
            j = 0
            image_size = final_data["IMAGE_SIZE"]
            for k in range(img_iteration):

                steps_per_epoch = (train_data[k].samples // valid_data[k].batch_size)
                validation_steps = (train_data[k].samples // valid_data[k].batch_size)

                n = len(my_model)
                if i < n:
                    history = my_model[i].fit(
                        train_data[j],
                        validation_data=valid_data[j],
                        epochs=final_model_data['EPOCHS'],
                        steps_per_epoch=steps_per_epoch,
                        validation_steps=validation_steps,
                        callbacks=call
                    )
                    val_acc = history.history['val_accuracy']
                    res=0
                    for val in val_acc:
                        res = res+val
                    res = res/len(val_acc)
                    ch = len(image_size)-1
                    acc[res]=[model_names[z], str(image_size[k])+','+str(image_size[k])+','+str(image_size[ch]), valid_data[k].batch_size,res]
                    i = i + 1
                j = j + 1
            return acc
        except Exception as e:
            exception = GenericException(
                "Failed during training in module [{0}] class [{1}] method[{2}]"
                .format(self.__module__, modelfinder.__name__,
                         self.find_imagesize.__name__))
            file = open("Logs/logs.txt", 'a+')
            exception_msg = exception.error_message_detail(str(e), sys)
            self.logger.log(file, "Exception occured %s " % exception_msg)
            file.close()











