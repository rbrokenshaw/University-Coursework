#Student Number: C1772582

#! /usr/bin/python3
import re


##CMT115 COURSEWORK 2018/19 ###
###############################
##You need to implet the following methods:
##
##Question 1
##anagram_validator()  [15 marks]
##
##Question 2
##credit_card_validator()  [15 marks]

################################

###################################################
# Question 1: Check for anagrams:#
###################################################
def read_anagram(file_name):
    '''
    Input: a file name
    Return: a nested list of two words list
    Example : [[word1,word2],[word3,word4]...etc]
    '''
    anagramList = []

    #Read text file line by line, remove whitespace and newlines, check there are two words to compare and put the two words into a nested list
    with open(file_name, "r") as text_file: 
        for line in text_file:

            lineTidy = line.strip()
            lineTidy = line.replace ("\n", "")
            lineSplit = lineTidy.split(",")
            if len(lineSplit) == 2:
                anagramList.append(lineSplit)
                
        return anagramList

    
def anagram_validator(anagram):
    '''
    Input is the output from "read_anagram()".
    Return: list of "anagrams" or "Not anagrams" values for each two words
    example input (dog,gdo),(try,elm) then output would be ["anagrams","Not anagrams"] with sequence of the input
    '''

    anagramResult = []

    for pair in anagram:
        try:
            #If length of second word doesn't match the first word, it isn't an anagram.
            if len(pair[0]) != len(pair[1]): 
                anagramResult.append("Not anagrams")

            else:
                #The length of the first word will be needed to check against count of same letters found in second word.
                wordLength = len(pair[0]) 
                letterCount = 0

                #for each letter in first word that is also in the second word, add 1 to the letter count.
                for letter in pair[0].lower(): 
                    if letter in pair[1].lower():
                        letterCount += 1

                #If the final letter count matches the length of the first word, it is an anagram.
                if letterCount == wordLength: 
                    anagramResult.append("Anagrams")

                else:
                    anagramResult.append("Not anagrams")
        except IndexError: 
            pass

    return anagramResult

    
############################################
# Question 2: Validate credit cards         #
############################################
def read_credit_cards(file_name):
    '''
    Input: a file name
    Return tuple of numbers
    '''

    with open(file_name, "r") as text_file:
        whole_thing = text_file.read()
        numbersTidy = whole_thing.strip()
        numbersTidy = numbersTidy.replace ("[", "")
        numbersTidy = numbersTidy.replace ("]", "")
        numberList = numbersTidy.split(",")

        numberTuple = (tuple(numberList))

        return numberTuple


def credit_card_validator(numbers):
    '''
    Input: tuple of numbers
    Return:
        dictionary of credit card numbers where key is the number and value if valid or invalid
    '''
    cardDict = {}

    for n in numbers:        
        cardDict[n.strip()] = ""

    for key in cardDict.keys():
        keyNoDashes = key.replace( "-" , "" )

        #Check if all integers and correct length
        if keyNoDashes.isdigit() and len(keyNoDashes) == 16:
            cardDict.update({key : "Valid"})

            #Check if starts with 4, 5 or 6:
            if int(key[0]) > 3 and int(key[0]) < 7:
                cardDict.update({key : "Valid"})

                #Check for 4 consecutive numbers
                numStr = keyNoDashes
                for i in range(len(numStr)):
                    try:
                        if numStr[i] == numStr[i+1]:
                            if numStr[i+1] == numStr[i+2]:
                                if numStr[i+2] == numStr[i+3]:
                                    cardDict.update({key : "Invalid"})

                    except IndexError:
                        pass

                    #Check for groups of 4
                    if "-" in key:
                        for group in key.split("-"):
                            if len(group) != 4:
                                cardDict.update({key : "Invalid"})


            else:
                cardDict.update({key : "Invalid"})

        else:
            cardDict.update({key : "Invalid"})

    return cardDict


def print_credit_card_summary(dict_o):
    '''
    Input: dict
    Return:
        printing summary of validation result - space between credit card and status is 40 width
        example:
        378282246310005     Invalid
        30569309025904      Invalid
    '''
    for item in dict_o.items():
        print ("{:>40}{:>}".format(item[0],item[1]))


####### THE CODE BELOW IS FOR TESTING###################
############### DO NOT  CHANGE #########################


import sys

if __name__ == '__main__':
    # Take care of the console inputs
    if len(sys.argv) <= 1:
        sys.argv = ['', "anagram.txt", "credit_cards.txt"]
    stars = '*' * 40
    print(stars)
    print("Testing Question 1 --- Anagrams?")
    print(stars)

    # testing reading_anagrams
    try:
        anagram = read_anagram(sys.argv[1])
        if not anagram:
            print("read_anagram() returns None.")
        else:
            print("anagram: ", anagram)
            print()
    except Exception as e:
        print("Error (readnumbers()): ", e)

    # testing anagram_validator
    Anagrams = 0
    NAnagrams = 0
    try:
        if not anagram:  # Question 1 has not been implemented
            print("anagram_validator() skipped....")
        else:
            result = anagram_validator(anagram)
            if result == None:
                print("anagram_validator() returns None.")
            else:
                for i in result:
                    if i == "Anagrams":
                        Anagrams += 1
                    elif i == "Not anagrams":
                        NAnagrams += 1
                print("Number of valid Anagrams is {} and Not anagrams is {}.".format(Anagrams, NAnagrams))

    except Exception as e:
        print("Error (anagram_validator()):", e)

    # testing  Question 2
    print("\n\n" + stars)
    print("Testing Question 2 --- Credit Card Validator")
    print(stars)

    # Testing reading_credit_cards
    try:
        tup = read_credit_cards(sys.argv[2])
        if not tup:
            print("read_credit_cards() returns None.")
        else:
            print("The tuple of credit_cards: {}".format(tup))
    except Exception as e:
        print("Error (read_credit_cards()):", e)

    # Testing credit_card_validator
    vcc = 0
    ivcc = 0
    try:
        if not tup:  # Readin_Question 2 has not been implemented
            print("credit_card_validator() skipped...")
        else:
            cc_dict = credit_card_validator(tup)
            tmp_cc_dict = cc_dict
            if not cc_dict:
                print("credit_card_validator()  returns None.")
            else:
                for items in cc_dict.keys():
                    if cc_dict[items] == "Valid":
                        vcc += 1
                    elif cc_dict[items] == "Invalid":
                        ivcc += 1
                print("Number of valid credit cards is {} and invalid {}.".format(vcc, ivcc))
    except Exception as e:
        print("Error (credit_card_validator()):", e)

    # testing  Question 2
    print("\n\n" + stars)
    print("Testing Question 2b --- Print Credit Card Summary")
    print(stars)
    # Testing print_credit_card_summary
    try:
        if not tmp_cc_dict:  # Dict credit card output has not been implemented
            print("print_credit_card_summary() skipped...")
        else:
            import io  # do not delete this line
            from contextlib import redirect_stdout  # do not delete this line

            f = io.StringIO()
            with redirect_stdout(f):
                print_credit_card_summary(tmp_cc_dict)
                out = f.getvalue()
            if not out:
                print("print_credit_card_summary()  returns None.")
            else:
                count44 = 0
                count46 = 0
                for line in out.splitlines():
                    if len(line) - len(line.split()) == 44:
                        count44 += 1
                    elif len(line) - len(line.split()) == 46:
                        count46 += 1
                if count44 == vcc and count46 == ivcc:
                    print("Your format looks good")
                else:
                    print("You might have some issues in your summary format")

    except Exception as e:
        print("Error (print_credit_card_summary()):", e)


