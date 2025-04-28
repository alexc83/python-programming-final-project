# CPSC 4970 - Python Programming
#
# Assignment 6 - Final Project
#
# Author: Alan Cruce
# Date: April 28, 2025

from module06.league_model.identified_object import IdentifiedObject


class TeamMember(IdentifiedObject):
    """
    Class for the TeamMember object
    """

    def __init__(self, oid, name, email):
        """
        Constructor for the TeamMember object.

        :param oid: id for the team member
        :param name: name of the team member
        :param email: email address for the team member
        """
        super().__init__(oid)
        self._name = name
        self._email = email

    @property
    def name(self):
        """
        Getter method for the team member name.

        :return: Team member name
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Setter method for the team member name

        :param value: name to set for the team member
        :return: none
        """
        self._name = value

    @property
    def email(self):
        """
        Getter for the email of the team member
        :return: email of the team member
        """
        return self._email

    @email.setter
    def email(self, value):
        """
        Setter for the email of the team member
        :param value: value of the email for the team member
        :return: none
        """
        self._email = value

    def send_email(self, emailer, subject, message):
        """
        Method to send email to the team member

        :param emailer: emailer object
        :param subject: subject of the email
        :param message: message of the email
        :return: none
        """
        emailer.send_plain_email([self._email], subject, message)

    def __str__(self):
        """
        Returns a string value of the object.

        :return: string value of the object
        """
        return f"{self._name}<{self._email}>"