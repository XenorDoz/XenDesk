"""
Main application window.

Acts as the root UI Container of XenDesk 
and assemble the main interface components.
"""

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QPushButton, QStackedWidget

from ui.side_bar import SideBar
import ui.content_view as CV

from core.configManager import config


"""
Hierarchy:
core_window
    - main_layout
        - main_side_bar
        - content_stack
"""

# Subclass to customize main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ##########
        # Core elements
        ##########

        self.setWindowTitle("XenDesk")
        self.setMinimumSize(QSize(config.main_window_size.width, config.main_window_size.height))

        ##########
        # Views stock
        ##########

        self.system_views = {
            0: CV.WelcomeView,
            1: CV.ConfigView
        }

        self.views = {} # Stores created views for access                                   id: <ContentView> 
        self.current_views = [] # Stores shown views, for "previous view" purposes          id

        ##########
        # Added stuff
        ##########

        self.main_layout = QHBoxLayout()

        # Sidebar

        self.main_side_bar = SideBar()
        self.main_side_bar.setFixedWidth(config.main_sidebar_width)
        
        self.config_button = QPushButton("Config")
        self.config_button.setProperty("role", "system-button")
        self.config_button.clicked.connect(self.show_view)
        button_size = int(config.main_sidebar_width - .1 * config.main_sidebar_width)
        self.config_button.setFixedSize(button_size, button_size)                 
        self.config_button.setAutoFillBackground(True)          

        radius = button_size // 2
        margin = (config.main_sidebar_width - button_size) // 2
        self.main_side_bar.layout().setContentsMargins(margin, 0, margin, margin)  # type: ignore
        self.config_button.setStyleSheet(f"""
            background-color: blue;
            color: white;
            border-radius: {radius}px;
        """)                                                                        # TODO THEME to custom later

        self.main_side_bar.layout().addStretch() # type: ignore
        self.main_side_bar.layout().addWidget(self.config_button, alignment = Qt.AlignmentFlag.AlignHCenter) # type: ignore

        # Content view
        
        self.content_stack = QStackedWidget()

        # Add everything
        
        self.main_layout.addWidget(self.main_side_bar)
        self.main_layout.addWidget(self.content_stack)

        ##########
        # Adding it to core window
        ##########

        self.core_window = QWidget()
        self.core_window.setLayout(self.main_layout)
        self.setCentralWidget(self.core_window)

        self.content_stack.layout().addWidget(CV.ConfigView()) # type: ignore


    # Was doing too much for that issue, keeping it for later

    

    def show_view(self,id):
        pass

        # # Show welcome view
        # self.show_view(0)




    # def show_view(self, id):
    #     # If displayed but hidden
    #     if id in self.current_views:
    #         return

    #     # If only in memory
    #     if id in self.views:
    #         return

    #     # If does not exist

    # def create_view(self, view_type: type[CV.ContentView], id: int | None = None):
    #     """
    #     Creates view, and add it to the view stack
    #     type: ContentView
    #     id: int, should only be used for predifined core systems
        
    #     Returns ID
    #     """

    #     # Grab next ID
    #     ID = config.next_global_id
    #     config.next_global_id += 1
    #     config.save()

    #     # Create view
    #     new_view = view_type()

    #     # Add it to view list
    #     self.views[ID] = new_view
    #     return ID

    # def show_view(self, ID: int | None = None):
    #     """
    #     Receives requests by ID
    #     Filters then asks view to get_view from ID and put it on top
    #     """

    #     index = self.get_view(ID)
        
    #     # Put it on top
    #     self.current_views.append(self.current_views.pop(index))  # type: ignore
    #     self.content_stack.setCurrentIndex(index) # type: ignore
        
    # def get_view(self, ID):
    #     """
    #     Receives ID 
    #     If ID not found, gives error view
    #     """                                      # TODO Error view
    #     if id != -1:        
    #         # Checks if exists
    #         if ID in self.views:
    #             # Grab the view
    #             return self.current_views.index(ID)

    #     # If nothing or error, show welcome view
    #     else:
    #         if 0 not in self.current_views:
    #             # If welcome view does not exist, create it
    #             return self.create_view(CV.WelcomeView, 0)          # TODO Error view
    #         else:
    #             # Otherwise, grab it
    #             return self.current_views.index(0)
        
    # def app_toggle_view(self, id):
    #     if id in self.views:
    #         self.show_view(id)
    #     elif id in self.system_views:
    #         self.show_view(self.create_view(self.system_views[id], id))