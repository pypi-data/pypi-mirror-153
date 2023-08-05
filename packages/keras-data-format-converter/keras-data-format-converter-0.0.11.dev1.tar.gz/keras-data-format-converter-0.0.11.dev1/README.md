# Keras data format converter

Generates equal keras models with the desired data format  


## Requirements
tensorflow >= 2.0


## API
`convert_channels_first_to_last(model: keras.Model, inputs_to_transpose: List[str] = None, verbose: bool = False) -> keras.Model`

`convert_channels_last_to_first(model: tf.keras.Model, inputs_to_transpose: List[str] = None, verbose: bool = False) \
        -> tf.keras.Model`

`model`: Keras model to convert

`inputs_to_transpose`: list of input names that need to be transposed due tothe data foramt changing  

`verbose`: detailed output

## Getting started

```python
from tensorflow import keras
from keras_data_format_converter import convert_channels_last_to_first

# Load Keras model
keras_model = keras.models.load_model("my_image_model")

# Call the converter (image_input is an input that needs to be transposed, can be different for your model)
converted_model = convert_channels_last_to_first(keras_model, ["image_input"])
```

## Supported Layers with Special handling
- [X] Normalization layers
- [x] Permute
- [x] Reshape
- [x] Concatenate
- [ ] Dot
- [ ] MultiHeadAttention
- [ ] TFOpLambda (Inserted by the Functional API construction whenever users call
  a supported TF symbol on KerasTensors, see [here](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/keras/layers/core.py#L1284) at Tensorflow repo for more info)

## Unsupported Layers due to lack of data_format property
- Cropping1D
- Upsampling1D
- Zeropadding1D
- All layers in tensorflow.keras.preprocessing

## How to deploy
- Create a new release version on GitHub
- Update parameters in setup.py (usually `version` and `download_url`)
- Run `python setup.py sdist` in root directory
- Run `pip install twine`
- Run `twine upload dist/*`
 


## License
This software is covered by MIT License.
