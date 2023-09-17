"""
This lecture covered over how everything in Python is an object, classes, and sub-classes

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
"""
print("--- Welcome to Lecture 6's example/follow-along code ---")
print("--- Check the code for some of the printed stuff below to make sense ---\n")

# First, a namespace is just the name python assigns to an object
a = 5           # a is a namespace that maps to an internal object

# EVERYTHING in Python is an object
# Each object has attributes: functions or variables pertaining to the object
# An attribute can be accessed with a dot: object.attribute

a.to_bytes()            # For example, the interger we previously declared is an object with
                        # a `to_bytes()` attribute
"123a".endswith("a")    # Same with strings

# We can defined out own object as classes!
# So let's make a basic class
class BeginnerClass:    # This is how you define a class
    # Everything here are attributes of the class

    # The following are class variables (shared between all class instances)
    a_list = []
    c_id = 5

    # Every function in the class is automatically given a self argument that refers to the object
    def get_id(self):
        return self.c_id

    def print_happy(self):
        print("I am happy!")

    def add_numbers(self, a, b):
        return a + b

    # The following is a special function that Python calls when an instance of the class is created
    # The init can have input argument, which will be passed when we create an instance of this class
    def __init__(self, name):
        # The following are instance variables: their scope is only in the class
        self.name = name
        self.b_list = []
        self._secret = "hi"     # Variables starting with an _ are considered protected
        print(f"Init of BeginnerClass for name {name}")

# Now we make an instance of the class
b1 = BeginnerClass("B1")

# We can get some of the class's attributes
print("b1.c_id(): ", b1.c_id)

# We technically can also access protected variables, nothing will stop us
# Generally not good practice to do so
print("b1._secret: ", b1._secret)

# We can call functions of the class
print("b1.get_id(): ", b1.get_id())

# Be careful when having class variables (vs instance variables), as they are shared between ALL classes
b2 = BeginnerClass("B2")
b1.a_list.append("B1-List")
print("b1.a_list: ", b1.a_list)        # expected behaviors
print("b2.a_list: ", b2.a_list)        # Somehow b2 has the same value as b1's a_list

# This is why it's recommended to have class variables only have constants, and everything else
#   should be an instance variable
b1.b_list.append("B1-List")
print("b1.b_list: ", b1.b_list)        # expected behaviors
print("b2.b_list: ", b2.b_list)        # An instance variable is not shared between classes

# We can make sub-classes: They are classes which inherit all attributes of the parent class unless
#   otherwise overriden
class AdvancedClass(BeginnerClass):
    # The following method is re-defined, so calls to this function in this class will execute the code
    #   below, not in the parent class
    def print_happy(self):
        print("I am happy-er")

    def add_numbers(self, a, b):
        # We can use super() to call functions from the parent class that were de-defined in this
        #   subclass
        # In this case, we use it to execute the parent class'es add_numbers, then we do something to it
        r = super().add_numbers(a, b)
        print(f"Return: {r:d}")
        return r

# We still need to pass something, as the __init__ function was not re-defined
b3 = AdvancedClass("B3")
# The advanced class inherits all attributes of the parent class
print("b3.get_id(): ", b3.get_id())
print("b3.name: ", b3.name)
# We can call re-defined functions
b3.print_happy()
b3.add_numbers(5, 5)

print("\n--- end ---")
# end
