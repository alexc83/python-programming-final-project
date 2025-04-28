# CPSC 4970 - Python Programming
#
# Assignment 6 - Final Project
#
# Author: Alan Cruce
# Date: April 28, 2025

# abstract class
from abc import ABC, abstractmethod

class IdentifiedObject(ABC):
    """
    Abtract super class for the League objects:
    League, Team, Team Member, Competition
    """
    def __init__(self, oid):
        """
        Constructor
        :param oid: id of the subclass object
        """
        self._oid = oid

    @property
    def oid(self):
        """
        All subclasses need an id

        :return: oid
        """
        return self._oid

    def __eq__(self, other):
        """
        Equality method where equality is based on oid

        :param other: other object being compared
        :return: True if the objects are the same
        """
        if type(self) is type(other) and self.oid == other.oid:
            return True
        else:
            return False

    def __hash__(self):
        """
        Returns a hash code for the object

        :return: hash code
        """
        return hash(self.oid)
