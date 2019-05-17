"""
Defines the Saytex class, containing methods for converting between
natural language and LaTeX. The conversion is done in a two-step process 
by first translating the input into SayTeX Syntax, after which the 
saytexsyntax module is used for the final LaTeX conversion.
"""

from . import config

from .saytexsyntax import SaytexSyntax

from .layers import SaytexLayer

class UnrecognizableSaytexInput(Exception):
    """
    Raised in to_latex and to_saytex, if the input cannot be transformed 
    into valid SayTeX Syntax.
    """
    pass

class Saytex:
    """
    Contains the method ``to_latex`` to convert from natural
    language to LaTeX. It will do this by invoking the layers
    defined in ``config.py`` in the specified order, followed by a
    final call to SaytexSyntax. The method ``to_saytex`` will do the
    same thing, without the call to SaytexSyntax.
    """

    def __init__(self):
        """
        Initializes a Saytex instance. Specifically, an instance of
        SaytexSyntax will be initialized as well.
        """
        self.saytex_syntax_compiler = SaytexSyntax()

        # add the default layers
        self.layers = set(config.default_layers)
        self.layer_priorities = dict(config.default_layer_priorities)


    def to_latex(self, math_string):
        """
        Converts natural language into LaTeX code.

        :param math_string: A string containing a spoken math expression. The
            string must be recognizable to SayTeX, of which the specifics depend
            on the particular layers that are used. The set of all recognizable
            SayTeX strings is a superset of SayTeX Syntax.

        :return: A string containing a valid translation of the input string
            to LaTeX code. If the string is not recognizable (that is, it
            cannot be converted into SayTeX), the UnrecognizableSaytexInput exception 
            is thrown.
        """
        
        # convert into saytex
        saytex_syntax = self.to_saytex(math_string)

        # saytex syntax to latex
        latex = self.saytex_syntax_compiler.to_latex(saytex_syntax)

        return latex
    
    def to_saytex(self, math_string):
        """
        Converts natural language into SayTeX Syntax.
        
        :param math_string: A string containing a spoken math expression. The
            string should use the SayTeX+ format, which is a superset of
            SayTeX Syntax.

        :return: A string containing a valid translation of the input string
            to SayTeX Syntax. If the string is not recognizable (that is, it
            cannot be converted into SayTeX), the UnrecognizableSaytexInput exception 
            is thrown.
        """

        # the idea is to use a layering approach, where the string goes through
        # a bunch of transformations until finally becoming pure saytex
        
        # in_progress_string contains the string as it is being converted into saytex
        in_progress_string = math_string

        # sort the layers by priority
        # lowest priority comes first (yes, i know, not ideal naming there)
        sorted_layers = sorted(list(self.layers), key = lambda layer_class : self.layer_priorities[layer_class])

        # now apply the layers
        for layer_class in sorted_layers:
            # intialize and execute the layer
            layer = layer_class()
            in_progress_string = layer.execute_layer(in_progress_string)
            #print(in_progress_string)
            #print("and that was after layer: " + str(layer_class))

        # the string that is the result of all layer executions
        saytex_syntax = in_progress_string

        # verify that it does conform to saytex syntax
        if not self.saytex_syntax_compiler.is_valid_saytex_syntax(saytex_syntax):
            raise UnrecognizableSaytexInput("The string '" + math_string + "' was converted into the string '" + saytex_syntax + "', which does not conform to SayTeX Syntax.")

        # return the saytex syntax
        return saytex_syntax
    

    def add_layer(self, layer_class, layer_priority):
        """
        Adds a layer to the natural language -> Saytex Syntax conversion process.

        :param layer_class: The class of the layer, which must be a subclass of
            saytex.layers.layer.Layer. Note that this parameter is not a string, but rather
            the class itself.
        :param layer_priority: The priority of the layer, represented as a number.
            The priority affects in which order the layers are executed, and a lower
            number means it is executed sooner. The priorities only make sense in
            relation to other priorities, and the default priorities can be found in
            saytex.config.
        
        :return: None
        """

        if layer_class in self.layers:
            # this layer is already here!
            raise ValueError("Layer already exists!")
        
        self.layers.add(layer_class)
        self.layer_priorities[layer_class] = layer_priority
    
    def remove_layer(self, layer_class):
        """
        Removes a layer from the conversion process. Can be used to remove
        default layers.

        :param layer_class: The class of the layer, which must be a subclass of
            saytex.layers.layer.Layer. Note that this parameter is not a string, but rather
            the class itself.
        
        :return: None
        """

        if layer_class not in self.layers:
            raise LookupError("Trying to remove layer that does not exist!")
        
        self.layers.remove(layer_class)
        del self.layer_priorities[layer_class]
    
    def get_layers(self):
        """
        Returns the set of currently used layers.

        :return: Set of layers.
        """
        return set(self.layers)
    
    def get_layer_priorities(self):
        """
        Returns a dictionary mapping the currently used layers to their priorities.

        :return: Dictionary of layers to numbers.
        """
        return dict(self.layer_priorities)