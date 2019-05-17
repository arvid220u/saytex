"""
Recognizes spoken numbers and transforms them into number literals.
"""

from .layer import SaytexLayer

import math

class SpokenNumberRecognitionLayer(SaytexLayer):

    def execute_layer(self, input_string):
        """
        Transforms spoken numbers into number literals.
        For example, "five hundred and five" is transformed into "505".
        """

        # easiest way is probably to enumerate all possible numbers, or maybe not
        digits = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        tons = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
        tens = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
        
        class numberpart:
            def __init__(self, s, v, p):
                self.s = s
                self.v = v
                self.p = p
            def __str__(self):
                return self.s
        
        ns = []
        for i, d in enumerate(digits):
            ns.append(numberpart(d, i, 0))
        for i, d in enumerate(tons):
            ns.append(numberpart(d, i+10, 1))
        for i, d in enumerate(tens):
            ns.append(numberpart(d, (i+2)*10, 2))
        ns.append(numberpart('hundred',100,3))
        ns.append(numberpart('thousand',1000,4))
        ns.append(numberpart('million',1000000,5))
        ns.append(numberpart('billion',1000000000,6))
        ns.append(numberpart('trillion',1000000000000,7))

        nsdict = {}
        for npart in ns:
            nsdict[str(npart)] = npart

        
        def numbertype(x):
            if x == 0:
                return 0
            return int(math.log10(x))

        # now iterate through the string linearly!
        innumber = False
        output_string = ""
        curnumber = []
        for word in input_string.split():
            if word == 'and' and innumber:
                continue
            if word in nsdict:
                innumber = True
                b = nsdict[word]
                if len(curnumber) == 0:
                    curnumber.append(b.v)
                else:
                    # if curnumber has exact same value (log 10) as curnumber last one, then terminate this number and start a new one
                    if numbertype(b.v) == numbertype(curnumber[-1]):
                        dnm = 0
                        for x in curnumber:
                            dnm += x
                        output_string += " " + str(dnm)
                        curnumber = [b.v]
                        continue

                    if curnumber[-1] > b.v:
                        curnumber.append(b.v)
                    else:
                        mult = 0
                        while curnumber[-1] < b.v:
                            mult += curnumber[-1]
                            curnumber.pop()
                            if len(curnumber) == 0:
                                break
                        curnumber.append(mult * b.v)
            else:
                if innumber:
                    dnm = 0
                    for x in curnumber:
                        dnm += x
                    output_string += " " + str(dnm)
                    innumber = False
                    curnumber = []

                output_string += " " + word

        if innumber:
            dnm = 0
            for x in curnumber:
                dnm += x
            output_string += " " + str(dnm)
            innumber = False

        # the output string will start with a space, which we don't want
        output_string = output_string.lstrip(" ")

        return output_string