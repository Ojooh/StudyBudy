



class DetermineState:
    def __init__(self, state):
        self.state  = state
        self.fryp   = ""
        self.fry    = ""
        self.mode   = ""
        self.filt   = ""
        self.folt   = ""

    def determine_order (self):
        if self.state.folder_order == "ASC":
            if self.state.folder_filters == "Last Modified":
                self.fryp    = "last_editted"
            elif self.state.folder_filters == "Last Opened":
                self.fryp = "last_opened"
            else:
                self.fryp = self.state.folder_filters.lower()
        elif self.state.folder_order == "DESC":
            if self.state.folder_filters == "Last Modified":
                self.fryp    = "-last_editted"
            elif self.state.folder_filters == "Last Opened":
                self.fryp = "-last_opened"
            else:
                self.fryp = "-" + self.state.folder_filters.lower()
        if self.state.file_order == "ASC":
            if self.state.file_filters == "Last Modified":
                self.fry = "last_editted"    
            elif self.state.file_filters == "Last Opened":
                self.fry = "last_opened"
            else:
                self.fry = self.state.file_filters.lower()
        elif self.state.file_order == "DESC":
            if self.state.file_filters == "Last Modified":
                self.fry     = "-last_editted"
            elif self.state.file_filters == "Last Opened":
                self.fry = "-last_opened"
            else:
                self.fry = "-" + self.state.file_filters.lower()
        return self.fryp, self.fry


    def determine_mode (self):
        if self.state.mode == "light":
            return "Light-mode"
        elif self.state.mode == "dark":
            return "Dark-mode"

    def determine_tab_filter(self):
        if self.state.folder_filters == "Last Modified":
            self.folt = "last_editted"
        elif self.state.folder_filters == "Last Opened":
            self.folt = "last_opened"
        else:
            self.folt = "last_opened"
        if self.state.file_filters == "Last Modified":
            self.filt = "last_editted"
        elif self.state.file_filters == "Last Opened":
            self.filt = "last_opened"
        else:
            self.filt = "last_editted"

        return self.filt, self.folt
        
