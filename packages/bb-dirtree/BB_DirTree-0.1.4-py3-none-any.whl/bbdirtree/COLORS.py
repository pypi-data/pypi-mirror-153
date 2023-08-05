"""
# ANSI escapes for text manipulation

Import and use these to make your python scripts perdy.
All escape codes are returned in octal format.
A few cursor controls are included but you can find
many more with a few duckduckgo searches.
"""

def C_Bl():
    """ Black """
    return '\x1b[0;30;23m'

def C_Bli():
    """ Black **italic** """
    return '\x1b[0;30;3m'

def C_B():
    """ Blue """
    return '\x1b[0;34;23m'

def C_Bi():
    """ Blue **italic** """
    return '\x1b[0;34;3m'

def C_b():
    """ Light Blue """
    return '\x1b[1;34;23m'

def C_bi():
    """ Light Blue **italic** """
    return '\x1b[1;34;3m'

def C_C():
    """ Cyan """
    return '\x1b[0;36;23m'

def C_Ci():
    """ Cyan **italic** """
    return '\x1b[0;36;3m'

def C_c():
    """ Light Cyan """
    return '\x1b[1;36;23m'

def C_ci():
    """ Light Cyan **italic** """
    return '\x1b[1;36;3m'

def C_O():
    """ Orange """
    return '\x1b[0;33;23m'

def C_Oi():
    """ Orange **italic** """
    return '\x1b[0;33;3m'

def C_P():
    """ Purple """
    return '\x1b[0;35;23m'

def C_Pi():
    """ Purple **italic** """
    return '\x1b[0;35;3m'

def C_p():
    """ Light Purple """
    return '\x1b[1;35;23m'

def C_pi():
    """ Light Purple **italic** """
    return '\x1b[0;35;3m'

def C_r():
    """ Light Red """
    return '\x1b[0;30;23m'

def C_ri():
    """ Light Red **italic** """
    return '\x1b[0;30;23m'

def C_W():
    """ White """
    return '\x1b[1;37;23m'

def C_Wi():
    """ White **italic** """
    return '\x1b[1;37;3m'

def C_Gr():
    """ Dark Gray """
    return '\x1b[1;30;23m'

def C_Gri():
    """ Dark Gray **italic** """
    return '\x1b[1;30;3m'

def C_gr():
    """ Gray """
    return '\x1b[0;37;23m'

def C_gri():
    """ Gray **italic** """
    return '\x1b[0;37;3m'

def C_G():
    """ Green """
    return '\x1b[0;32;23m'

def C_Gi():
    """ Green **italic** """
    return '\x1b[0;32;3m'

def C_g():
    """ Light Green """
    return '\x1b[1;32;23m'

def C_gi():
    """ Light Green **italic** """
    return '\x1b[1;32;3m'

def C_R():
    """ Red """
    return '\x1b[0;31;23m'

def C_Ri():
    """ Red **italic** """
    return '\x1b[0;31;3m'

def C_Y():
    """ Yellow """
    return '\x1b[1;33;23m'

def C_Yi():
    """ Yellow **italic** """
    return '\x1b[1;33;3m'

def F_B():
    """ Bold """
    return '\x1b[1m'

def F__B():
    """ Remove Bold """
    return '\x1b[21m'

def F_I():
    """ Italic """
    return '\x1b[3m'

def F__I():
    """ Remove Italic """
    return '\x1b[23m'

def F_S():
    """ Strikethrough """
    return '\x1b[9m'

def F__S():
    """ Remove Strikethrough """
    return '\x1b[29m'

def F_U():
    """ Underline """
    return '\x1b[4m'

def F__U():
    """ Remove Underline """
    return '\x1b[24m'

def C__():
    """ Reset Text Formatting """
    return '\x1b[0m'

def c_UP(n=1):
    """
     Cursor Up
     n = Number of lines
    """
    return f'\x1b[{n}A'

def c_DOWN(n=1):
    """
     Cursor Down
     n = Number of lines
    """
    return f'\x1b[{n}B'

def c_RIGHT(n=1):
    """
     Cursor Right
     n = Number of columns
    """
    return f'\x1b[{n}C'

def c_LEFT(n=1):
    """
     Cursor Left
     n = Number of columns
    """
    return f'\x1b[{n}D'

def c_COL(n=1):
    """
     Cursor To Column
     n = column number
    """
    return f'\x1b[{n}G'

def c_CLEAR(n=1):
    """
     Clear
     n = 1 - line  -  -  -  -default
     n = 2 - left of cursor
     n = 3 - right of cursor
     n = 4 - screen
    """
    if n == 1:
        return '\x1b[K'
    elif n == 2:
        return '\x1b[1K'
    elif n == 3:
        return '\x1b[0K'
    elif n == 4:
        return '\x1b[2J'

def c_HIDE():
    """ Cursor Invisible """
    return '\x1b[?25l'

def c_SHOW():
    """ Cursor Visible """
    return '\x1b[?25h'
