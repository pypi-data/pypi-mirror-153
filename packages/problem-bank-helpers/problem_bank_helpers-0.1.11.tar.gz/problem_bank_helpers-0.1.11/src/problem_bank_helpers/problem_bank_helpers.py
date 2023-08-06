# Author: Firas Moosvi, Jake Bobowski, others
# Date: 2021-06-13

from collections import defaultdict
import numpy as np
import sigfig
import pandas as pd
import os

## Load data and dictionaries
#global names,jumpers,vehicles,manual_vehicles,metals,T_c
names = pd.read_csv("https://raw.githubusercontent.com/open-resources/problem_bank_helpers/main/data/names.csv")["Names"].tolist()
jumpers = pd.read_csv("https://raw.githubusercontent.com/open-resources/problem_bank_helpers/main/data/jumpers.csv")["Jumpers"].tolist()
vehicles = pd.read_csv("https://raw.githubusercontent.com/open-resources/problem_bank_helpers/main/data/vehicles.csv")["Vehicles"].tolist()
manual_vehicles = pd.read_csv("https://raw.githubusercontent.com/open-resources/problem_bank_helpers/main/data/manual_vehicles.csv")["Manual Vehicles"].tolist()
metals = pd.read_csv("https://raw.githubusercontent.com/open-resources/problem_bank_helpers/main/data/metals.csv")["Metal"].tolist()
T_c = pd.read_csv("https://raw.githubusercontent.com/open-resources/problem_bank_helpers/main/data/metals.csv")["Temp Coefficient"].tolist()
## End Load data

def create_data2():

    nested_dict = lambda: defaultdict(nested_dict)
    return nested_dict()

def sigfigs(x):
    '''Returns the number of significant digits in a number. This takes into account
       strings formatted in 1.23e+3 format and even strings such as 123.450'''
    # if x is negative, remove the negative sign from the string.
    if float(x) < 0:
        x = x[1:]
    # change all the 'E' to 'e'
    x = x.lower()
    if ('e' in x):
        # return the length of the numbers before the 'e'
        myStr = x.split('e')
        return len( myStr[0] ) - 1 # to compenstate for the decimal point
    else:
        # put it in e format and return the result of that
        ### NOTE: because of the 8 below, it may do crazy things when it parses 9 sigfigs
        n = ('%.*e' %(8, float(x))).split('e')
        # remove and count the number of removed user added zeroes. (these are sig figs)
        if '.' in x:
            s = x.replace('.', '')
            #number of zeroes to add back in
            l = len(s) - len(s.rstrip('0'))
            #strip off the python added zeroes and add back in the ones the user added
            n[0] = n[0].rstrip('0') + ''.join(['0' for num in range(l)])
        else:
            #the user had no trailing zeroes so just strip them all
            n[0] = n[0].rstrip('0')
        #pass it back to the beginning to be parsed
    return sigfigs('e'.join(n))
    
    
# A function to rounding a number x keeping sig significant figures. 
def round_sig(x, sig):
    from math import log10, floor
    if x == 0:
        y = 0
    else:
        y = sig - int(floor(log10(abs(x)))) - 1
    return round(x, y)

# def round_sig(x, sig_figs = 3):
#     """A function that rounds to specific significant digits. Original from SO: https://stackoverflow.com/a/3413529/2217577; adapted by Jake Bobowski

#     Args:
#         x (float): Number to round to sig figs
#         sig_figs (int): Number of significant figures to round to; default is 3 (if unspecified)

#     Returns:
#         float: Rounded number to specified significant figures.
#     """
#     return round(x, sig_figs-int(np.floor(np.log10(np.abs(x))))-1)

# If the absolute value of the submitted answers are greater than 1e4 or less than 1e-3, write the submitted answers using scientific notation.
# Write the alternative format only if the submitted answers are not already expressed in scientific notation.
# Attempt to keep the same number of sig figs that were submitted.    
def sigFigCheck(subVariable, LaTeXstr, unitString):    
    if subVariable is not None:
        if (abs(subVariable) < 1e12 and abs(subVariable) > 1e4) or (abs(subVariable) < 1e-3 and abs(subVariable) > 1e-4):
            decStr = "{:." + str(sigfigs(str(subVariable)) - 1) + "e}"
            return("In scientific notation, $" + LaTeXstr + " =$ " + decStr.format(subVariable) + unitString + " was submitted.")
        else:
            return None
            
            
