import json

import flask
from flask import request
from flask_cors import CORS
from flask import request

import keras 
from keras.models import Model
from keras.layers import *
from keras import optimizers
from keras.models import Sequential
from keras.models import load_model


import numpy as np
import io
import matplotlib.image as mpimg
import sys
import math
from PIL import Image
import cv2

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app, resources={r"*": {"origins": "*"}})

class GuessNumber():
    def __init__(self):
        self.modele = None

    def load_modele(self):
        self.modele = load_model('model.h5')

    def getNumberFromArray(self, my_array):
        return self.modele.predict(my_array)
	
    def test(self, my_array):
        print('la')
        print(len(my_array))
        return '{"1":"1"}'
        

demo = GuessNumber()
print("c'est parti !")

#@app.route('/load_new_modele', methods=['POST'])
#def new_model():
#     print('loading a new modele')
#     demo.load_modele()
#     return '{"0":"0"}'

@app.route('/guess_number', methods=['POST'])
def post_guess_number():
    """ Get an image in the form of an array and return a number """
      
    try:
        print("je recoit quelque chose")
        demo.load_modele()
        data = request.data
		
        fileBytes = io.BytesIO(data)
        file_ = Image.open(fileBytes)
        file_.save("data.png")
		
        image = file_.resize((28, 28), Image.ANTIALIAS)
        image.save("resultat_downsize.png")
		
        img = np.array(image)
        img = img[:,:,3:]
        #print(img.shape)
		
        img = img.flatten()
        #print(img.shape)
        img = np.expand_dims(img, axis=0)
		
        preds = demo.getNumberFromArray(img)[0]
        #print(preds)
        preds = ['{:.3f}'.format(i) for i in preds]
        #print(preds)
		
        preds = [str(i) for i in preds]
        chiffres = ['0','1','2','3','4','5','6','7','8','9']
        dictionary = dict(zip(chiffres, preds))
        print(dictionary)
		
        return flask.jsonify(**dictionary)
    except:
        print(sys.exc_info())
        return '{"reponse":"Something went wrong."}'



@app.route('/guess_number_old', methods=['POST'])
def post_guess_number_old():
    """ Get an image in the form of an array and return a number """
      
    try:
        print("je recoit quelque chose")
        demo.load_modele()
        data = request.data
      
        a = str(data).replace('x', '0x').split('\\')
        a = a[1:]
        a[-1] = a[-1][:-1]        
        a = [item for item in a if len(item) == 4]
               				
        data = [int(i[:4], 16) for i in a]

        data = data[3::4]
		
        int_ceil = math.ceil(math.sqrt(len(data)))
        int_ceil*=int_ceil
        #print(int_ceil)
        #print(len(data))
		
        if len(data) != int_ceil:
          for i in range(int_ceil-len(data)):
             data.append(0)
        
        #print(sum([1 for i in data if i==255]))
        img = np.reshape(data, (84, 84))
        
        #print(img.shape)
        mpimg.imsave("resultat.png", img)
        image = Image.open("resultat.png")
        image = image.resize((28, 28), Image.ANTIALIAS)
        
        image.save("resultat_downsize.png")
                
        img = np.array(image)
        img = img[:,:,:3]
        img = img.sum(axis=2)
        #img[img<255] = 0
        #img[img>=255] = 1
        img = np.subtract(img, img.min())
        img = np.divide(img, img.max())
        #print(img)
        #print(img.shape)
        img = img.flatten()
        #print(img.shape)
        img = np.expand_dims(img, axis=0)
        
        preds = demo.getNumberFromArray(img)[0]
        #print(preds)
        preds = ['{:.3f}'.format(i) for i in preds]
        #print(preds)
        preds = [str(i) for i in preds]
        chiffres = ['0','1','2','3','4','5','6','7','8','9']
        dictionary = dict(zip(chiffres, preds))
        print(dictionary)

        return flask.jsonify(**dictionary)
        #return '{"0":"0"}'
    except:
        print(sys.exc_info())
        return '{"reponse":"Something went wrong."}'
	

@app.route('/test', methods=['GET'])
def test_api():
	return "ca marche"



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,threaded=False)


