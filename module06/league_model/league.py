# CPSC 4970 - Python Programming
#
# Assignment 5
#
# Author: Alan Cruce
# Date: April 18, 2025

from module06.league_model.exceptions import DuplicateOid
from module06.league_model.identified_object import IdentifiedObject


class League(IdentifiedObject):
    """
    This is the class for the League object.
    """
    def __init__(self, oid, name):
        """
        This is the contructor for the League object.

        For module04 two new sets were created, a teams_oids set and
        a competitions_oids set to help check to ensure teams and competitions
        with duplicate oids cannot be added.

        :param oid: unique ID for the league
        :param name: name of the league
        """
        super().__init__(oid)
        self._name = name
        self._teams = []
        self._competitions = []
        self._teams_oids = set()
        self._competitions_oids = set()
        self._last_oid = 0

    @property
    def name(self):
        """
        Getter method for league name.

        :return: the league name
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Setter method for the league name.

        :param value: name to set for the league name
        :return: none
        """
        self._name = value

    @property
    def teams(self):
        """
        Getter method for a list of teams in the league

        :return: list of teams in the league
        """
        return self._teams

    @property
    def competitions(self):
        """
        Getter method for a list of competitions in the league

        :return: list of competitions in the league
        """
        return self._competitions

    def add_team(self, team):
        """
        Method for adding a team to the league

        For module04 a check was added to ensure a team with a duplicate
        oid of a team already added to the league is not allowed to be added.

        :param team: Object of what team to add
        :return: none
        """
        if team.oid in self._teams_oids:
            raise DuplicateOid(team.oid)
        if team not in self._teams:
            self._teams.append(team)
            self._teams_oids.add(team.oid)

    def remove_team(self, team):
        """
        Method for removing a team from the league.

        For module04 a check was added to ensure teams cannot be removed
        if they are part of a competition by raising a ValueError.

        In addition, functionality of removing the team.oid from the _teams_oids set
        was also added when a team is successfully removed.

        :param team: the team object to remove
        :return: none
        """
        # check competition list to ensure the team being removed is not involved
        # in any competition
        for competition in self._competitions:
            if team in competition.teams_competing:
                raise ValueError("Team cannot be deleted as it is involved in a competition")

        if team in self._teams:
            self._teams.remove(team)
            self._teams_oids.remove(team.oid)

    def team_named(self, team_name):
        """
        Returns the team object if already on the team list

        :param team_name: Team object to return if exists in the team list
        :return: team object
        """
        for team in self._teams:
            if team.name == team_name:
                return team
        return None

    def add_competition(self, competition):
        """
        Add a competition to the competition list.

        For module04 a check was added to ensure a competition with a duplicate
        oid of a competition already added to the league is not allowed to be added.

        :param competition: which competition to add to the list
        :return: none
        """
        # check for duplicate oid
        if competition.oid in self._competitions_oids:
            raise DuplicateOid(competition.oid)
        # check to ensure all teams are in the league
        for team in competition.teams_competing:
            if team.oid not in self._teams_oids:
                raise ValueError("Team not in league")
        self._competitions.append(competition)
        self._competitions_oids.add(competition.oid)

    def teams_for_member(self, member):
        """
        Returns a list of teams for the member provided.

        :param member: Member whose teams will be returned on a ist
        :return: list of teams the member is on
        """
        return [team for team in self._teams if member in team.members]

    def competitions_for_team(self, team):
        """
        returns a list of competitions involved in for the team provided

        :param team: Team of which a list of competitions will be provided
        :return: list of competitions the provided team are involved in
        """
        return [competition for competition in self._competitions if team in competition.teams_competing]

    def competitions_for_member(self, member):
        """
        returns a list of competitions the provided member is involved in

        :param member: member whose competitions were be provided in a list
        :return: list of competitions the member is involved in
        """
        return [competition for team in self.teams_for_member(member) for competition in self.competitions_for_team(team)]

    def __str__(self):
        """
        Returns a string value of the object.

        :return: string value of the object
        """
        return f"{self._name}: {len(self._teams)} teams, {len(self._competitions)} competitions"

