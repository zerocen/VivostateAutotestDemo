import os


class DataPathManager:
    project_dir = None
    api_data_dir = None
    page_data_dir = None
    log_dir = None

    def __init__(self):
        self.project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.api_data_dir = os.path.join(f"{self.project_dir}", "data", "api")
        self.page_data_dir = os.path.join(f"{self.project_dir}", "data", "page")
        self.log_dir = os.path.join(f"{self.project_dir}", "logs")


data_path_manager = DataPathManager()
