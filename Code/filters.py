from PyQt5.QtWidgets import QMenu, QAction, QApplication, QStyleOptionMenuItem, QStyle
from PyQt5.QtCore import pyqtSignal, QRect

import software_list


class FilterWindow(QMenu):
    filterSelected = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Filters")
        self.selected_categories = []

        # Fetch categories from the software list and sort them alphabetically
        categories = sorted(set(option["Category"] for option in software_list.soft_list))

        # Add "All" category at the top
        all_action = QAction("All", self)
        all_action.setCheckable(True)
        all_action.triggered.connect(self.category_selected)
        self.addAction(all_action)

        # Create category actions in alphabetical order
        self.category_actions = []
        for category in categories:
            action = QAction(category, self)
            action.setCheckable(True)
            action.triggered.connect(self.category_selected)
            self.addAction(action)
            self.category_actions.append(action)

        # Set background color and style
        self.setStyleSheet("QMenu { background-color: #191919; color: #FFFFFF; }")

    def category_selected(self):
        action = self.sender()

        if action.text() == "All":
            if action.isChecked():
                self.selected_categories = [category_action.text() for category_action in self.category_actions]
                for category_action in self.category_actions:
                    category_action.setChecked(True)
            else:
                self.selected_categories = []
                for category_action in self.category_actions:
                    category_action.setChecked(False)
        else:
            if action.isChecked():
                self.selected_categories.append(action.text())
            else:
                self.selected_categories.remove(action.text())
                # Uncheck "All" if any other category is unchecked
                all_action = self.actions()[0]
                all_action.setChecked(False)

        self.filterSelected.emit(self.selected_categories)

    def showEvent(self, event):
        action = self.activeAction()
        if action:
            opt = QStyleOptionMenuItem()
            self.initStyleOption(opt, action)
            rect = self.style().subElementRect(QStyle.SE_MenuItem, opt, self)

            # Adjust the position of the menu
            button_geometry = self.parentWidget().filter_button.geometry()
            menu_height = rect.height() * self.actions().count()
            menu_width = rect.width()
            menu_x = button_geometry.x() + button_geometry.width() + 2
            menu_y = button_geometry.y()
            menu_rect = QRect(menu_x, menu_y, menu_width, menu_height)
            self.setGeometry(menu_rect)

        super().showEvent(event)
