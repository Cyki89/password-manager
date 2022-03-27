# Colors
BG_PRIMARY = '#262b31'
BG_SECONDARY = '#1b2127'
BG_SECONDARY_HOVER = '#1a1116'
FG_PRIMARY = '#8f9299'
FG_SCONDARY = '#d1d3d6'
COLOR_WHITE  = '#ffffff'
COLOR_BLACK = '#000000'
COLOR_RED = '#ff0000'
COLOR_RED_HOVER = '#dd0000'
COLOR_GREEN = '#00ff00'
COLOR_PRIMARY = '#007bff'
COLOR_PRIMARY_HOVER = '#0069d9'


STYLE_SHEET = f'''
    MainWindow {{
        background-color: {BG_PRIMARY};
        color: {FG_PRIMARY};
    }}

    Label {{
        color: {FG_PRIMARY};
    }}

    NavbarFrame, FooterFrame {{
        background-color: {COLOR_PRIMARY};
    }}

    NavbarLabel, NavbarBrandLabel {{
        color: {COLOR_WHITE};
    }}

    NavbarButton {{
        color: {COLOR_WHITE};
        padding: 15 10; 
        border: none; 
        outline: none;
    }}

    NavbarButton:hover {{
        background: {COLOR_PRIMARY_HOVER};
    }}

    ModalForm, PasswordDataForm {{
        background: {BG_SECONDARY};
        color: {FG_SCONDARY};
    }}

    FormLabel {{
        color: {FG_SCONDARY};
        padding: 10 15 10 0;
    }}

    FormHeader {{
        color: {COLOR_PRIMARY};
    }}

    FormTextInput, #DarkTabTextInput {{
        color: {FG_SCONDARY};
        background: {BG_SECONDARY};
        border: 1 solid {FG_SCONDARY}; 
        padding: 10 10; 
        border-radius: 15;
    }}

    FormTextInput:hover, FormTextInput:focus,
    #DarkTabTextInput:hover, #DarkTabTextInput:focus {{
        background: {BG_SECONDARY_HOVER};
        border: 1 solid {COLOR_PRIMARY};
    }}

    TabTextInput {{
        color: {FG_PRIMARY};
        background: {BG_PRIMARY};
        border: 1 solid {FG_PRIMARY}; 
        padding: 10 10; 
        border-radius: 15;
    }}

    TabTextInput:hover, TabTextInput:focus {{
        background: {BG_SECONDARY};
        border: 1 solid {COLOR_PRIMARY};
    }}

    FormTextOutput {{
        color: {FG_SCONDARY};
        background: {BG_SECONDARY};
        border: 1 solid {COLOR_PRIMARY}; 
        padding: 10 10;
        margin-right: 20;
        border-radius: 15;
    }}

    TabTextOutput {{
        color: {FG_PRIMARY};
        background: {BG_PRIMARY};
        border: 1 solid {COLOR_PRIMARY}; 
        padding: 10 10;
        margin-right: 20;
        border-radius: 15;
    }}

    FormPrimaryButton {{
        color: {FG_SCONDARY};
        background: {COLOR_PRIMARY}; 
        padding: 10 10; 
        border: none;
        border-radius: 26; 
        outline: none;
    }}

    FormPrimaryButton:hover{{
        background: {COLOR_PRIMARY_HOVER};
    }}

    FormApproveButton {{
        color: {FG_SCONDARY};
        background: {COLOR_PRIMARY}; 
        padding: 10 30;
        margin: 5; 
        border: none;
        border-radius: 26; 
        outline: none;
    }}

    FormApproveButton:hover {{
        background: {COLOR_PRIMARY_HOVER};
    }}

    FormCancelButton {{
        color: {FG_SCONDARY};
        background: {COLOR_RED}; 
        padding: 10 30;
        margin: 5; 
        border: none;
        border-radius: 26; 
        outline: none;
    }}

    FormCancelButton:hover {{
        background: {COLOR_RED_HOVER};
    }}


    ErrorBox {{
        color: {COLOR_RED}; 
        padding: 0;
        margin: 0; 
        border: none;
    }}

    SuccessBox {{
        color: {COLOR_GREEN}; 
        padding: 0;
        margin: 0; 
        border: none;
    }}

    CheckBox {{
        color: {FG_SCONDARY}; 
    }}

    TabLabel {{
        color: {FG_SCONDARY};
    }}

    QTabWidget::pane {{
        border: 0;
    }}

    QTabWidget::tab {{
        background: {BG_SECONDARY}; 
        color: {FG_SCONDARY}; 
        padding: 5 10; 
        border-right: 2px solid {COLOR_PRIMARY};
    }}

    QTabBar::tab {{
        background: {BG_SECONDARY}; 
        color: {FG_SCONDARY}; 
    }}

    QTabBar::tab:hover, QTabBar::tab::selected {{
        background: {COLOR_PRIMARY}; 
        color: {COLOR_WHITE};
    }}

    TabHeader {{
        color: {COLOR_WHITE};
    }}

    QTableWidget::item {{
        padding: 20 10;
    }}
    
    QTableWidget {{
        color: {FG_PRIMARY}; 
        background: {BG_PRIMARY};
    }}

    QTableCornerButton::section {{
        background: {COLOR_PRIMARY}; 
    }}

    QHeaderView {{
        background: {BG_PRIMARY};
    }}

    QHeaderView::section {{
        color: {COLOR_WHITE}; 
        background: {COLOR_PRIMARY};
    }}

'''