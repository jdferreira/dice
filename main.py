#!/usr/bin/env python3

"""
For all possible pairs of non-standard dice, calculate which has a higher chance
of winning.

A non-standard die is a die where all the sides have one number from 0 to 6,
but it is not necessary that all sides are different. Examples of non-standard
dice are given by the following lists, where each element is the value of one
side:

    - [4, 4, 4, 4, 0, 0]
    - [3, 3, 3, 3, 3, 3]
    - [6, 6, 2, 2, 2, 2]

As the order is not important, we represent each die as the descending values of
its sides.
"""

import sys

from collections import defaultdict

# Default values

MIN_VALUE = 0
MAX_VALUE = 4
SIDES = 4

def die_generator(*, min_value=MIN_VALUE, max_value=MAX_VALUE, sides=SIDES):
    """
    This returns a generator that generates all the possible dice, given the
    minimum and maximum values of the sides, as well as the number of sides.
    """
    
    # Technical note: we do this by fixing the first side as a number
    # between min_value and max_value and then generate (n - 1) sides where the
    # maximum value is the value on this side
    
    # We iterate over all possible values on the first side
    
    for first_side in range(min_value, max_value + 1):
        if sides == 1:
            yield (first_side,)
        else:
            gen = die_generator(min_value=0, max_value=first_side, sides=sides - 1)
            yield from ((first_side,) + die for die in gen)

def is_best(this, oponent):
    """
    Determine which of the two given dive has a higher probability of rolling
    a higher value than the other die.
    """
    
    # For each side in this die, count the number of sides in oponent that have
    # a higher value. Take into account that there can be ties.
    
    total = len(this) * len(oponent)
    count = 0
    ties = 0
    for side1 in this:
        count += sum(1 for side2 in oponent if side1 > side2)
        ties += sum(1 for side2 in oponent if side1 == side2)
    
    # This die wins `count` times, and the oponent wins `total - ties - count`
    # times.
    
    return count > total - ties - count

def clean(graph):
    """
    Remove from the graph the dice that only win or only loose. Keep doing it
    until no change occurs.
    """
    
    # Graph is a dictionary of the form
    # { die: (win_against, lose_against )}
    # where win_against and lose_against are lists of dice
    
    while True:
        # Get the dice that only win (or only tie). This is the list of dice for
        # which one of the two lists is empty
        to_delete = [die for die, (w, l) in graph.items() if len(w) == 0 or len(l) == 0]
        
        # If nothing else can be removed, stop the cleaning process
        if len(to_delete) == 0:
            break
        
        # Remove these dice from the graph, taking care to delete them from
        # the win and lose lists as well
        for die in to_delete:
            del graph[die]
        
        for (w, l) in graph.values():
            for die in to_delete:
                if die in w:
                    w.remove(die)
                if die in l:
                    l.remove(die)

def main():
    # Generate all pairs of dice
    # For each pair, determine which is the best one
    
    # Create a data structure to hold on to this information. We do this in a
    # dictionary that associates with each die two lists: one containing the
    # dice against which this wins, and another containing the dice against
    # which this loses.
    
    graph = defaultdict(lambda: ([], []))
    
    for this in die_generator():
        for oponent in die_generator():
            
            # If this is the best die of the two, print the relationship on the
            # output.
            if is_best(this, oponent):
                graph[this][0].append(oponent)
                graph[oponent][1].append(this)
    
    # Remove all "uninteresting" information from the graph
    clean(graph)
    
    for this in sorted(graph):
        w, l = graph[this]
        
        this_name = "".join(map(str, this))
        
        for oponent in sorted(w):
            oponent_name = "".join(map(str, oponent))
            print("{} > {}".format(this_name, oponent_name))


if __name__ == '__main__':
    main()