# An error-checking function disigned to give hints if the submitted answer is:
# (1) correct except for and overall sign or...
# (2) the answer is right expect for the power of 10 multiplier or...
# (3) answer has both a sign and exponent error.            
def ErrorCheck(errorCheck, subVariable, Variable, LaTeXstr, tolerance):
    import math, copy
    from math import log10, floor
    if errorCheck == 'true' or errorCheck == 'True' or errorCheck == 't' or errorCheck == 'T':
        if subVariable is not None and subVariable != 0 and Variable != 0:
            if math.copysign(1, subVariable) != math.copysign(1, Variable) and abs((abs(subVariable) - abs(Variable))/abs(Variable)) <= tolerance:
                return("Check the sign of $" + LaTeXstr + "$.")
            elif math.copysign(1, subVariable) == math.copysign(1, Variable) and \
                    (abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable)/10**floor(log10(abs(Variable))))/(abs(Variable)/10**floor(log10(abs(Variable))))) <= tolerance or \
                    abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable/10)/10**floor(log10(abs(Variable))))/(abs(Variable/10)/10**floor(log10(abs(Variable))))) <= tolerance or \
                    abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable*10)/10**floor(log10(abs(Variable))))/(abs(Variable*10)/10**floor(log10(abs(Variable))))) <= tolerance) and \
                    abs((abs(subVariable) - abs(Variable))/abs(Variable)) > tolerance:
                return("Check the exponent of $" + LaTeXstr + "$.")
            elif math.copysign(1, subVariable) != math.copysign(1, Variable) and \
                    (abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable)/10**floor(log10(abs(Variable))))/(abs(Variable)/10**floor(log10(abs(Variable))))) <= tolerance or \
                    abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable/10)/10**floor(log10(abs(Variable))))/(abs(Variable/10)/10**floor(log10(abs(Variable))))) <= tolerance or \
                    abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable*10)/10**floor(log10(abs(Variable))))/(abs(Variable*10)/10**floor(log10(abs(Variable))))) <= tolerance) and \
                    abs((abs(subVariable) - abs(Variable))/abs(Variable)) > tolerance:
                return("Check the sign and exponent of $" + LaTeXstr + "$.")
            else:
                return None
        else:
            return None
    else:
        return None

# def attribution(TorF, source = 'original', vol = 0, chapter = 0):
#     if TorF == 'true' or TorF == 'True' or TorF == 't' or TorF == 'T':
#         if source == 'OSUP':
#             return('<hr></hr><p><font size="-1">From chapter ' + str(chapter) + ' of <a href="https://openstax.org/books/university-physics-volume-' + str(vol) + \
#                     '/pages/' + str(chapter) + '-introduction" target="_blank">OpenStax University Physics volume ' + str(vol) + \
#                     '</a> licensed under <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank">CC BY 4.0</a>.</font><br> <font size="-1">Download for free at <a href="https://openstax.org/details/books/university-physics-volume-' + str(vol) + \
#                     '" target="_blank">https://openstax.org/details/books/university-physics-volume-' + str(vol) + \
#                     '</a>.</font><br> <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank"><pl-figure file-name="by.png" directory="clientFilesCourse" width="100px" inline="true"></pl-figure></a></p>')
#         elif source == 'original':
#             return('<hr></hr><p><font size="-1">Licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank">CC BY-NC-SA 4.0</a>.</font><br><a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank"><pl-figure file-name="byncsa.png" directory="clientFilesCourse" width="100px" inline="true"></pl-figure></a></p>')
#         else:
#             return None
#     else:
#         return None

def roundp(*args,**kwargs):
    """ Wrapper function for the sigfig.round package. Also deals with case if requested sig figs is more than provided.

    Args:
        num (number): Number to round or format.

    Returns:
        float/str: Rounded number output to correct significant figures.
    """
    a = [item for item in args]
    kw = {item:v for item,v in kwargs.items() if item in ['sigfigs', 'decimals']}
        
    num_str = str(float(a[0]))
        
    # Add trailing zeroes if needed
    
    if kw.get('sigfigs',None):
        z = kw['sigfigs']
    elif kw.get('decimals', None):
        z = kw['decimals']
    else:
        z = 3 # Default sig figs
                        
    num_str = num_str + str(0)*z*2
                
    result = sigfig.round(num_str,**kwargs)
        
    # Switch back to the original format if it was a float
    if isinstance(a[0],float):
        return float(result) # Note, sig figs will not be carried through if this is a float
    elif isinstance(a[0],str):
        return result
    elif isinstance(a[0],int):
        return int(float(result))
    else:
        return sigfig.round(*args,**kwargs)

