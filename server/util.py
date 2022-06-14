import numpy as np
import cv2
import base64
from wavelet import w2d
import joblib 
import json

__class_name_to_number = {}
__class_number_to_name = {}
__model = None

def classify_image(image_base64_data, filepath=None):
    imgs = get_cropped_images_if_2_eyes(filepath, image_base64_data)

    result = []
    for img in imgs:
        scaled_raw_img = cv2.resize(img, (32, 32))
        img_har = w2d(img, 'db1', 5)
        scaled_har_img = cv2.resize(img_har, (32, 32))
        combined_img = np.vstack((scaled_raw_img.reshape(32*32*3, 1), scaled_har_img.reshape(32*32, 1)))

        len_img_array = 32 * 32 * 3 + 32 * 32

        final = combined_img.reshape(1, len_img_array).astype(float)

        # result.append(class_number_to_name(__model.predict(final)[0]))

        result.append({
            'class' : class_number_to_name(__model.predict(final)[0]),
            'class_probability': np.round(__model.predict_proba(final)*100, 2).tolist()[0],
            'class_dictionary': __class_name_to_number
        })
        return result


def get_cv2_image_from_base64_string(b64str):
    encoded_data =  b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img
    

def get_cropped_images_if_2_eyes(image_path, image_base64_data):
    face_cascade = cv2.CascadeClassifier('/media/darkdevil/2C3479B034797DA0/Data Science practice/celebrity_idetification/model/opencv/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('/media/darkdevil/2C3479B034797DA0/Data Science practice/celebrity_idetification/model/opencv/haarcascades/haarcascade_eye.xml')

    if image_path:
        img = cv2.imread(image_path)
    else:
        img = get_cv2_image_from_base64_string(image_base64_data)    

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    cropped_faces = []

    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            cropped_faces.append(roi_color)

    return cropped_faces        


def  get_b64_test_images_yash():
    with open("/media/darkdevil/2C3479B034797DA0/Data Science practice/celebrity_idetification/server/b64.txt") as f:
        return f.read()

def load_saved_artifacts():
    print("Loading saved artifacts...start")
    global __model
    global __class_name_to_number
    global __class_number_to_name

    with open("/media/darkdevil/2C3479B034797DA0/Data Science practice/celebrity_idetification/server/artifacts/class_dictionary.json", "r") as nf:
        __class_name_to_number = json.load(nf)
        __class_number_to_name = {v:k for k, v in __class_name_to_number.items()}
   
    
    with open("/media/darkdevil/2C3479B034797DA0/Data Science practice/celebrity_idetification/server/artifacts/saved_model.pkl", "rb") as f:
        __model = joblib.load(f)
    print("Loading saved artifacts...done")

def class_number_to_name(class_num):
    return __class_number_to_name[class_num]

if __name__ == "__main__":
    load_saved_artifacts()
    # print(classify_image(get_b64_test_images_yash(), None))

    # print(class_number_to_name(2))
    print(classify_image(None, "/media/darkdevil/2C3479B034797DA0/Data Science practice/celebrity_idetification/model/test_images/After Ram Charan-Yash_ Prabhas REACTS.jpg"))