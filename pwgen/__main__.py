import sys
from   os  import isatty
from   .   import VERSION, generate

opt_uppercase    = True
opt_lowercase    = True
opt_digits       = True
opt_specialchars = True
opt_spaces       = True
arg_length       = 64

#Quick command-line options reference:
#+---------------------+----+-----+----------+
#| What                | On | Off | Default? |
#+---------------------+----+-----+----------+
#| Uppercase letters   | -u | -U  | On       |
#| Lowercase letters   | -l | -L  | On       |
#| Digits              | -d | -D  | On       |
#| Special characters  | -x | -X  | On       |
#| Spaces              | -s | -S  | On       |
#+---------------------+----+-----+----------+

def main( argv ):
    try:
        #Parse arguments
        argc = len( argv )
        #Options or length specified
        if argc == 2:
            arg1 = argv[1]
            if arg1 == "--help" or arg1 == "-h":
                help()
                return 0
            elif arg1 == "--version":
                print( VERSION )
                return 0
            elif not parseOptions( arg1 ) and not parseLength( arg1 ):
                raise RuntimeError( "Unrecognized argument: \"{}\"".format( arg1 ) )
        #Options AND length specified, in that order
        elif argc == 3:
            arg1 = argv[1]
            arg2 = argv[2]
            if arg1 == "--help" or arg1 == "-h":
                help()
                return 0
            elif not parseOptions( arg1 ):
                raise RuntimeError( "Unrecognized argument: \"{}\"".format( arg1 ) )
            elif not parseLength( arg2 ):
                raise RuntimeError( "Unrecognized argument: \"{}\"".format( arg2 ) )
        #More arguments provided than what is supported
        elif argc > 3:
            raise RuntimeError( "Too many arguments specified." )
        
        print( generate(
            length       = arg_length,
            uppercase    = opt_uppercase,
            lowercase    = opt_lowercase,
            digits       = opt_digits,
            specialchars = opt_specialchars,
            spaces       = opt_spaces
        ) )
        
        return 0
    except RuntimeError as e:
        print( e.args[0], file=sys.stderr )
        if isatty( sys.stdout.fileno() ):
            print()
            help()
        return 1

def help():
    print(
"""Usage:
    python3 -m pwgen [OPTIONS] [length]

Description:
    Generates a random password of the desired length, consisting of lower and uppercase letters, digits, spaces and/or other symbols.
    If length is not specified, it defaults to 64. If specified, length must be a positive integer (length >= 1).
    
    All supported characters are enabled by default. However, you can explicitly enable or disable which types of characters will appear
    in the generated password with the following options. However, please note that at least one non-space character type must be enabled.

Options:
    -u         Enable uppercase characters (default).
    -U         Disable uppercase characters.
    -l         Enable lowercase characters (default).
    -L         Disable lowercase characters.
    -d         Enable digits (default).
    -D         Disable digits.
    -x         Enable special characters (default).
    -X         Disable special characters.
    -s         Enable spaces (default). Spaces will not appear at the start or end of the password.
    -S         Disable spaces.
    --version  Print pwgen version and exit immediately.
    --help     Print this help text and exit immediately."""
    )

def parseOptions( arg ):
    global opt_uppercase, opt_lowercase, opt_digits, opt_specialchars, opt_spaces
    if   arg.startswith( "--" ) and len( arg ) > 2:
        raise RuntimeError( f"Unrecognized long option: \"--{arg[2:]}\"" )
    elif arg.startswith( "-" ) and len( arg ) > 1:
        for char in arg[1:]:
            if char == "u":
                opt_uppercase = True
            elif char == "U":
                opt_uppercase = False
            elif char == "l":
                opt_lowercase = True
            elif char == "L":
                opt_lowercase = False
            elif char == "d":
                opt_digits = True
            elif char == "D":
                opt_digits = False
            elif char == "x":
                opt_specialchars = True
            elif char == "X":
                opt_specialchars = False
            elif char == "s":
                opt_spaces = True
            elif char == "S":
                opt_spaces = False
            else:
                raise RuntimeError( f"Unrecognized short option: \"-{char}\"" )
        return True
    return False

def parseLength( arg ):
    global arg_length
    try:
        arg_length = int( arg )
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    sys.exit( main( sys.argv ) )