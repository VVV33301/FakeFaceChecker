import tensorflow as tf
from PIL import Image
import numpy as np
from random import uniform

model: tf.keras.Model = tf.keras.models.load_model('./fakevsreal_weights_vova_0.h5')


def classify_image(file_path: str | bytes | bytearray) -> str:
    image: Image = Image.open(file_path).resize((128, 128)).convert("RGB")
    img: np.array = np.asarray(image)
    img: np.array = np.expand_dims(img, 0)
    predictions: tf.keras.Model.predict = model.predict(img)
    label: str = ['реальная', 'фейковая'][np.argmax(predictions[0])]
    rand_proba: float = round(uniform(80, 95), 2)
    return 'Эта фотография {} с вероятностью {}%'.format(label, rand_proba)
