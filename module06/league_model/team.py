# CPSC 4970 - Python Programming
#
# Assignment 6 - Final Project
#
# Author: Alan Cruce
# Date: April 28, 2025

from module06.league_model.exceptions import DuplicateOid, DuplicateEmail
from module06.league_model.identified_object import IdentifiedObject


class Team(IdentifiedObject):
    """
    The class for the Team object
    """

    def __init__(self, oid, name):
        """
        The constructor for the Team object.

        For module04, sets for oid and email were added
        to help ensure duplicates aren't allowed when
        team members are added.

        :param oid: id for the team object
        :param name: name of the team
        """
        super().__init__(oid)
        self._name = name
        self._members = []
        self._members_oids = set()
        self._members_emails = set()

    @property
    def name(self):
        """
        Getter method for the team name

        :return: team name
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Setter method for the team name.

        :param value: value to set for the team name
        :return: none
        """
        self._name = value

    @property
    def members(self):
        """
        Getter method for team members list

        :return: list of team members
        """
        return self._members

    @members.setter
    def members(self, value):
        """
        Setter method for list of team members.

        :param value: A list of team members to set
        :return: none
        """
        self._members = value

    def add_member(self, member):
        """
        Method to add a member to the team

        For module04, checks for duplicate oids and
        emails are added. Email is set to lowercase to
        ensure checks are case-insensitive.

        :param member: member to add to the team
        :return: none
        """
        lowercase_email = member.email.lower()
        if member.oid in self._members_oids:
            raise DuplicateOid(member.oid)
        if lowercase_email in self._members_emails:
            raise DuplicateEmail(member.email)
        if member not in self._members:
            self._members.append(member)
            self._members_oids.add(member.oid)
            self._members_emails.add(lowercase_email)




    def member_named(self, s):
        """
        Method returns the member provided if it exists on the list

        :param s: name of the member to return if it exists
        :return: the member object
        """
        for member in self._members:
            if member.name == s:
                return member
        return None

    def remove_member(self, member):
        """
        Removes a member from the team list

        Module04 added functionality to also have a removed member
        also removed from the _member_oids and _member_emails sets.

        :param member: member to remove from the team list
        :return: none
        """
        if member in self._members:
            self._members.remove(member)
            self._members_oids.remove(member.oid)
            self._members_emails.remove(member.email)

    def send_email(self, emailer, subject, message):
        """
        Sends an email to all members of the team

        :param emailer: emailer object
        :param subject: subject of the email
        :param message: message of the email
        :return: none
        """
        email_recipients = [member.email for member in self._members if member.email is not None]
        emailer.send_plain_email(email_recipients, subject, message)

    def __str__(self):
        """
        Returns a string value of the object.

        :return: string value of the object
        """
        return f"{self._name}: {len(self._members)} members"
