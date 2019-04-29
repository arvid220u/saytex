# add config variables


"""
The used_layers is a dictionary indicating which layers are to be used by SayTeX in
converting natural language into SayTeX Syntax. Changing the layers that are
in use will affect what spoken math expressions that SayTeX can recognize.
Each layer is represented by a string, which should correspond to a class
defined in layers.py. To add a layer, its subclass needs to be created and
the layer_id_to_class dictionary needs to be modified, both in layers.py, and
additionally the layer needs to be added to used_layers and layer_priorities
in config.py.
"""
used_layers = layer_priorities = {
    "speech_recognition_error_correction": True,
    "capitalization": True,
    "spoken_number_recognition": True,
    "synonym_standardization": True,
    "from_to_recognition": True,
    "divided_by_recognition": True,
    "auto_completion_to_avoid_compile_errors": True,
    "prettification": True
}


"""
The layer_priorities is a dictionary mapping layer ids to a number, reflecting
the in which order the layers should be executed. Layers are executed from low
to high priority. Layers with the same priority can be executed in any order; the
idea is that such layers are independent of each other. In designing new layers,
one should strive for not adding a new priority level. When disabling a layer,
remove
"""
layer_priorities = {
    "speech_recognition_error_correction": 0,
    "capitalization": 1,
    "spoken_number_recognition": 1,
    "synonym_standardization": 1,
    "from_to_recognition": 2, # this is debatable, but it kind of depends on the capitalization layer
    "divided_by_recognition": 2,
    "auto_completion_to_avoid_compile_errors": 3,
    "prettification": 3
}