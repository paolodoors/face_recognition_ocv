

# Reentrenamiento de un modelo
Aquí las instrucciones para reentrenar un modelo agregando nuevas categorías.
Tener en cuenta que las imágenes de la carpeta *images* ya han sido procesadas para un tamaño más óptimo y se han generado los xml que describen los labels de las imágenes.

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