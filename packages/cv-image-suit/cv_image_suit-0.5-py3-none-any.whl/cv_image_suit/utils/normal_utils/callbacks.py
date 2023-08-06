import os
import time
import tensorflow as tf

class callback:
    """Configures callbacks for use in various training loops.
      Args:
          get_log_path: unique log location.
          checkpoint : None
      Returns:
          Instance of CallbackList used to control all Callbacks.
     """
    def __init__(self):
        self.log_dir="Tensorboard/logs/fit"

    def get_log_path(self):
      fileName = time.strftime("log_%Y_%m_%d_%H_%M_%S")
      logs_path = os.path.join(self.log_dir, fileName)
      print(f"Saving logs at {logs_path}")
      return logs_path


    def checkpoint(self):
        CKPT_path = "Checkpoint/Model_ckpt.h5"
        checkpointing_cb = tf.keras.callbacks.ModelCheckpoint(CKPT_path, save_best_only=True)
        earlystoping = tf.keras.callbacks.EarlyStopping('val_loss',patience=8,verbose=1,mode='min')
        reducer = tf.keras.callbacks.ReduceLROnPlateau('val_loss',patience=5,verbose=1,mode='min',min_lr=0.00001)
        return  [checkpointing_cb,earlystoping,reducer]

