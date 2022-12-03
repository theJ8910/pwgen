from secrets            import choice
from random             import shuffle
from importlib.metadata import version

VERSION = version( __package__ )

UPPERCASE_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWERCASE_LETTERS = "abcdefghijklmnopqrstuvwxyz"
DIGITS            = "0123456789"
SPECIAL_CHARS     = ",./;'[]\\`<>?:\"{}|~!@#$%^&*()_+"

def generate( length=64, uppercase=True, lowercase=True, digits=True, specialchars=True, spaces=True ):
    """
    Generates a password of the specified length, consisting of the specified characters.
    length determines the length of the password to generate.
        length is expected to be an int >= 1. Defaults to 64.
    uppercase, lowercase, digits, specialchars, and spaces are optional bools that determine what type of characters can appear in the generated password.
        Provide True for a parameter to enable its respective characters (e.g. uppercase=True to allow uppercase characters) to appear, or False to prevent
        those characters from appearing. Note however that at least one of uppercase, lowercase, digits, or specialchars must be True. Also note that if
        spaces is True, spaces will not appear at the beginning or the end of the generated password.
        All of these parameters default to True.
    Returns the generated password as a str.
    """
    #Make sure user provided a valid length for the password
    if length < 1:
        raise RuntimeError( "The password must be at least 1 character long." );

    #Build the character set we'll generate the password from.
    chars = ""
    if uppercase:
        chars += UPPERCASE_LETTERS
    if lowercase:
        chars += LOWERCASE_LETTERS
    if digits:
        chars += DIGITS
    if specialchars:
        chars += SPECIAL_CHARS

    #Make sure our charset has at least one non-space character by this point
    if len( chars ) == 0:
        raise RuntimeError( "At least one of the following types of characters must be enabled: uppercase letters, lowercase letters, digits, or special characters." )

    #If spaces are desired, use two charsets instead of one - one with spaces, one without.
    if spaces:
        charsNoSpaces = list( chars )
        shuffle( charsNoSpaces )
        chars += " "

    #Convert the characters to a list and shuffle it. Probably not necessary, but I like to feel like this adds a little extra randomization to the mix.
    chars = list( chars )
    shuffle( chars )
    
    #We don't want spaces as the first or last character of the password.
    #Take special care to ensure this doesn't happen:
    if spaces:
        if length == 1:
            return choice( charsNoSpaces )
        elif length == 2:
            return choice( charsNoSpaces ) + choice( charsNoSpaces )
        else:
            return choice( charsNoSpaces ) + "".join( choice( chars ) for i in range( length-2 ) ) + choice( charsNoSpaces )
    #If the user doesn't desire spaces, generating the password is a lot simpler:
    else:
        #You can't initialize a string from an iterable, generators included, which seems dumb to me but whatever.
        #So instead, we're using the .join() method here with an empty separator to accomplish this instead.
        return "".join( choice( chars ) for i in range( length ) )
