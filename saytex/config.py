


used_layers = {
    "speech_recognition_error_correction": True,
    "case_insensitivity": True,
    "capitalization": True,
    "spoken_number_recognition": True,
    "synonym_standardization": True,
    "from_to_recognition": True,
    "divided_by_recognition": True,
    "auto_completion_to_avoid_compile_errors": False,
    "prettification": False
}
"""
The used_layers is a dictionary indicating which layers are to be used by SayTeX in
converting natural language into SayTeX Syntax. Changing the layers that are
in use will affect what spoken math expressions that SayTeX can recognize.
Each layer is represented by a string, which should correspond to a class
defined in layers.py. To add a layer, its subclass needs to be created in the layers
package, and the three dictionaries used_layers, layer_priorities and layer_id_to_class
should be updated.
"""



layer_priorities = {
    "speech_recognition_error_correction": 0,
    "case_insensitivity": 0,
    "capitalization": 1,
    "spoken_number_recognition": 1,
    "synonym_standardization": 1,
    "from_to_recognition": 2, # this is debatable, but it kind of depends on the capitalization layer
    "divided_by_recognition": 2,
    "auto_completion_to_avoid_compile_errors": 3,
    "prettification": 3
}
"""
The layer_priorities is a dictionary mapping layer ids to a number, reflecting
the in which order the layers should be executed. Layers are executed from low
to high priority. Layers with the same priority can be executed in any order; the
idea is that such layers are independent of each other. In designing new layers,
one should strive for not adding a new priority level.
"""


from saytex.layers.speech_recognition_error_correction import SpeechRecognitionErrorCorrectionLayer
from saytex.layers.capitalization import CapitalizationLayer
from saytex.layers.spoken_number_recognition import SpokenNumberRecognitionLayer
from saytex.layers.synonym_standardization import SynonymStandardizationLayer
from saytex.layers.from_to_recognition import FromToRecognitionLayer
from saytex.layers.divided_by_recognition import DividedByRecognitionLayer
from saytex.layers.case_insensitivity import CaseInsensitivityLayer

layer_id_to_class = {
    "speech_recognition_error_correction": SpeechRecognitionErrorCorrectionLayer,
    "case_insensitivity": CaseInsensitivityLayer,
    "capitalization": CapitalizationLayer,
    "spoken_number_recognition": SpokenNumberRecognitionLayer,
    "synonym_standardization": SynonymStandardizationLayer,
    "from_to_recognition": FromToRecognitionLayer,
    "divided_by_recognition": DividedByRecognitionLayer,
    "auto_completion_to_avoid_compile_errors": None,
    "prettification": None
}
"""
The layer_id_to_class dictionary contains a mapping from a string identifying
a layer to the class implementing the layer. The string is used in config.py.
"""