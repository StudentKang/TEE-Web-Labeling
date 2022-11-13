from flask import Flask,render_template, request,jsonify
from werkzeug.utils import secure_filename
from torchvision import transforms
from utils.utils import getJsonInfo
import SimpleITK as sitk
import cv2
import numpy as np
import os
import torch
from models.net import resnet34
import shutil

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
global filename
#Load Model
device = torch.device("cuda:{}".format(0) if torch.cuda.is_available() else "cpu")
model = resnet34(11).to(device)
assert os.path.exists("model_weights/res34.pth"), "file: '{}' dose not exist.".format("model_weights/resNet34.pth")
model.load_state_dict(torch.load("model_weights/res34.pth", map_location=device))
print("----Load Done----")



def dcm2classHashMap(dcmFilePath:str,framesNum:str,gtJsonPath:str,classJsonPath:str,model,device:str):
    """_summary_

    Args:
        dcmFilePath (str): Dcm file Path 
        framesNum (str):  Wanted frame num
        gtJsonPath (str): Path of GtJson
        classJsonPath (str): _description_
        model: Net Model
        device (str): device id
    """
    data_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5],std=[0.5])
        ])
    assert os.path.exists(classJsonPath), "file: '{}' dose not exist.".format(classJsonPath)


    model.eval()#eval

    # T1 = time.perf_counter()
    dicom = sitk.ReadImage(dcmFilePath)
    # T2 = time.perf_counter()
    # print(T2-T1)
    
    [x2,y2,x1,y1] = getJsonInfo(gtJsonPath)

    image = np.squeeze(sitk.GetArrayFromImage(dicom))
    total_frams = framesNum if (framesNum<image.shape[0]) else image.shape[0]

    cnt = 0
    res = {}
    maxNum = 0
    maxKey = ""

    flag = True
    picnum = 0
    # T1 = time.perf_counter()
    with torch.no_grad():
        for frame in range(total_frams): #img into video
            # print('frame')
            img = image[frame][:, :, (2, 1, 0)]   #plt to cv

            img = img[y1:y2,x1:x2]
            
            
            if(flag):
                cv2.imwrite(os.path.join("static","imgs",str(picnum)+'.jpg'),img)
                picnum += 1
            if(picnum>3):
                flag = False
        

            img = data_transform(img)
            img = torch.unsqueeze(img, dim=0)

            # cv2.imwrite(os.path.join(save_path_png,str(cnt)+'.jpg'),img[y1:y2,x1:x2])
            
            # predict class
            output = torch.squeeze(model(img.to(device))).cpu()
            predict = torch.softmax(output, dim=0)
            predict_cla = torch.argmax(predict).numpy()

            res[str(predict_cla)] = res.get(str(predict_cla),0)+1
            if(res[str(predict_cla)]>maxNum):
                maxNum = res[str(predict_cla)]
                maxKey = str(predict_cla)
            cnt += 1
            if(cnt>framesNum):
                break

    # T2 = time.perf_counter()
    # print(T2-T1)
    return int(maxKey)
    

@app.route('/')
def index():
    score=[1,2,3,4,5,6,7,8,9,10,11]
    return render_template("index.html",score=score)


@app.route('/predict', methods=['POST'])
def predict():
    global filename
    id = int(request.form.get('curpagenum'))
    # print(id)
    f = request.files.getlist("file")[id-1]
    filename = secure_filename(f.filename)
    # print(secure_filename(f.filename))
    dcm_path = os.path.join("tmp","dcm","temp_dcm")
    
    # T1 = time.perf_counter()
    f.save(dcm_path)
    # T2 = time.perf_counter()
    # print("保存耗时",T2-T1)
    index = dcm2classHashMap("tmp/dcm/temp_dcm",8,"cfg/GT.json","cfg/index.json",model,device)
    return jsonify({'index':index})


@app.route('/submit', methods=['POST'])
def submit():
    id = request.form.get("dcmclass")
    if(not os.path.exists(os.path.join("tmp","dcm","temp_dcm"))):
        return jsonify({'Log':"Failed!"})
    if(os.path.exists(os.path.join("tmp","dcm","temp_dcm"))):
        shutil.move(os.path.join("tmp","dcm","temp_dcm"),os.path.join("data",id,filename))
    return jsonify({'Log':"Successful Upload!"})



if __name__ == '__main__':

    app.run(host='127.0.0.1',port=5000,debug=True)