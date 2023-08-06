# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 22:33:19 2019

@author: lockhart
"""

#------------------------------------------------------------------------------
def int_2_str(integer, amnt_digits, spacer="0"):
    """
    Function to convert and integer value to a string with specifics amount of
    fix digits for example: int_2_str(integer=5, amnt_digits=4, spacer="0")
    will result in returning "0005" string

    Parameters
    ----------
    integer : int
        Integer to be converted to string character.
    amnt_digits : int
        amount of digits in the string.

    Returns
    -------
    string : str
        String with the number correctly formated.
    """
    
    number_str = str(integer)
    len_number = len(number_str)
    
    amnt_spacer = amnt_digits - len_number
    string = ""
    
    for count in range(amnt_spacer):
        string = string + spacer
    
    string = string + number_str
    
    return string

def ustoint(usecond):
    """
    Function to get the integer required to get a time in us in the pulse
    generator.
    """
    
    integer = int((usecond-19.695)/2.6963)
    
    return integer


