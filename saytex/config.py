"""
This configuration file contains the default layers as well as the default
layer priorities. Changing it will change the default for all Saytex
instances. To change the layers for a specific Saytex instance, look into
the documentation on add_layer and remove_layer of Saytex.
"""

from saytex.layers.speech_recognition_error_correction import SpeechRecognitionErrorCorrectionLayer
from saytex.layers.case_insensitivity import CaseInsensitivityLayer
from saytex.layers.capitalization import CapitalizationLayer
from saytex.layers.spoken_number_recognition import SpokenNumberRecognitionLayer
from saytex.layers.synonym_standardization import SynonymStandardizationLayer
from saytex.layers.handle_of import HandleOfLayer
from saytex.layers.from_to_recognition import FromToRecognitionLayer
from saytex.layers.divided_by_recognition import DividedByRecognitionLayer
from saytex.layers.prettification import PrettificationLayer


default_layers = {
    SpeechRecognitionErrorCorrectionLayer,
    CaseInsensitivityLayer,
    CapitalizationLayer,
    SpokenNumberRecognitionLayer,
    SynonymStandardizationLayer,
    HandleOfLayer,
    FromToRecognitionLayer,
    DividedByRecognitionLayer,
    PrettificationLayer
}
"""
The used_layers is a set containing the default layers to be used by Saytex when
converting natural language into SayTeX Syntax. Changing the layers that are
in use will affect what spoken math expressions that SayTeX can recognize.
Each layer must be a subclass of saytex.layers.layer.Layer. Creating new layers is
as simple as creating a new subclass of saytex.layers.layer.Layer, and then adding
it to the default_layers and default_layer_priorities, or just adding it on a
case-by-case situation to a Saytex instance.
"""



default_layer_priorities = {
    SpeechRecognitionErrorCorrectionLayer: 0,
    CaseInsensitivityLayer: 0,
    CapitalizationLayer: 1,
    SpokenNumberRecognitionLayer: 1,
    SynonymStandardizationLayer: 1,
    HandleOfLayer: 2, # depends on synonym standardization
    FromToRecognitionLayer: 3, # this is debatable, but it kind of depends on the capitalization layer
    DividedByRecognitionLayer: 3, # depends on the handle-of layer
    PrettificationLayer: 4 # should always be done last
}
"""
The layer_priorities is a dictionary mapping layer classes to a number, reflecting
the in which order the layers should be executed. Layers are executed from low
to high priority. Layers with the same priority can be executed in any order; the
idea is that such layers are independent of each other. In designing new layers,
one should strive for not adding a new priority level.
"""