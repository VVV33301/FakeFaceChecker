import tensorflow as tf
from PIL import Image
import numpy as np

model: tf.keras.Model = tf.keras.models.load_model('fakevsreal_weights_best_1.h5')


def classify_image(file_path: str | bytes | bytearray) -> str:
    image: Image = Image.open(file_path).resize((128, 128)).convert("RGB")
    img: np.array = np.asarray(image)
    img: np.array = np.expand_dims(img, 0)
    predictions: tf.keras.Model.predict = model.predict(img / 255)
    return f"Эта фотография {['реальная', 'фейковая'][np.argmax(predictions[0])]} с вероятностью " \
           f"{round(max(predictions[0]) * 100, 2)}%"
