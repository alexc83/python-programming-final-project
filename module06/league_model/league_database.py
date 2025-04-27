
import csv
import os
import pickle

from module06.league_model.league import League
from module06.league_model.team import Team
from module06.league_model.team_member import TeamMember


class LeagueDatabase:
    """
    This class sets up functionality for the League Database as
    required by the assignment instructions. The main() method below
    tests all the functionality. All files are stored in league_model/data.

    The following steps are taken:

    1.) The load database function will create a new leaguel.db file
    the first time the database is loaded.

    2.) A database instance is created.

    3.) New leagues are created using the League constructor
    and then added or removed from the database.

    4.) The database is saved with league.db.backup backing
    up the most recent league.db file.

    5.) The main class also exports the test file for the assignment,
    Teams.csv. The data is loaded into league1.

    6.) League 1, with the test data loaded, is then exported into
    league1.csv.
    """

    # class variable
    _sole_instance = None

    @classmethod
    def instance(cls):
        """
        Class method for the sole instance of the class
        :return: _sole_instance class variable
        """
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    @classmethod
    def load(cls, file_name):
        """
        Class method for loading the database using the
        provided file name. If no file is found, then a new
        database is created using the file name provided.
        This is done via the pickle module.

        :param file_name: name of the database file to be loaded
        :return: none
        """
        try:
            with open(file_name, mode="rb") as file:
                cls._sole_instance = pickle.load(file)
        except FileNotFoundError as e:
            print(f"Error, database file not found.")
            print(f"Python error: {e}")
            print(f"New database created")
            cls._sole_instance = cls()

    def __init__(self):
        """
        Constructor to initiate a new leagues list when the database
        is first created along with initiating the last_oid at 0.
        """
        self._leagues = []
        self._last_oid = 0

    @property
    def leagues(self):
        """
        Getter method for the leagues list.

        :return: the leagues list
        """
        return self._leagues

    @property
    def last_oid(self):
        """
        Getter method for the last_oid field.
        :return: the last_oid
        """
        return self._last_oid

    @last_oid.setter
    def last_oid(self, value):
        """
        Setter for last_oid. This is used when a new league
        or team is added to the league database to ensure the oid
        is unique. The value is the new oid to be set to the last_oid
        field.

        :param value: updated value for last_oid
        :return: none
        """
        self._last_oid = value

    def add_league(self, league):
        """
        Method for adding a league to the database.

        :param league: The league object to be added
        :return: none
        """
        self._leagues.append(league)

    def remove_league(self, league):
        """
        Method for removing a league from the database.

        :param league: the league object to be removed
        :return: none
        """
        self._leagues.remove(league)

    def league_named(self, name):
        """
        Method that returns a league based on the league name
        from the database if it exists, otherwise None is returned.

        :param name: the league name to be searched for
        :return: the league required or None if the league is not found
        """
        for league in self._leagues:
            if league.name == name:
                return league
        return None

    def next_oid(self):
        """
        This method iterates the last_oid field by 1 when adding
        a new league or team to the database.

        :return: updated last_oid
        """
        self._last_oid += 1
        return self._last_oid

    def save(self, file_name):
        """
        This method saves the database. If a databse file is with the name
        provided is already found, that database is copied as a backup before the
        changes are saved. This is done via the pickle module.

        :param file_name: Name of the file to save the database to.
        :return: none
        """
        if os.path.exists(file_name):
            backup_file = file_name + ".backup"
            os.replace(file_name, backup_file)
        with open(file_name, "wb") as file:
            pickle.dump(self, file)
            print(f"Database saved to {file_name}")

    def import_league_teams(self, league, file_name):
        """
        This method loads a csv file with team and team member
        data and loads that data into the league specified in the database.

        :param league: the league to load the data into
        :param file_name: the csv file with the data to be loaded
        :return: none
        """

        try:
            with open(file_name, mode='r', encoding="UTF_8") as csv_file:
                reader = csv.reader(csv_file)
                # skip header
                next(reader)

                for row in reader:
                    team_name, member_name, member_email = row

                    # team object
                    team = league.team_named(team_name)
                    # add team is not added already
                    if team is None:
                        team = Team(self.next_oid(), team_name)
                        league.add_team(team)

                    # member object
                    member = team.member_named(member_name)
                    # add team member if not added already
                    if member is None:
                        member = TeamMember(self.next_oid(), member_name, member_email)
                        team.add_member(member)
        except Exception as e:
            print(f"Error {e}")

    def export_league_teams(self, league, file_name):
        """
        This method exports the data in the database from a specific league
        into a csv file.

        :param league: The league whose data is to be exported
        :param file_name: The file to save the csv data to
        :return none
        """
        try:
            with open(file_name, mode="w", encoding="utf-8", newline="") as csv_file:
                writer = csv.writer(csv_file)

                writer.writerow(["Team name", "Member name", "Member email"])

                for team in league.teams:
                    for member in team.members:
                        writer.writerow([team.name, member.name, member.email])
        except Exception as e:
            print(f"{e}")

def main():
    """
    This method is testing all of the above methods

    :return: none
    """
    # load database for the first time
    LeagueDatabase.load("data/league.db")
    # create database instance
    db = LeagueDatabase.instance()
    # add leagues to database
    league1 = League(db.next_oid(), "League 1")
    league2 = League(db.next_oid(), "League 2")
    db.add_league(league1)
    db.add_league(league2)
    # save database
    db.save("./data/league.db")
    # add a third league
    league3 = League(db.next_oid(), "League 3")
    db.add_league(league3)
    # delete league 3
    db.remove_league(league3)
    db.save("./data/league.db")
    # import data from Teams.csv
    db.import_league_teams(league1, "./data/Teams.csv")
    db.save("./data/league.db")
    # export data from league 1 to a new csv file
    db.export_league_teams(league1, "./data/league1.csv")
    db.save("./data/league.db")


if __name__ == "__main__":
    main()
