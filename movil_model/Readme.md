

# Reentrenamiento de un modelo
Aquí las instrucciones para reentrenar un modelo agregando nuevas categorías.
Tener en cuenta que las imágenes de la carpeta *images* ya han sido procesadas para un tamaño más óptimo y se han generado los xml que describen los labels de las imágenes.

**Nota:** los archivos xml del folder *annotation/xmls* tienen en su interior el path de la imagen que describen. Esos paths no son tenidos en cuenta por el script create_pet_tf_record.py.

1. Generar el archivo trainval.txt
Para generar el arhivo se debe ejecutar lo siguiente:

```
ls images | grep ".JPEG" | sed s/.JPEG// > annotations/trainval.txt
```

2. Generar los arhivos TFR para el dataset
Tensorflow API wants the datasets to be in TFRecord file format.
Ejecutar entonces el script:

```
python create_pet_tf_record.py
```

Este script **funciona sin parámetros** para la esctructura que viene por defecto. Si la estructura es diferente, se deben editar las siguientes líneas del archivo *create_pet_tf_record.py*:

```
flags.DEFINE_string('data_dir', 'images', 'Root directory to raw pet dataset.')
flags.DEFINE_string('output_dir', 'data', 'Path to directory to output TFRecords.')
flags.DEFINE_string('label_map_path', 'data/label.pbtxt',
                    'Path to label map proto')
```

Al correr el script se deberían haber generado los archivos *pet_train.record* y *pet_val.record* dentro de la carpeta data. Estos archivos son los que luego utilizaremos para reentrenar el modelo.

3. Ahora si, a reentrenar (tarda mucho!)

![Alt Text](https://media.giphy.com/media/rNgT8P8pL3dn2/giphy.gif)

Para poner a reentrenar el modelo, primero tenenos que:
* Seleccionar el modelo. [Link](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md)

* Elegir un archivo de configuración acorde a ese modelo. [Link](https://github.com/tensorflow/models/tree/master/research/object_detection/samples/configs)

En este caso, elegí el modelo faster_rcnn_resnet101_coco_2018_01_28.
Modificamos el archivo de configuración seleccionado y lo colocamos en la carpeta model con el nombre model.config

En este archivo debemos modificar los paths que correspondan y el número de clases:

```
model {
  faster_rcnn {
    num_classes: 2
```


```
  fine_tune_checkpoint: "<SOME_PATH>/faster_rcnn_resnet101_coco_2018_01_28/model.ckpt"
```

```
  train_input_reader: {
  tf_record_input_reader {
    input_path: "data/pet_train.record*"
  }
  label_map_path: "data/label.pbtxt"
}
```

```
eval_input_reader: {
  tf_record_input_reader {
    input_path: "data/pet_val.record*"
  }
  label_map_path: "data/label.pbtxt"
  shuffle: false
  num_readers: 1
}
```

Y ahora ejecutamos el archivo train.sh que contiene lo siguiente:

```
export PIPELINE_CONFIG_PATH=model/model.config
export MODEL_DIR=model/
export NUM_TRAIN_STEPS=50000
export SAMPLE_1_OF_N_EVAL_EXAMPLES=1

python ../models/research/object_detection/model_main.py \
    --pipeline_config_path=${PIPELINE_CONFIG_PATH} \
    --model_dir=${MODEL_DIR} \
    --num_train_steps=${NUM_TRAIN_STEPS} \
    --sample_1_of_n_eval_examples=$SAMPLE_1_OF_N_EVAL_EXAMPLES \
    --alsologtostderr
```

