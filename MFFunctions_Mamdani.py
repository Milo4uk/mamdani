from BasicFuzzyFunctions import *


def age_is_low(x):
    return SmZ(x, 2, 5)

def age_is_medium(x):
    return SmTrap(x, 2, 4, 6, 8)

def age_is_old(x):
    return SmS(x, 5, 9)



def quality_is_low(x):
    return SmZ(x, 2, 6)

def quality_is_alright(x):
    return SmTrap(x, 3, 7, 8, 10)

def quality_is_fine(x):
    return SmS(x, 7, 13)



def price_is_cheap(x):
    return SmZ(x, 10, 40)

def price_is_average(x):
    return SmTrap(x, 20, 40, 60, 80)

def price_is_expencive(x):
    return SmS(x, 60, 90)
