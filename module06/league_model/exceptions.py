# CPSC 4970 - Python Programming
#
# Assignment 6 - Final Project
#
# Author: Alan Cruce
# Date: April 28, 2025

class DuplicateOid(Exception):
    """
    This exception class is raised when a new object
    is attempted to be added to the league system
    (i.e. a team member or competition) with a duplicate
    oid of an object already part of the league system.
    """

    def __init__(self, oid):
        super().__init__("Error: duplicate oid found")
        self.oid = oid

class DuplicateEmail(Exception):
    """
    This exception class is raised when a new team member
    is attempted to be added to a team with the same email
    address of a team member already part of the team.
    """

    def __init__(self, email):
        super().__init__("Error: duplicate email found")
        self.email = email