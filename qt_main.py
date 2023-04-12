import sys
import os

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPlainTextEdit,
    QAction,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QRadioButton,
    QPushButton,
    QFileDialog,
    QWidget,
    QCheckBox
)


class LogViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Log Viewer')

        # Create a text edit for displaying logs
        self.logTextEdit = QPlainTextEdit()
        self.logTextEdit.setReadOnly(True)

        # Create a menu bar
        menuBar = self.menuBar()

        # Create a file menu
        fileMenu = menuBar.addMenu('File')

        # Create an "Open" action
        openAction = QAction('Open', self)
        openAction.triggered.connect(self.openFile)
        fileMenu.addAction(openAction)

        # Create a "Quit" action
        quitAction = QAction('Quit', self)
        quitAction.triggered.connect(self.quit)
        fileMenu.addAction(quitAction)

        # Create a group box for log level filters
        self.logLevelGroupBox = QGroupBox('Filter by log level')

        # Create radio buttons for each log level
        self.infoRadioButton = QCheckBox('Info')
        self.warningRadioButton = QCheckBox('Warning')
        self.errorRadioButton = QCheckBox('Error')
        self.debugRadioButton = QCheckBox('Debug')

        # Set the "Info" radio button as the default selection
        self.infoRadioButton.setChecked(True)

        # Create a layout for the radio buttons
        logLevelLayout = QHBoxLayout()
        logLevelLayout.addWidget(self.infoRadioButton)
        logLevelLayout.addWidget(self.warningRadioButton)
        logLevelLayout.addWidget(self.errorRadioButton)
        logLevelLayout.addWidget(self.debugRadioButton)

        # Set the layout for the log level group box
        self.logLevelGroupBox.setLayout(logLevelLayout)

        # Create a "Filter" button
        filterButton = QPushButton('Filter')
        filterButton.clicked.connect(self.filterLogs)

        # Create a layout for the filter button
        filterLayout = QVBoxLayout()
        filterLayout.addWidget(self.logTextEdit)
        filterLayout.addWidget(self.logLevelGroupBox)
        filterLayout.addWidget(filterButton)

        # Create a widget for the filter button layout and set it as the central widget
        filterWidget = QWidget()
        filterWidget.setLayout(filterLayout)
        self.setCentralWidget(filterWidget)

    def openFile(self):
        # Open a file dialog to choose a file
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open File')

        if fileName != '':
            # Read logs from file
            self.readLogsFromFile(fileName)

    def readLogsFromFile(self, filepath, filters=None):
        with open(filepath, 'r') as f:
            logs = f.readlines()

        if filters is not None and len(filters) > 0:
            filtered_logs = list()
            for log in logs:
                for filter in filters:
                    if filter in log:
                        filtered_logs.append(log)
            self.logTextEdit.setPlainText(''.join(filtered_logs))
        else:
            self.logTextEdit.setPlainText(''.join(logs))

    def filterLogs(self):
        logLevel = list()
        if self.infoRadioButton.isChecked():
            logLevel.append('INFO')
        if self.warningRadioButton.isChecked():
            logLevel.append('WARNING')
        if self.errorRadioButton.isChecked():
            logLevel.append('ERROR')
        if self.debugRadioButton.isChecked():
            logLevel.append('DEBUG')

        # Read filtered logs from file
        logs_file = 'example.log'
        if os.path.exists(logs_file):
            self.readLogsFromFile(logs_file, logLevel)
        else:
            print(f"Error: Could not find logs file {logs_file}")
            sys.exit(1)

    def quit(self):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    logViewer = LogViewer()
    logViewer.setGeometry(100, 100, 800, 600)
    logViewer.show()

    sys.exit(app.exec_())
