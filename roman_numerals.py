#!/usr/bin/python3.6

import argparse
import sys

class RomanNumeralConverter:
    conversionList = [(1, 'I'), (5, 'V'), (10, 'X'), (50, 'L'), (100, 'C')]
    mapp = dict(conversionList)
    mapp.update({v:k for k,v in mapp.items()})
    min_value = 1
    max_value = 4 * conversionList[-1][0] - 1

    def __init__(self):
        pass

    @staticmethod
    def toRoman(num, display = False):
        """
        Given an int `num` and a bool `display`, this method attempts to
        convert the int into the corresponding roman numeral. If display is
        True, that conversion will be printed to the console.

        Returns
        -------
        str roman numeral representation of the given integer.

        Exception
        ---------
        ValueError if the given int is outside of the acceptable range.
        """
        if num < RomanNumeralConverter.min_value:
            raise ValueError('Cannot convert values less than {:.0f}'.format(
                RomanNumeralConverter.min_value
            ))
        if num > RomanNumeralConverter.max_value:
            raise ValueError('Cannot convert values greater than {:.0f}'.format(
                RomanNumeralConverter.max_value
            ))

        x = num
        roman = ''
        for idx in range(len(RomanNumeralConverter.conversionList) - 1, -1, -1):
            val, char = RomanNumeralConverter.conversionList[idx]
            multiple = x//val
            x -= multiple * val
            # Handling 4's (i.e. 4, 40, 24, etc.)
            if multiple == 4:
                roman += char + RomanNumeralConverter.conversionList[idx + 1][1]
            elif multiple:
                roman += char * multiple
            # Handling 9's (i.e. 9, 90, 29, etc.)
            if val%10 == 0 and x >= val - val//10:
                x -= val - val//10
                roman += RomanNumeralConverter.conversionList[idx - 2][1] + char

        if display:
            RomanNumeralConverter.displayConversion(num, roman)

        return roman

    @staticmethod
    def toNum(roman, display = False):
        """
        Given a str `roman` and a bool `display`, this method assumes the str
        to be a roman numeral and attempts to convert to the corresponding
        int. If display is True, that conversion will be printed to the
        console.

        Returns
        -------
        int respresentation of the given roman numeral.

        Exception
        ---------
        ValueError if the given string is not a valid roman numeral.
        """
        num = 0
        prevVal = 0
        error = -1
        for char in roman:
            val = RomanNumeralConverter.mapp.get(char, error)
            if val == error:
                # Note that there may be some characters that are in fact
                # roman numeral characters but just not included in this
                # converter (i.e. D = 500)
                raise ValueError(('"{}" in "{}" is not a valid roman numeral'
                    ' character!').format(char, roman))

            # Now here you may want a check for an invalid prevVal
            # For instance, VC is nonsense. Instead the correct representation
            # for 95 is XCV TODO
            if prevVal and prevVal < val:
                num -= 2 * prevVal

            num += val
            prevVal = val

        if display:
            RomanNumeralConverter.displayConversion(num, roman)

        return num

    @staticmethod
    def displayConversion(num, roman):
        """
        Given an int `num` and a str `roman`, this method prints their values.
        i.e. num=32, roman='XXXII'
             prints: ' 32: XXXII'
        
        Returns
        -------
        None
        """
        print(('{:' + str(len(str(RomanNumeralConverter.max_value))) +
            '.0f}: {}').format(num, roman
        ))

if __name__ == '__main__':
    testList = list(range(1, 11)) + [200, RomanNumeralConverter.max_value]
    for num in testList:
        roman = RomanNumeralConverter.toRoman(num, display = True)
        num = RomanNumeralConverter.toNum(roman, display = True)
