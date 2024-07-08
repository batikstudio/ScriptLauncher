#! /usr/bin/env python3

import os
import subprocess
import configparser  # Config file manager module
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QListView, QComboBox,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget, QFileDialog, QMessageBox)
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QFile)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFontDatabase, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)


# Create the application, load .ui file and show window
app = QApplication([])
ui_file = "./components/main.ui"
loader = QUiLoader()
window = loader.load(ui_file)
window.show()
home_dir = os.environ['HOME']
working_dir = f"{home_dir}/.config/scriptlauncher"
CONFIG_FILE = f"{working_dir}/config.ini"


# Get selected folder and load scripts into QlistWidget
def select_directory():
    global directory
    directory = QFileDialog.getExistingDirectory(window, "Select folder", home_dir)
    if directory:
        line_folder.setText(directory)
        update_script_list()

# Save default folder in settings
def save_default_directory(directory):
    config = get_config()
    set_config_value(config, "Preferences", "DefaultDirectory", directory)
    save_config(config)
    print("New path saved")


# Update QlistWidget with the current folder
def update_script_list():
    global directory
    try:
        if directory:
            script_list.clear()
            script_files = [filename for filename in os.listdir(directory) if filename.lower().endswith(".sh")]
            sorted_script_files = sorted(script_files, key=lambda x: x.lower())
            script_list.addItems(sorted_script_files)
    except FileNotFoundError:
        QMessageBox.critical(window, "Directory not found", "The selected directory in config file not exist") 
    except:
        QMessageBox.critical(window, "Error", "There was an error") 


# Slot to update the list when clic "Scan" or change path manually
def scan_directory():
    global directory
    directory = line_folder.text()
    update_script_list()

# Run selected script
def run_selected_script():
    selected_item = script_list.currentItem()
    if selected_item:
        script_path = os.path.join(directory, selected_item.text())
        run_script_in_terminal(script_path)

def run_script_in_terminal(script_path):

    target_terminals = [
        ["x-terminal-emulator", "-e"],  # Ubuntu
        ["gnome-terminal", "--"],       # GNOME
        ["konsole", "-e"],              # KDE
        ["xfce4-terminal", "-e"],       # XFCE
        ["lxterminal", "-e"],           # LXDE
        ["mate-terminal", "-e"],        # MATE
        ["xterm", "-e"],                # Xterm systems
        ["urxvt", "-e"]                 # rxvt-unicode
    ]
    terminal_found = False
    
    for terminal in target_terminals:
        try:
            subprocess.Popen(terminal + [f"/bin/bash", script_path])
            print(f"Detected terminal: ", terminal[0])
            terminal_found = True
            break

        except Exception as e:
            print(f"Terminal not found '{terminal[0]}': {e}")
            print("Next...")
            
    if not terminal_found:
        print("No terminal found")
        return False
    else:
        return True

def verify_config_file():

    if os.path.exists(CONFIG_FILE):
        # Verify if exist config file and print in terminal
        print(f"The config file {CONFIG_FILE} was found")
    else:
        # If config file not exist, show an error dialog
        message = f"The config file {CONFIG_FILE} couldn't be found... Creating a new file."
        QMessageBox.critical(None, "Error", message)
        try:
            os.mkdir(working_dir)
            new_config_file = open(CONFIG_FILE, "w")
            new_config_file.write("[Preferences]\ndefaultdirectory = ")
            print("New config file created")
            new_config_file.close()
        except FileExistsError:
            new_config_file = open(CONFIG_FILE, "w")
            new_config_file.write("[Preferences]\ndefaultdirectory = ")
            print("New config file created")
            new_config_file.close()
        except:
            print("There was an error")
            

# Get config from config from config file
def get_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

# Save in config file
def save_config(config):
    with open(CONFIG_FILE, "w") as config_file:
        config.write(config_file)

# Get value from config file
def get_config_value(config, section, key, fallback=""):
    return config.get(section, key, fallback=fallback)

# Set up the value to config variable
def set_config_value(config, section, key, value):
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, value)

# Get path from config
def get_default_directory():
    config = get_config()
    return get_config_value(config, "Preferences", "DefaultDirectory")

def recover_dir():
    line_folder.setText(default_directory) # Set up path in QLineInput


def show_about_dialog():
    print("about")
    with open("../share/doc/about.txt", "r") as file:
        about_text = file.read()
    #    QMessageBox.critical(window, "About", about_text)
    about_window = QMessageBox(window)
    logo = QPixmap("../share/icons/app_logo_128x128.png")
    about_window.setWindowTitle("About MHL File Verify")
    about_window.setText(about_text)
    about_window.setIconPixmap(logo)
    about_window.setStandardButtons(QMessageBox.Ok)
    about_window.exec()


def save_default_directory_from_lineedit():
    save_default_directory(line_folder.text())
    
def load_fonts():
    # To find real name of a font "fc-scan OpenSans-SemiBold.ttf"
    print("Fonts Loaded")
    QFontDatabase.addApplicationFont('../share/fonts/OpenSans-Regular.ttf')
    QFontDatabase.addApplicationFont('../share/fonts/OpenSans-Light.ttf')
    QFontDatabase.addApplicationFont('../share/fonts/OpenSans-SemiBold.ttf')

load_fonts()
verify_config_file() # Launch verify config file function

# Create variables to reference menu actions
action_open_folder = window.findChild(QAction, "action_open_folder")
action_run = window.findChild(QAction, "action_run")
action_default_dir = window.findChild(QAction, "action_default_dir")
action_recover_dir = window.findChild(QAction, "action_recover_dir")
menu_about = window.findChild(QMenu, "menuAbout")
action_about = window.findChild(QAction, "action_about")
action_exit = window.findChild(QAction, "action_exit")

# Connect menu actions to functions
action_open_folder.triggered.connect(select_directory)
action_run.triggered.connect(run_selected_script)
action_default_dir.triggered.connect(save_default_directory_from_lineedit)
action_recover_dir.triggered.connect(recover_dir)
action_about.triggered.connect(show_about_dialog)
action_exit.triggered.connect(QCoreApplication.quit)

# Get QListWidget from .ui file and create a variable to store the path
script_list = window.findChild(QListView, "list_scripts")
line_folder = window.findChild(QLineEdit, "line_folder")
directory = ""

default_directory = get_default_directory() # Get default path from config file
line_folder.setText(default_directory) # Set up path in QLineInput
directory = default_directory
update_script_list() # Show list scripts when boot the app

# Connect function to directory selection button
select_directory_button = window.findChild(QPushButton, "button_open")
select_directory_button.clicked.connect(select_directory)

# Connect function to run button
run_script_button = window.findChild(QPushButton, "button_run")
run_script_button.clicked.connect(run_selected_script)

# Connect function to double click QListWidget event
script_list.itemDoubleClicked.connect(run_selected_script)

# Connect function to scan button and the change in QLineEdit
scan_button = window.findChild(QPushButton, "button_scan")
scan_button.clicked.connect(scan_directory)

app.exec() # Launch app
