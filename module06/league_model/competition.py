# CPSC 4970 - Python Programming
#
# Assignment 6 - Final Project
#
# Author: Alan Cruce
# Date: April 28, 2025

from module06.league_model.identified_object import IdentifiedObject


class Competition(IdentifiedObject):
    """
    This class is for the Competition object.
    """
    def __init__(self, oid, teams, location, datetime):
        """
        This is the contractor
        :param oid: this is the unique ID for each competition
        :param teams: this is a list of teams in the competition
        :param location: this is the location of the competition
        :param datetime: a datetime object representing when the competition will occur
        """
        super().__init__(oid)
        self._teams_competing = teams
        self._location = location
        self._date_time = datetime

    @property
    def teams_competing(self):
        """
        This is a getter method for the list of teams in the competition.
        :return: The list of teams competing
        """
        return self._teams_competing

    @property
    def date_time(self):
        """
        This is a getter method for the datetime object for when
        the competition takes place
        :return: the datetime object of the competition date and time
        """
        return self._date_time

    @date_time.setter
    def date_time(self, value):
        """
        Setter method for the date and time of when the competition is taking place.
        :param value: the datetime value to set for the competition
        :return: none
        """
        self._date_time = value

    @property
    def location(self):
        """
        Getter method for the location of the competition

        :return: the location
        """
        return self._location

    @location.setter
    def location(self, value):
        """
        Setter method for the location of the competition

        :param value: the location to set
        :return: none
        """
        self._location = value

    def send_email(self, emailer, subject, message):
        """
        This method sends an email to everybody in the competition

        :param emailer: The object used to email
        :param subject: Subject of the email
        :param message: Message to send in the email
        :return: none
        """
        email_recipients = {
            member.email for team in self.teams_competing
            for member in team.members if member.email is not None
        }
        emailer.send_plain_email(email_recipients, subject, message)


    def __str__(self):
        """
        Returns a string value of the object.

        :return: string value of the object
        """
        if self._date_time:
            formatted_datetime = self._date_time.strftime("%m/%d/%Y %H:%M")
            return (f"Competition at {self._location} on {formatted_datetime} "
                    f"with {len(self._teams_competing)} teams")
