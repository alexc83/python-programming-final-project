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
from PyQt6.QtWidgets import QMessageBox, QDialog

from module06.league_model.team_member import TeamMember
from module06.ui.edit_member_dialog import EditMemberDialog

# this code helps prevent issues with relative file paths
complete_file_path = os.path.join(os.path.dirname(__file__), "edit_team_dialog.ui")
UI_MainWindow, QTBaseWindow = uic.loadUiType(complete_file_path)


class EditTeamDialog(QTBaseWindow, UI_MainWindow):
    """
    This class is for the Edit Team dialog that allows users to edit members
    on the team that was selected in the main window.
    """

    def __init__(self, league_db=None, selected_league=None, selected_team=None, parent=None):
        """
        This is the constructor for the edit team dialog. A league database object is passed
        along with the selected team being edited and the league that the team belongs to.

        A copy of the selected team is made in the constructor so any changes made are not
        saved to the actual team object until the user hits save. If the dialog is not saved,
        changes are not updated in the database. If saved, the changes are updated in the database
        at that time.

        :param league_db: The league database object
        :param selected_team: The actual team selected to be edited
        :param selected_league: The league that the selected team belows to
        :param parent:
        """
        # initial setup
        super().__init__(parent)
        self.setupUi(self)
        # league database object and selected league object
        self.league_db = league_db
        self.selected_league = selected_league
        # the selected team is copied for temporary changes until the user saves to the database
        self.selected_team_original = selected_team
        self.selected_team_copy = copy.deepcopy(selected_team)
        self.update_ui()
        # buttons
        self.add_member_button.clicked.connect(self.add_member_button_clicked)
        self.delete_member_button.clicked.connect(self.delete_member_button_clicked)
        self.edit_member_button.clicked.connect(self.edit_member_button_clicked)
        self.button_box.accepted.connect(self.save_button_clicked)
        self.button_box.rejected.connect(self.cancel_button_clicked)

    def add_member_button_clicked(self):
        """
        This method is executed when the add member button is clicked. A member name and email
        must be entered by the user or a popup will show stating the user must enter a name and email.

        Once a member name and email is entered and add member is clicked, a new TeamMember object is created
        and added to the database.

        The UI is updated with the new team member.

        :return: none
        """
        # checks if there is a name and email entered and throws a message if not
        if self.member_name_line_edit.text() == "" or self.member_email_line_edit.text() == "":
            self.warn("Enter Name and Email", "You must enter a member name and email to add")
        else:
            # creates a new TeamMember object using the name and email provided by the user
            new_member = TeamMember(self.league_db.next_oid(), self.member_name_line_edit.text(),
                                    self.member_email_line_edit.text())
            # updates the team copy object and updates the UI
            self.selected_team_copy.add_member(new_member)
            # this makes the add member name and email fields blank
            self.member_name_line_edit.setText("")
            self.member_email_line_edit.setText("")
            self.update_ui()

    def delete_member_button_clicked(self):
        """
        This method is executed when the delete member button is clicked. If the user has not
        selected a team member in the list widget, a popup box appears to inform the
        user that a team member must be selected.

        Once a team member is selected and the delete button is clicked, the team member selected
        is removed from the database and the UI is updated.

        :return: none
        """
        selected_member = self.get_selected_member()
        if selected_member is None:
            self.warn("Select Member", "You must select a team member to delete")
        else:
            self.selected_team_copy.remove_member(selected_member)
            self.update_ui()

    def edit_member_button_clicked(self):
        """
        This method is executed when the edit button is clicked. If the user has not
        selected a team member in the list widget, a popup box appears to inform the user
        that a team member must be selected.

        Once a team member is selected and the edit button is clicked, a dialog window for
        editing the selected team member is shown to the user.

        Once the user finishes editing the team member, the database is only updated if the user
        clicks save in the edit team member dialog box. A popup stating if changes were saved or
        not is given to the user once the edit team member dialog box is closed.

        :return: none
        """
        selected_member = self.get_selected_member()
        if selected_member is None:
            self.warn("Select Member", "You must select a team member to edit")
        else:
            dialog = EditMemberDialog(selected_member)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.update_ui()
                self.warn("Changes saved", f"Changes to {selected_member.name} were saved")
            else:
                self.warn("Changes not saved", f"Changes to {selected_member.name} were not saved")

    def save_button_clicked(self):
        """
        This method is executed when the save button in the dialog button box is clicked. Since all
        changes made prior to clicking save have been stored in the team copy object, this method
        transfers the changes into the actual database.

        First, a list of teams in the selected league object is saved and then  the index of the
        selected team in found. Finally, the copy object (with the updated changes) is copied into
        the teams list in the selected_league object, thus updating the team and league data.

        :return: none
        """
        # the list of teams in the selected league object is saved
        teams = self.selected_league.teams
        # the index in the team list for the selected team is saved
        index = teams.index(self.selected_team_original)
        # the data from the copy is saved to the selected league teams list
        teams[index] = self.selected_team_copy
        # the dialog box is then closed
        self.accept()

    def cancel_button_clicked(self):
        """
        This method is selected when the cancel button in the dialog button box is clicked.

        Since all changes made prior to clicking cancel are only made to the copy of the selected
        team object, no changes are saved to the selected league object (which occurs in the
        save_button_clicked() method.

        This method just closes the dialog.

        :return:
        """
        self.reject()

    def get_selected_member(self):
        """
        This method is used by the edit and delete member methods to return which
        team member is currently selected in the list widget to ensure the correct team member
        is being managed by the user.

        :return: the team member currently selected in the list widget
        """
        selected = self.member_list_widget.selectedItems()
        if not selected:
            return None
        else:
            selected_item = selected[0]
            selected_member = selected_item.data(Qt.ItemDataRole.UserRole)
            return selected_member

    def update_ui(self):
        """
        This method is called whenever changes are made to the database to ensure the changes
        show up in the UI, such as removing deleted team members or adding new team members to
        the list widget.

        :return: none
        """
        row = self.member_list_selected_row()
        self.member_list_widget.clear()
        for member in self.selected_team_copy.members:
            item = QtWidgets.QListWidgetItem(f"Member name: {member.name}")
            item.setData(Qt.ItemDataRole.UserRole, member)
            self.member_list_widget.addItem(item)

        if row != -1 and len(self.selected_team_copy.members) > row:
            self.member_list_widget.setCurrentItem(self.member_list_widget.item(row))

    def member_list_selected_row(self):
        """
        This method is used by the update UI method to ensure if a team memberswas selected
        in the list widget that the same team member is selected (if not deleted) after the
        UI is updated.

        :return: the index of the team member selected in the selected team list
        """
        selected = self.member_list_widget.selectedItems()
        if len(selected) == 0:
            return -1
        assert len(selected) == 1
        selected_item = selected[0]
        selected_member = selected_item.data(Qt.ItemDataRole.UserRole)
        for i, member in enumerate(self.selected_team_copy.members):
            if member == selected_member:
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

