from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QPushButton, QLabel, QMessageBox, QCheckBox,  QSpinBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from qtawesome import icon
from utils.debug import close_debug_terminal
import sys
import json, os
from utils.settings import settings, save_settings
from core.logic.retry_stage import retry_stage
from core.logic.co_op import coop_stage
from core.logic.epic_raid import epic_raid_stage
from core.logic.retry_special_moves import special_moves_stage
from core.logic.sub_stories import sub_stories
from core.logic.brave_battles import brave_battles

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BBS Auto Farmer")
        self.setMinimumSize(600, 500)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.main_tab = QWidget()
        self.settings_tab = QWidget()
        self.info_tab = QWidget()
        
        self.tabs.addTab(self.main_tab, icon("fa5s.home", color="white"), "Main")
        self.tabs.addTab(self.settings_tab, icon("fa5s.cog", color="white"), "Settings")
        self.tabs.addTab(self.info_tab, icon("fa5s.info-circle", color="white"), "Info")
        
        self.init_main_tab()
        self.init_settings_tab()
        self.init_info_tab()
    
    def closeEvent(self, event):
        close_debug_terminal()
        event.accept()

    def save_user_settings(self):
        settings["max_orbs"] = self.orbs_spin.value()
        settings["use_revive_candles"] = self.candles_checkbox.isChecked()
        settings["debug_mode"] = self.debug_checkbox.isChecked()
        settings["max_tickets"] = self.tickets_spin.value()
        settings["auto_set_boost_to_max"] = self.boost_checkbox.isChecked()
        settings["auto_collect_ticket_from_giftbox"] = self.giftbox_checkbox.isChecked()
        settings["brave_battles_tickets"] = self.brave_battles_spin.value()
        save_settings()
    
    def show_error_popup(self, title, message):
        """Display an error popup with the given title and message."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()
    
    def show_success_popup(self, title, message):
        """Display a success popup with the given title and message."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()
    
    def get_settings_summary(self, include_settings=None):
        """Get a formatted string of current settings.
        
        Args:
            include_settings (list): List of setting keys to include. If None, includes all settings.
        """
        if include_settings is None:
            include_settings = [
                'max_orbs', 'max_tickets', 'use_revive_candles', 
                'auto_set_boost_to_max', 'auto_collect_ticket_from_giftbox', 'brave_battles_tickets'
            ]
        
        settings_text = []
        setting_labels = {
            'max_orbs': 'Max Orbs',
            'max_tickets': 'Max Tickets', 
            'use_revive_candles': 'Use Revive Candles',
            'auto_set_boost_to_max': 'Auto Boost to Max',
            'auto_collect_ticket_from_giftbox': 'Auto Collect Ticket from Giftbox',
            'brave_battles_tickets': 'Brave Battles Tickets'
        }
        
        for setting_key in include_settings:
            if setting_key in settings and setting_key in setting_labels:
                settings_text.append(f"- {setting_labels[setting_key]}: {settings[setting_key]}")
        
        return "Settings:\n" + "\n".join(settings_text)
    
    def confirm_and_start_stage(self, stage_name, stage_function, include_settings=None):
        """Generic confirmation dialog for any stage.
        
        Args:
            stage_name (str): Name of the stage
            stage_function (callable): Function to run the stage
            include_settings (list): List of setting keys to show in confirmation dialog
        """
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle(f"Confirm {stage_name}")
        msg.setText(
            f"{self.get_settings_summary(include_settings)}\n\n"
            f"Start {stage_name.lower()} with these settings?"
        )
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        if msg.exec() == QMessageBox.Yes:
            self.run_stage(stage_name, stage_function)
    
    def run_stage(self, stage_name, stage_function):
        """Generic stage runner with error handling."""
        try:
            result = stage_function()
            
            if result is None:
                self.show_error_popup(
                    f"{stage_name} Failed",
                    f"Failed to start {stage_name.lower()}. Please check if the game window is open and properly positioned."
                )
                return
            
            # Check if result is a string (error message)
            if isinstance(result, str):
                self.show_error_popup(f"{stage_name} Error", result)
                return
            
            # Check if result is a tuple (success with orbs and tickets)
            if isinstance(result, tuple) and len(result) == 2:
                orbs_used, tickets_used = result
                self.show_success_popup(
                    f"{stage_name} Completed",
                    f"{stage_name} completed.\n\nOrbs used: {orbs_used}\nTickets used: {tickets_used}"
                )
                return
            
            # Unexpected result type
            self.show_error_popup(
                f"{stage_name} Error",
                f"Unexpected result from {stage_name.lower()}. Please check the implementation."
            )
            
        except Exception as e:
            # Handle general exceptions
            self.show_error_popup(
                f"{stage_name} Error",
                f"An unexpected error occurred during {stage_name.lower()}: {str(e)}"
            )
    
    # Stage-specific methods using the generic approach
    def confirm_and_start_retry(self):
        self.confirm_and_start_stage("Retry Stage", retry_stage, include_settings=['max_orbs', 'max_tickets', 'use_revive_candles', 'auto_set_boost_to_max', 'auto_collect_ticket_from_giftbox'])
    
    def confirm_and_start_coop(self):
        self.confirm_and_start_stage("Co-Op Stage", coop_stage, include_settings=['max_orbs', 'max_tickets', 'use_revive_candles', 'auto_set_boost_to_max'])
    
    def confirm_and_start_epic_raid(self):
        self.confirm_and_start_stage("Epic Raid Stage", epic_raid_stage, include_settings=['max_orbs', 'max_tickets', 'use_revive_candles', 'auto_set_boost_to_max'])
    
    def confirm_and_start_special_moves(self):
        self.confirm_and_start_stage("Special Moves Stage", special_moves_stage, include_settings=[ 'use_revive_candles'])
    
    def confirm_and_start_sub_stories(self):
        self.confirm_and_start_stage("Sub Stories Stage", sub_stories, 
                                   include_settings=['max_orbs', 'max_tickets', 'use_revive_candles'])
    
    def confirm_and_start_brave_battles(self):
        self.confirm_and_start_stage("Brave Battles Stage", brave_battles, 
                                   include_settings=['brave_battles_tickets'])
            
    def init_main_tab(self):
        layout = QVBoxLayout()

        layout.setContentsMargins(20, 10, 20, 0)
        layout.addSpacing(16)  # space between header group and buttons

        # 🧱 Group h1 + p
        header_group = QWidget()
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)  # increased spacing between h1 and p
        header_layout.setContentsMargins(0, 0, 0, 16)  # more bottom margin for the group

        title = QLabel("Main Actions")
        title.setObjectName("h1")
        header_layout.addWidget(title)

        description = QLabel("Select an action to start. (Make sure to change the settings and that the window is 1600x900)")
        description.setObjectName("p")
        header_layout.addWidget(description)

        header_group.setLayout(header_layout)
        layout.addWidget(header_group)

        # 👉 Buttons
        btn_retry = QPushButton("Start Retry Quest")
        btn_retry.setObjectName("primaryButton")
        btn_retry.clicked.connect(self.confirm_and_start_retry)
        layout.addWidget(btn_retry)

        layout.addSpacing(12)

        btn_coop = QPushButton("Start Co-Op Quest")
        btn_coop.setObjectName("dangerButton")
        btn_coop.clicked.connect(self.confirm_and_start_coop)
        layout.addWidget(btn_coop)
        
        layout.addSpacing(12)
        
        btn_epic_raid = QPushButton("Start Epic Raid (Don't recommend it)")
        btn_epic_raid.setObjectName("dangerButton")
        btn_epic_raid.clicked.connect(self.confirm_and_start_epic_raid)
        layout.addWidget(btn_epic_raid)
        layout.addSpacing(12)

        btn_special_moves = QPushButton("Start Special Moves")
        btn_special_moves.setObjectName("dangerButton")
        btn_special_moves.clicked.connect(self.confirm_and_start_special_moves)
        layout.addWidget(btn_special_moves)
        
        layout.addSpacing(12)

        btn_sub_stories = QPushButton("Start Sub Stories")
        btn_sub_stories.setObjectName("dangerButton")
        btn_sub_stories.clicked.connect(self.confirm_and_start_sub_stories)
        layout.addWidget(btn_sub_stories)
        
        layout.addSpacing(12)

        btn_brave_battles = QPushButton("Start Brave Battles")
        btn_brave_battles.setObjectName("dangerButton")
        btn_brave_battles.clicked.connect(self.confirm_and_start_brave_battles)
        layout.addWidget(btn_brave_battles)

        layout.addStretch(1)
        self.main_tab.setLayout(layout)
        
    def init_settings_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 10, 20, 0)
        layout.addSpacing(16)

        title = QLabel("Settings")
        title.setObjectName("h1")
        layout.addWidget(title)
        layout.addSpacing(12)

        # Orbs setting
        orbs_label = QLabel("Amount of Orbs to Use: (0 = Waits for tickets to recharge)")
        orbs_label.setObjectName("p")
        layout.addWidget(orbs_label)
        self.orbs_spin = QSpinBox()
        self.orbs_spin.setMinimum(0)
        self.orbs_spin.setMaximum(100000)
        self.orbs_spin.setValue(settings["max_orbs"])
        layout.addWidget(self.orbs_spin)
        layout.addSpacing(12)

        # Tickets setting
        tickets_label = QLabel("Amount of Tickets to Use: (-1 = Infinite)")
        tickets_label.setObjectName("p")
        layout.addWidget(tickets_label)
        self.tickets_spin = QSpinBox()
        self.tickets_spin.setMinimum(-1)
        self.tickets_spin.setMaximum(100000)
        self.tickets_spin.setValue(settings["max_tickets"])
        layout.addWidget(self.tickets_spin)
        layout.addSpacing(12)

        # Revive candles setting
        self.candles_checkbox = QCheckBox("Use Revive Candles")
        self.candles_checkbox.setChecked(settings["use_revive_candles"])
        layout.addWidget(self.candles_checkbox)
        layout.addSpacing(16)
        
        # Debug mode setting
        self.debug_checkbox = QCheckBox("Debug Mode")
        self.debug_checkbox.setChecked(settings["debug_mode"])
        layout.addWidget(self.debug_checkbox)
        layout.addSpacing(16)

        # Auto set boost to max setting
        self.boost_checkbox = QCheckBox("Auto Set Boost to Max")
        self.boost_checkbox.setChecked(settings["auto_set_boost_to_max"])
        layout.addWidget(self.boost_checkbox)
        layout.addSpacing(16)

        # Auto collect ticket from giftbox setting
        self.giftbox_checkbox = QCheckBox("Auto Collect Ticket from Giftbox")
        self.giftbox_checkbox.setChecked(settings["auto_collect_ticket_from_giftbox"])
        layout.addWidget(self.giftbox_checkbox)
        layout.addSpacing(16)

        # Brave Battles tickets setting
        brave_battles_label = QLabel("Amount of Brave Battles to Complete: (-1 = Infinite)")
        brave_battles_label.setObjectName("p")
        layout.addWidget(brave_battles_label)
        self.brave_battles_spin = QSpinBox()
        self.brave_battles_spin.setMinimum(-1)
        self.brave_battles_spin.setMaximum(1000)
        self.brave_battles_spin.setValue(settings.get("brave_battles_tickets", 10))
        layout.addWidget(self.brave_battles_spin)
        layout.addSpacing(16)

        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_user_settings)
        layout.addWidget(save_btn)

        layout.addStretch(1)
        self.settings_tab.setLayout(layout)

    def init_info_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 10, 20, 0)
        layout.addSpacing(16)

        title = QLabel("Info & Resources")
        title.setObjectName("h1")
        layout.addWidget(title)
        layout.addSpacing(12)

        github_label = QLabel('<a href="https://github.com/xJohnnyrl/bbs-auto-farmer">GitHub Repository</a>')
        github_label.setOpenExternalLinks(True)
        github_label.setObjectName("p")
        layout.addWidget(github_label)
        layout.addSpacing(8)

        youtube_label = QLabel('<a href="https://youtu.be/5Iqe13ydSzs?si=s4jfnPJjI7ouNKj0n">YouTube Tutorial</a>')
        youtube_label.setOpenExternalLinks(True)
        youtube_label.setObjectName("p")
        layout.addWidget(youtube_label)
        layout.addSpacing(8)

        feedback_label = QLabel('Submit feedback or issues on <a href="https://github.com/xJohnnyrl/bbs-auto-farmer/issues">GitHub Issues</a>, send me a message on <a href="https://x.com/xJohnnyrl">Twitter</a>, or just leave a comment on the youtube tutorial.')
        feedback_label.setOpenExternalLinks(True)
        feedback_label.setObjectName("p")
        layout.addWidget(feedback_label)
        layout.addSpacing(16)

        layout.addStretch(1)
        self.info_tab.setLayout(layout)

def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # Load style sheet using resource manager
    from utils.resource_manager import get_resource_path
    style_path = get_resource_path("gui/style.qss")
    with open(style_path, "r") as f:
        app.setStyleSheet(f.read())
    
    window.show()
    sys.exit(app.exec())