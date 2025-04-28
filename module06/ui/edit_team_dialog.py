import copy

from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QDialog

from module06.league_model.team_member import TeamMember
from module06.ui.edit_member_dialog import EditMemberDialog

UI_MainWindow, QTBaseWindow = uic.loadUiType("edit_team_dialog.ui")


class EditTeamDialog(QTBaseWindow, UI_MainWindow):

    def __init__(self, league_db=None, selected_league=None, selected_team=None, parent=None):
        # initial setup
        super().__init__(parent)
        self.setupUi(self)
        self.league_db = league_db
        self.selected_league = selected_league
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
        selected_member = self.get_selected_member()
        if selected_member is None:
            self.warn("Select Member", "You must select a team member to delete")
        else:
            self.selected_team_copy.remove_member(selected_member)
            self.update_ui()

    def edit_member_button_clicked(self):
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
        print("Save clicked")
        teams = self.selected_league.teams
        index = teams.index(self.selected_team_original)
        teams[index] = self.selected_team_copy
        self.accept()

    def cancel_button_clicked(self):
        # self.warn("Changes not saved", "Changes will not be saved")
        self.reject()

    def get_selected_member(self):
        selected = self.member_list_widget.selectedItems()
        if not selected:
            return None
        else:
            selected_item = selected[0]
            selected_member = selected_item.data(Qt.ItemDataRole.UserRole)
            return selected_member

    def update_ui(self):
        row = self.member_list_selected_row()
        self.member_list_widget.clear()
        for member in self.selected_team_copy.members:
            item = QtWidgets.QListWidgetItem(f"Member name: {member.name}")
            item.setData(Qt.ItemDataRole.UserRole, member)
            self.member_list_widget.addItem(item)

        if row != -1 and len(self.selected_team_copy.members) > row:
            self.member_list_widget.setCurrentItem(self.member_list_widget.item(row))

    def member_list_selected_row(self):
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
        mb = QMessageBox(QMessageBox.Icon.NoIcon, title, message, QMessageBox.StandardButton.Ok)
        mb.exec()

