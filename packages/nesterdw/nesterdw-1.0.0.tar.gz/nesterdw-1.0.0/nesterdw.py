"""This is the nester.py module which contains a function called print_lol() dedicated at printing lists
including splitting sub-lists down to elements"""

def print_lol(the_list):
    """print_lol() printing elements of the lists,
    splitting sub-lists down to elements"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
