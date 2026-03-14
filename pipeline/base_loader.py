class BaseNeuroLoader:
    """
    A bluprint for loading massive neuroscience datasets
    """

    # The init method sets up the object when it is created
    def __init__(self, file_path, dataset_name):
        # We are storing the inputs inside the object using self
        self.file_path = file_path
        self.dataset_name = dataset_name
        self.is_loaded = False  # We are setting this false as by default the dataset is not loaded yet

    def display_info(self):
        print(f"Dataset: {self.dataset_name}")
        print(f"Location : {self.file_path}")
        print(f"Currently Loaded : {self.is_loaded}")

    def load_data(self):
        print(f"Loading generic data from {self.file_path}")
