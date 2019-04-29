"""
Defines all layers, used for converting natural language into SayTeX Syntax.
All layers should subclass the layer interface defined in layers.py.
"""

from . import *

"""
The layer_id_to_class dictionary contains a mapping from a string identifying
a layer to the class implementing the layer. The string is used in config.py.
"""
layer_id_to_class = {
    "speech_recognition_error_correction": None,
    "capitalization": None,
    "spoken_number_recognition": None,
    "synonym_standardization": None,
    "from_to_recognition": None,
    "divided_by_recognition": None,
    "auto_completion_to_avoid_compile_errors": None,
    "prettification": None
}