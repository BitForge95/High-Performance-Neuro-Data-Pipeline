from abc import ABC, abstractmethod


class BaseNeuroLoader(ABC):
    """
    An Abstract Base Class (strict blueprint) for loading massive neuroscience datasets.
    """

    def __init__(self, file_path, dataset_name):
        self.file_path = file_path
        self.dataset_name = dataset_name
        self.is_loaded = False

    def display_info(self):
        print(f"Dataset: {self.dataset_name}")
        print(f"Location: {self.file_path}")
        print(f"Currently Loaded: {self.is_loaded}")

    # 3. Add the abstractmethod decorator
    # This tells Python: "Any child class MUST have a method called load_data, or I will crash."
    @abstractmethod
    def load_data(self):
        pass  # 'pass' just means "do nothing". The child will provide the actual code!
