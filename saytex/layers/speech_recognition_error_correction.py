"""
Corrects errors in the speech recognition software used.
Currently specific to the Microsoft speech engine, and might not produce
good results if used with other speech recognition software.
"""

from .layer import SaytexLayer

class SpeechRecognitionErrorCorrectionLayer(SaytexLayer):

    common_mischaracterizations = [
        ('see','c'),
        ('hey','a'),
        ('day','a'),
        ('overbyte','over b'),
        ('richer','greater'),
        ('clothes','close'),
        ('whole','close'),
        ('closed','close'),
        ('cosign','cosine'),
        ('quotes','close'),
        ('oakland','open'),
        ('eggs','x'),
        ('clubs','close'),
        ('eclipse','a plus'),
        ('aid','a'),
        ('beat','b'),
        ('nfinity','infinity'),
        ('menace','minus'),
        ('age','h'),
        ('why','y'),
        ('acts','x'),
        ('and','end')
    ]

    common_mischaracterizations_aggressive = [
        ('some','sum'),
        ('be','b'),
        ("I'm",'n'),
        ('sign','sine'),
    ]

    aggressive = True    

    def execute_layer(self, input_string):
        """
        Replaces the mischaracterizations with guesses for what the user actually said.
        Not doing anything smart really, only using word replacements.
        Could easily be modified to be smarter.
        """

        in_progress_string = input_string

        in_progress_string = self.replace_words(self.common_mischaracterizations, in_progress_string)

        if self.aggressive:
            in_progress_string = self.replace_words(self.common_mischaracterizations_aggressive, in_progress_string)
        
        return in_progress_string