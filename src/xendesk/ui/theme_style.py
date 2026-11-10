# Semantic color, not part of the theme: destructive actions stay red
DELETE_COLOR = "#c0392b"


def build_stylesheet(colors: dict) -> str:
    """
    Builds one stylesheet from a theme dict
    """
    primary = colors["primary"]
    secondary = colors["secondary"]
    buttons = colors["buttons"]
    text = colors["text"]

    return f"""
        #root {{ background-color: {primary}; }}
        #sidebar, #content, #config_view, #welcome_view {{ background-color: {secondary}; }}

        QWidget {{ font-size: 14pt; }}
        QLabel {{ color: {text}; background: transparent; }}
        QLabel[role="title"] {{ font-size: 40pt; font-weight: bold; }}
        QLabel[role="title2"] {{ font-size: 20pt; font-weight: bold; }}
        QLabel[role="title3"] {{ font-size: 16pt; font-weight: bold; }}
        QLabel[role="subtitle"] {{ font-size: 16pt; }}

        /* Thin separator, painted with the buttons color */
        QFrame[role="separator"] {{ background-color: {buttons}; }}

        #config_button {{ background-color: {buttons}; color: {text}; }}
        QPushButton, QLineEdit, QComboBox {{ background-color: {buttons}; color: {text}; }}
        #delete_button {{ background-color: {DELETE_COLOR}; color: white; }}
        }}
    """