def round_str(*args,**kwargs):
    
    if type(args[0]) is str:
        return args[0]
    
    if 'sigfigs' not in kwargs.keys():
        kwargs['sigfigs'] = 2
    
    if 'format' not in kwargs.keys():
        if np.abs(args[0]) < 1:
            return roundp(*args,**kwargs,format='std')
        elif np.abs(args[0]) < 1E6:
            return roundp(*args,**kwargs,format='English')
        else:
            return roundp(*args,**kwargs,format='sci')
    else:
        return roundp(*args,**kwargs)

def num_as_str(num, digits_after_decimal = 2):
    """Rounds numbers properly to specified digits after decimal place

    Args:
        num (float): Number that is to be rounded
        digits_after_decimal (int, optional): Number of digits to round to. Defaults to 2.

    Returns:
        str: A string that is correctly rounded (you know why it's not a float!)
    """
    """
    This needs to be heavily tested!!
    WARNING: This does not do sig figs yet!
    """

    # Solution attributed to: https://stackoverflow.com/a/53329223

    if type(num) == str:
        return num
    elif type(num) == dict:
        return num
    else:
        from decimal import Decimal, getcontext, ROUND_HALF_UP

        round_context = getcontext()
        round_context.rounding = ROUND_HALF_UP

        tmp = Decimal(num).quantize(Decimal('1.'+'0'*digits_after_decimal))

        return str(tmp)

def sign_str(number):
    """Returns the sign of the input number as a string.

    Args:
        sign (number): A number, float, etc...

    Returns:
        str: Either '+' or '-'
    """
    if (number < 0):
        return " - "
    else:
        return " + "

################################################
#
# Feedback and Hint Section
#
################################################

def automatic_feedback(data,string_rep = None,rtol = None):

    # In grade(date), put: data = automatic_feedback(data)

    if string_rep is None:
        string_rep = data['correct_answers'].keys()
    if rtol is None:
        rtol = 0.03

    for i,ans in enumerate(data['correct_answers'].keys()):
        data["feedback"][ans] = ErrorCheck(data['submitted_answers'][ans],
                                           data['correct_answers'][ans],
                                           string_rep[i],
                                           rtol)

    return data


# An error-checking function designed to give hints if the submitted answer is:
# (1) correct except for and overall sign or...
# (2) the answer is right expect for the power of 10 multiplier or...
# (3) answer has both a sign and exponent error.            
def ErrorCheck(subVariable, Variable, LaTeXstr, tolerance):
    import math
    from math import log10, floor
    
    if subVariable is not None and subVariable != 0 and Variable != 0:
        if math.copysign(1, subVariable) != math.copysign(1, Variable) and abs((abs(subVariable) - abs(Variable))/abs(Variable)) <= tolerance:
            return("Check the sign of $" + LaTeXstr + "$.")
        elif math.copysign(1, subVariable) == math.copysign(1, Variable) and \
                (abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable)/10**floor(log10(abs(Variable))))/(abs(Variable)/10**floor(log10(abs(Variable))))) <= tolerance or \
                abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable/10)/10**floor(log10(abs(Variable))))/(abs(Variable/10)/10**floor(log10(abs(Variable))))) <= tolerance or \
                abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable*10)/10**floor(log10(abs(Variable))))/(abs(Variable*10)/10**floor(log10(abs(Variable))))) <= tolerance) and \
                abs((abs(subVariable) - abs(Variable))/abs(Variable)) > tolerance:
            return("Check the exponent of $" + LaTeXstr + "$.")
        elif math.copysign(1, subVariable) != math.copysign(1, Variable) and \
                (abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable)/10**floor(log10(abs(Variable))))/(abs(Variable)/10**floor(log10(abs(Variable))))) <= tolerance or \
                abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable/10)/10**floor(log10(abs(Variable))))/(abs(Variable/10)/10**floor(log10(abs(Variable))))) <= tolerance or \
                abs((abs(subVariable)/10**floor(log10(abs(subVariable))) - abs(Variable*10)/10**floor(log10(abs(Variable))))/(abs(Variable*10)/10**floor(log10(abs(Variable))))) <= tolerance) and \
                abs((abs(subVariable) - abs(Variable))/abs(Variable)) > tolerance:
            return("Check the sign and exponent of $" + LaTeXstr + "$.")
        elif math.copysign(1, subVariable) == math.copysign(1, Variable) and abs((abs(subVariable) - abs(Variable))/abs(Variable)) <= tolerance:
            return("Nice work, $" + LaTeXstr + "$ is correct!")
        else:
            return None
    else:
        return None