

"""
The used_layers is a dictionary indicating which layers are to be used by SayTeX in
converting natural language into SayTeX Syntax. Changing the layers that are
in use will affect what spoken math expressions that SayTeX can recognize.
Each layer is represented by a string, which should correspond to a class
defined in layers.py. To add a layer, its subclass needs to be created in the layers
package, and the three dictionaries used_layers, layer_priorities and layer_id_to_class
should be updated.
"""
used_layers = {
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


import saytex.layers
"""
The layer_id_to_class dictionary contains a mapping from a string identifying
a layer to the class implementing the layer. The string is used in config.py.
"""
layer_id_to_class = {
    "speech_recognition_error_correction": saytex.layers.speech_recognition_error_correction.SpeechRecognitionErrorCorrection,
    "capitalization": None,
    "spoken_number_recognition": None,
    "synonym_standardization": None,
    "from_to_recognition": None,
    "divided_by_recognition": None,
    "auto_completion_to_avoid_compile_errors": None,
    "prettification": None
}