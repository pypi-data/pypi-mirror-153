import sys

from cv_image_suit.utils.normal_utils.config import config
from cv_image_suit.utils.normal_utils import callbacks, data_manager, model
import tensorflow as tf
from cv_image_suit.Logging_Layer.logger import App_Logger
from cv_image_suit.Exception_Layer.exception import GenericException


class tftrainer:
    def __init__(self):
        self.confige = config("Config_Layer/configs.json")
        self.call = callbacks.callback()
        self.mod = model.modell()
        self.dm = data_manager.datamanage()
        self.logger = App_Logger()

    def train(self):

        """The logic for one training step.

        This method should contain the mathematical logic for one step of training.
        This typically includes the forward pass, loss calculation, backpropagation,
        and metric updates.

         Args:
          data: A nested structure of `Tensor`s.

        Returns:
          A `dict` containing values.Typically, the
          values of the `Model`'s metrics are returned. Example:
          `{'loss': 0.2, 'accuracy': 0.7}`.

        """
        try:
            self.param = self.confige.load_data()
            self.config_model = self.confige.configureModel(self.param)
            self.config_data = self.confige.configureData(self.param)
            self.log_dir = self.call.get_log_path()
            self.ckp = self.call.checkpoint()
            model_obj = self.mod.load_pretrain_model()
            my_model = model_obj

            #my_model.load_weights("cv_image_suit/Checkpoint/Model_ckpt.h5")

            train_data, valid_data = self.dm.train_valid_generator()

            #callbacks
            log_dir = self.log_dir
            tb_cb = tf.keras.callbacks.TensorBoard(log_dir=log_dir)
            model_checkpoint = self.ckp[0]
            early_stopping = self.ckp[1]
            lr_reducer = self.ckp[2]

            call = [tb_cb, model_checkpoint, early_stopping, lr_reducer]

            #Calculating steps_per_epoch & validation_steps
            steps_per_epoch = train_data.samples // train_data.batch_size
            validation_steps = valid_data.samples // valid_data.batch_size

            my_model.fit(
                train_data,
                validation_data=valid_data,
                epochs=self.config_model['EPOCHS'],
                steps_per_epoch=steps_per_epoch,
                validation_steps=validation_steps,
                callbacks=call
            )

            new_path = f"New_trained_model/{'new'+self.config_model['MODEL_NAME']+'.h5'}"
            my_model.save(new_path)
            return f"Model saved at the following location : {new_path}"
        except Exception as e:
            exception = GenericException(
                "Failed during training in module [{0}] class [{1}] method[{2}]"
                .format(self.__module__, tftrainer.__name__,
                         self.train.__name__))
            file = open("Logs/logs.txt", 'a+')
            exception_msg = exception.error_message_detail(str(e), sys)
            self.logger.log(file, "Exception occured %s " % exception_msg)
            file.close()
            raise Exception(exception_msg)

