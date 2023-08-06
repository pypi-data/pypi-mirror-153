import sys
from cv_image_suit.Logging_Layer.logger import App_Logger
import numpy
from cv_image_suit.com_in_ineuron_ai_utils.utils import decodeImage
from cv_image_suit.Prediction_Layer.predict import tfpredict
import json
import webbrowser
from threading import Timer
from cv_image_suit.Training_Layer.train_engine import tftrainer
from cv_image_suit.Experiment_Layer.model_finder import modelfinder
from os import listdir
import os
from tensorboard import program
from cv_image_suit.com_in_ineuron_ai_utils.utils import batch_validate
from cv_image_suit.Exception_Layer.exception import GenericException
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.encoders import jsonable_encoder

class ClientApp:
    def __init__(self,pred_dir=None):
        self.filename = "inputImage.jpg"
        self.pred_dir = pred_dir
        self.classifier = tfpredict(self.filename, self.pred_dir)
        self.tftraining = tftrainer()
        self.modelfinder = modelfinder("Config_Layer/experiment_inputs_configs.json")
        self.logger = App_Logger()



app = FastAPI() # initializing a flask app
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
    max_age=2
    )
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse) # route to display the home page
async def homePage(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/input2', response_class=HTMLResponse)  # route to display the home page
async def input_form2(request:Request):
    return templates.TemplateResponse("input_experiments.html", {"request": request})

@app.get('/input3',response_class=HTMLResponse)  # route to display the home page
async def input_form3(request:Request):
    exps=[]
    if os.path.isdir(os.getcwd() + "/Tensorboard/logs/"):
        for x in listdir(os.getcwd() + "/Tensorboard/logs/"):
            exps.append(x)
    if not isinstance(exps, list):
        exps = [exps]
    return templates.TemplateResponse("experiment_log.html", {"request": request, "exps":exps})

@app.get('/input',response_class=HTMLResponse)  # route to display the home page
def input_form(request:Request):
    model_list = []
    if os.path.isdir(os.getcwd()+"/New_trained_model"):
        for x in listdir(os.getcwd()+"/New_trained_model"):
            model_list.append(x)
    return templates.TemplateResponse("input_form.html", {"request": request, "model_list": model_list})

@app.get('/download',)
async def downloadFile():
    file_name = "experiment_result.json"
    file_path = os.getcwd() + "/Config_Layer/" + file_name
    return FileResponse(path=file_path, media_type='application/octet-stream', filename=file_name)

@app.get('/download2')
async def downloadFile2():
    file_name = "Predictions.csv"
    file_path = os.getcwd() + "/Prediction_Output_File/" + file_name
    return FileResponse(path=file_path, media_type='application/octet-stream', filename=file_name)

@app.post('/experiment',response_class=HTMLResponse)
async def experiment_func(request:Request,MODEL_OBJ: list = Form(),OPTIMIZER: list = Form()):

    clApp = ClientApp()
    try:
        form_data = await request.form()
        # Data config
        TRAIN_DATA_DIR = form_data['TRAIN_DATA_DIR']
        VALID_DATA_DIR = form_data['VALID_DATA_DIR']
        CLASSES = int(form_data['CLASSES'])
        IMAGE_SIZE = form_data['IMAGE_SIZE']
        AUGMENTATION = form_data['AUGMENTATION']
        BATCH_SIZE = form_data['BATCH_SIZE']
        PERCENT_DATA = int(form_data['PERCENTAGE_DATA'])

        BATCH = BATCH_SIZE.split(',')
        BATCH = [int(j) for j in BATCH]
        BATCH_SIZE = numpy.sort(BATCH)
        BATCH_SIZE = [int(j) for j in BATCH_SIZE]
        size = IMAGE_SIZE.split(',')
        size = [int(j) for j in size]
        if PERCENT_DATA > 100:
            return templates.TemplateResponse("input_experiments.html",
                                              {"request": request,
                                               "error": ["PERCENT_DATA cannot be more than 100"]}
                                              )
        size = numpy.sort(size)
        size = [int(j) for j in size]
        allowed_batch = batch_validate(TRAIN_DATA_DIR,VALID_DATA_DIR,PERCENT_DATA)
        if BATCH_SIZE[0] > allowed_batch:
            return templates.TemplateResponse("input_experiments.html",
                                              {"request": request,
                                               "error": ["Image size must be larger than 71x71 and last value must 3"]}
                                              )
        elif size[1] < 71 and size[0] != 3:
            return templates.TemplateResponse("input_experiments.html",
                                              {"request": request,
                                               "error": ["Image size must be larger than 71x71 and last value must 3"]}
                                              )

        MODEL_OBJ = MODEL_OBJ
        EXP_NAME = form_data['EXP_NAME']
        FREEZE_ALL = form_data['FREEZE_ALL']
        FREEZE_TILL = int(form_data['FREEZE_TILL'])
        OPTIMIZER = OPTIMIZER
        EPOCHS = int(form_data['EPOCHS'])

        configs = {
            "TRAIN_DATA_DIR": TRAIN_DATA_DIR,
            "VALID_DATA_DIR": VALID_DATA_DIR,
            "AUGMENTATION": AUGMENTATION,
            "CLASSES": CLASSES,
            "IMAGE_SIZE": IMAGE_SIZE,
            "BATCH_SIZE": BATCH_SIZE,
            "MODEL_OBJ": MODEL_OBJ,
            "EXP_NAME": EXP_NAME,
            "EPOCHS": EPOCHS,
            "FREEZE_ALL": FREEZE_ALL,
            "FREEZE_TILL": FREEZE_TILL,
            "OPTIMIZER": OPTIMIZER,
            "PERCENT_DATA": PERCENT_DATA
        }

        with open("Config_Layer/experiment_inputs_configs.json", "w") as f:
            json.dump(configs, f)
            f.close()

        Phase = "MODEL"
        best_model = clApp.modelfinder.find_model(phase=Phase)

        Phase = "IMAGE_SIZE"
        best_model = clApp.modelfinder.find_model(phase=Phase)

        Phase = "BATCH_SIZE"
        best_model = clApp.modelfinder.find_model(phase=Phase)

        Phase = "OPTIMIZER"
        best_model = clApp.modelfinder.find_model(phase=Phase)

        exps = []
        if os.path.isdir(os.getcwd() + "/Tensorboard/logs/"):
            for x in listdir(os.getcwd() + "/Tensorboard/logs/"):
                exps.append(x)
        if not isinstance(exps,list):
            exps = [exps]
        return templates.TemplateResponse("experiment_output.html",
                                          {"request": request,
                                           "model_list": best_model,
                                           "exps":exps}
                                          )
    except Exception as e:
        exception = GenericException(
            "Failed during training in module [{0}] class [{1}] method[{2}]"
                .format(ClientApp.__module__, ClientApp.__name__,
                        train_func.__name__))
        file = open("Logs/logs.txt", 'a+')
        exception_msg = exception.error_message_detail(str(e), sys)
        clApp.logger.log(file, "Exception occured %s " % exception_msg)
        file.close()
        raise Exception(exception_msg)


@app.post('/train',response_class=HTMLResponse) # route to show the predictions in a web UI
async def train_func(request:Request, ):

    clApp = ClientApp()
    try:
        form_data = await request.form()
        # Data config
        TRAIN_DATA_DIR = form_data['TRAIN_DATA_DIR']
        VALID_DATA_DIR = form_data['VALID_DATA_DIR']
        CLASSES =int(form_data['CLASSES'])
        IMAGE_SIZE = form_data['IMAGE_SIZE']
        AUGMENTATION = form_data['AUGMENTATION']
        BATCH_SIZE = int(form_data['BATCH_SIZE'])


        # Model config
        MODEL_OBJ = form_data['MODEL_OBJ']
        MODEL_NAME = form_data['MODEL_NAME']
        FREEZE_ALL = form_data['FREEZE_ALL']
        FREEZE_TILL = form_data['FREEZE_TILL']
        OPTIMIZER = form_data['OPTIMIZER']
        EPOCHS = int(form_data['EPOCHS'])
        RESUME = form_data['RESUME']

        size = IMAGE_SIZE.split(',')
        size = [int(j) for j in size]
        size = numpy.sort(size)
        size = [int(j) for j in size]
        PERCENT_DATA=100
        allowed_batch = batch_validate(TRAIN_DATA_DIR,VALID_DATA_DIR,PERCENT_DATA)
        if BATCH_SIZE > allowed_batch:
            return templates.TemplateResponse("input_form.html",
                                              {"request": request ,
                                               "error": ["Please provide smaller batch size"]})
        elif size[1] < 71 and size[0] != 3:
            return templates.TemplateResponse("input_form.html",
                                              {"request": request,
                                               "error": ["Image size must be larger than 71x71 and last value must 3"]})

        configs = {
            "TRAIN_DATA_DIR": TRAIN_DATA_DIR,
            "VALID_DATA_DIR": VALID_DATA_DIR,
            "AUGMENTATION": AUGMENTATION,
            "CLASSES": CLASSES,
            "IMAGE_SIZE": IMAGE_SIZE,
            "BATCH_SIZE": BATCH_SIZE,
            "MODEL_OBJ": MODEL_OBJ,
            "MODEL_NAME": MODEL_NAME,
            "EPOCHS": EPOCHS,
            "FREEZE_ALL": FREEZE_ALL,
            "FREEZE_TILL": FREEZE_TILL,
            "OPTIMIZER": OPTIMIZER,
            "RESUME": RESUME
        }

        with open("Config_Layer/configs.json", "w") as f:
            json.dump(configs, f)
            f.close()

        hist = clApp.tftraining.train()
        my_list = ["Traning Completed  ",hist]
        return templates.TemplateResponse("input_form.html",
                                          {"request": request,
                                           "output": my_list})
    except Exception as e:
        exception = GenericException(
            "Failed during training in module [{0}] class [{1}] method[{2}]"
            .format(ClientApp.__module__, ClientApp.__name__,
                     train_func.__name__))
        file = open("Logs/logs.txt", 'a+')
        exception_msg = exception.error_message_detail(str(e), sys)
        clApp.logger.log(file, "Exception occured %s " % exception_msg)
        file.close()
        raise Exception(exception_msg)

@app.get('/mid',response_class=HTMLResponse)  # route to display the home page
async def pred(request:Request):
    model_list = []
    if os.path.isdir(os.getcwd() + "/New_trained_model"):
        for x in listdir(os.getcwd()+"/New_trained_model"):
            model_list.append(x)
    return templates.TemplateResponse("mid_form.html", {"request": request, "model_list": model_list,"error":""})

@app.post('/test',response_class=HTMLResponse)  # route to display the home page
async def predcit(request:Request):
    form_data = await request.form()
    model_list = []
    if os.path.isdir(os.getcwd() + "/New_trained_model"):
        for x in listdir(os.getcwd() + "/New_trained_model"):
            model_list.append(x)
    model_found=0
    for x in model_list:
        if form_data['MODEL_NAME'] == x:
            model_found = 1
        else:
            model_found = 0
    if model_found == 0:
        return templates.TemplateResponse("mid_form.html", {"request": request, "model_list": model_list, "error": "Please Provide Model From Above List"})
    configs = {
        "MODEL_NAME": form_data['MODEL_NAME'],
        "PRED_TYPE": form_data['PRED_TYPE']
    }

    with open("Config_Layer/pred_configs.json", "w") as f:
        json.dump(configs, f)
        f.close()
    if form_data['PRED_TYPE'] == "Single Prediction":
        return templates.TemplateResponse("predict.html", {"request": request})
    else:
        return templates.TemplateResponse("predict_all.html", {"request": request})

@app.get('/logs',response_class=HTMLResponse)  # route to display the home page
async def log(request:Request):
    tracking_address = "Tensorboard/logs/fit"
    tb = program.TensorBoard()
    tb.configure(argv=[None, '--logdir', tracking_address])
    url = tb.launch()
    print(f"Tensorflow listening on {url}")
    webbrowser.open_new(url)
    return templates.TemplateResponse("input_form.html", {"request": request})

@app.post('/explogs',response_class=HTMLResponse)  # route to display the home page
async def log2(request:Request,exp: str = Form()):
    try:
        tracking_address = "Tensorboard/logs/"+exp
        tb = program.TensorBoard()
        tb.configure(argv=[None, '--logdir', tracking_address])
        url = tb.launch()
        webbrowser.open_new(url)
        print(f"Tensorflow listening on {url}")
        return templates.TemplateResponse("experiment_log.html", {"request": request,"url":url})
    except Exception as e:
        print(str(e))
        return templates.TemplateResponse("experiment_log.html", {"request": request})

@app.post("/predict")
async def predictRoute(request:Request,):
    clApp = ClientApp()
    img = await request.json()
    image = img['image']
    decodeImage(image, clApp.filename)
    result = clApp.classifier.predictiontf()
    return jsonable_encoder(result)

@app.post("/predict_all",response_class=HTMLResponse)
async def predictAllRoute(request:Request, PRED : str = Form()):
    clApp = ClientApp(PRED)
    result = clApp.classifier.predictiontf()
    return templates.TemplateResponse("predict_all.html", {"request": request, "error":["Prediction File Generated!!"]})

@app.get("/view_logs",response_class=HTMLResponse)
async def viewlogs(request:Request):
    with open('Logs/logs.txt','r') as f:
        lines = f.readlines()
        f.close()
    return templates.TemplateResponse("show_logs.html",
                                      {"request": request, "logs": lines})

def open_browser():
    webbrowser.open_new('http://127.0.0.1:8080/')


def start_app():
    Timer(3, open_browser).start()
    port = 8080
    uvicorn.run(app, host="0.0.0.0", port=port)



if __name__ == "__main__":
    start_app()
