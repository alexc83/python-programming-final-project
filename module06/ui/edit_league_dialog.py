# CPSC 4970 - Python Programming
#
# Assignment 6 - Final Project
#
# Author: Alan Cruce
# Date: April 28, 2025

import copy
import os

from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QDialog

from module06.league_model.team import Team
from module06.ui.edit_team_dialog import EditTeamDialog

# this code helps prevent issues with relative file paths
complete_file_path = os.path.join(os.path.dirname(__file__), "edit_league_dialog.ui")
UI_MainWindow, QTBaseWindow = uic.loadUiType(complete_file_path)



class EditLeagueDialog(QTBaseWindow, UI_MainWindow):
    """
    This class is for the Edit League dialog that allows users to edit teams
    in the league that was selected in the main window.
    """

    def __init__(self, league_db=None, selected_league=None, parent=None):
        """
        This is the constructor for the edit league dialog. A league database object is passed
        along with the selected league being edited.

        A copy of the selected league is made in the constructor so any changes made are not
        saved to the actual league object until the user hits save. If the dialog is not saved,
        changes are not updated in the database. If saved, the changes are updated in the database
        at that time.

        :param league_db: The league database object
        :param selected_league: The object for the league that was selected to edit
        :param parent:
        """
        # initial setup
        super().__init__(parent)
        self.setupUi(self)
        # league database object
        self.league_db = league_db
        # the selected league is copied for temporary changes until the user saves to the database
        self.selected_league_original = selected_league
        self.selected_league_copy = copy.deepcopy(selected_league)
        self.update_ui()
        # buttons
        self.add_team_button.clicked.connect(self.add_team_button_clicked)
        self.delete_team_button.clicked.connect(self.delete_team_button_clicked)
        self.edit_team_button.clicked.connect(self.edit_team_button_clicked)
        self.export_data_button.clicked.connect(self.export_data_button_clicked)
        self.import_data_button.clicked.connect(self.import_data_button_clicked)
        self.button_box.accepted.connect(self.save_button_clicked)
        self.button_box.rejected.connect(self.cancel_button_clicked)


    def add_team_button_clicked(self):
        """
        This method is executed when the add team button is clicked. A team name
        must be entered by the user or a popup will show stating the user must enter a name.

        Once a team name is entered and add team is clicked, a new Team object is created
        and added to the database.

        The UI is updated with the new team.

        :return: none
        """
        # checks if there is a name entered and throws a message if not
        if self.team_name_line_edit.text() == "":
            self.warn("Enter Name", "You must enter a team name to add")
        else:
            # creates a new Team object using the name provided by the user
            new_team = Team(self.league_db.next_oid(),
                                self.team_name_line_edit.text())
            # updates the team copy object and updates the UI
            self.selected_league_copy.add_team(new_team)
            # this makes the add team name field blank
            self.team_name_line_edit.setText("")
            self.update_ui()


    def delete_team_button_clicked(self):
        """
        This method is executed when the delete team button is clicked. If the user has not
        selected a team in the list widget, a popup box appears to inform the user that a team
        must be selected.

        Once a team is selected and the delete button is clicked, the team selected is removed
        from the database and the UI is updated.

        :return: none
        """
        selected_team = self.get_selected_team()
        if selected_team is None:
            self.warn("Select Team", "You must select a team to delete")
        else:
            self.selected_league_copy.remove_team(selected_team)
            self.update_ui()

    def edit_team_button_clicked(self):
        """
        This method is executed when the edit button is clicked. If the user has not
        selected a team in the list widget, a popup box appears to inform the user that a team
        must be selected.

        Once a team is selected and the edit button is clicked, a dialog window for editing
        the selected team is shown to the user.

        Once the user finishes editing the team, the database is only updated if the user clicks
        save in the edit team dialog box. A popup stating if changes were saved or not is given
        to the user once the edit team dialog box is closed.

        :return: none
        """
        # the team selected to edit is saved
        selected_team = self.get_selected_team()
        # if no team is selected a message is displayed to the user
        if selected_team is None:
            self.warn("Select Team", "You must select a team to edit")
        else:
            # the edit team dialog is executed
            dialog = EditTeamDialog(self.league_db, self.selected_league_copy, selected_team)
            # the UI is updated if changes are saved in the edit team dialog
            # a message stating if changes were made or not is displayed to the user
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.update_ui()
                self.warn("Changes saved", f"Changes to {selected_team.name} were saved")
            else:
                self.warn("Changes not saved", f"Changes to {selected_team.name} were not saved")

    def export_data_button_clicked(self):
        """
        This method is executed when the export data button is clicked. A csv file generated with
        current team data.

        The user is shown a QFileDialog, which will give the user the ability to choose where to
        save the generated csv file. The method defaults to the module06/league_model/data folder.

        If a filename is returned from the QFileDialog, a check is performed to ensure the
        generated file has a .csv extension, and then the export_league_teams() method from
        the league database object is executed.

        :return: none
        """
        # the QFileDialog returns a tuple with the filename in the 0 index
        fn = QFileDialog.getSaveFileName(self, "Save File", "../league_model/data",
                                         "CSV Files (*.csv)")
        # this ensures the file saved is a .csv file
        # the filename is in the 0 index of the fn tuple
        if fn[0]:
            if not fn[0].lower().endswith(".csv"):
                fn[0] += ".csv"
            # generate csv method is executed and a message is displayed to the user
            self.league_db.export_league_teams(self.selected_league_copy, fn[0])
            self.warn("Data Imported", f"Data Imported to file: {fn[0]}")

    def import_data_button_clicked(self):
        """
        This method is executed when the import data button is clicked.

        The user will be shown a QFileDialog box, allowing the user to choose a csv file
        to import. The filter below only allows .csv files to be clickable. The default folder
        is the module06/league_model/data folder.

        The imported file is loaded into the copy of the selected_team object to ensure changes
        are only kept if the user clicks the save button in the edit league dialog.

        :return: none
        """
        # this returns a tuple with the file name in the 0 index
        fn = QFileDialog.getOpenFileName(self, "Open File", "../league_model/data",
                                         "CSV Files (*.csv)")
        # the import_league_teams() method in the league database object is executed and ui updated
        self.league_db.import_league_teams(self.selected_league_copy, fn[0])
        self.update_ui()

    def save_button_clicked(self):
        """
        This method is executed when the save button in the dialog button box is clicked. Since all
        changes made prior to clicking save have been stored in the league copy object, this method
        transfers the changes into the actual database.

        First, a list of leagues in the database is saved and then the index of the selected league
        in found. Finally, the copy object (with the updated changes) is copied into the leagues list
        in the database, thus updating the actual database.

        :return:
        """
        # the list of leagues in the database is saved
        leagues = self.league_db.leagues
        # the index in the leagues list for the selected league is saved
        index = leagues.index(self.selected_league_original)
        # the data from the copy is saved to the database leagues list
        leagues[index] = self.selected_league_copy
        # the dialog box is then closed
        self.accept()

    def cancel_button_clicked(self):
        """
        This method is selected when the cancel button in the dialog button box is clicked.

        Since all changes made prior to clicking cancel are only made to the copy of the selected
        league object, no changes are saved to the actual database (which occurs in the save_button_clicked()
        method.

        This method just closes the dialog.

        :return:
        """
        # the dialog box is closed with no changes being saved to the database
        self.reject()

    def get_selected_team(self):
        """
        This method is used by the edit and delete team methods to return which
        team is currently selected in the list widget to ensure the correct team is being
        managed by the user.

        :return: the team currently selected in the list widget
        """
        selected = self.team_list_widget.selectedItems()
        if not selected:
            return None
        else:
            selected_item = selected[0]
            selected_team = selected_item.data(Qt.ItemDataRole.UserRole)
            return selected_team

    def update_ui(self):
        """
        This method is called whenever changes are made to the database to ensure the changes
        show up in the UI, such as removing deleted teams or adding new teams to the list
        widget.

        :return: none
        """
        row = self.team_list_selected_row()
        self.team_list_widget.clear()
        for team in self.selected_league_copy.teams:
            # self.league_list_widget.addItem(f"League name: {league.name}")
            item = QtWidgets.QListWidgetItem(f"Team name: {team.name}")
            item.setData(Qt.ItemDataRole.UserRole, team)
            self.team_list_widget.addItem(item)

        if row != -1 and len(self.selected_league_copy.teams) > row:
            self.team_list_widget.setCurrentItem(self.team_list_widget.item(row))

    def team_list_selected_row(self):
        """
        This method is used by the update UI method to ensure if a team was selected
        in the list widget that the same team is selected (if not deleted) after the
        UI is updated.

        :return: the index of the team selected in the current database leagues list
        """
        selected = self.team_list_widget.selectedItems()
        if len(selected) == 0:
            return -1
        assert len(selected) == 1
        selected_item = selected[0]
        selected_team = selected_item.data(Qt.ItemDataRole.UserRole)
        for i, team in enumerate(self.selected_league_copy.teams):
            if team == selected_team:
                return i
        return -1

    def warn(self, title, message):
        """
        This method produces a MessageBox based on the parameters.

        :param title: title of the MessageBox
        :param message: the message to be displayed in the MessageBox
        :return: none
        """
        mb = QMessageBox(QMessageBox.Icon.NoIcon, title, message, QMessageBox.StandardButton.Ok)
        mb.exec()
