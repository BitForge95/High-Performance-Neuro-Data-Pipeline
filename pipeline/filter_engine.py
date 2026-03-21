import numpy as np


class StringFilterEngine:
    """
    A modular engine to parse and apply string-based filters to neuro-data.
    """

    def __init__(self):
        self.supported_operators = [">", "<", ">=", "<=", "=="]

    def apply_filter(self, data_array, filter_string):
        """
        Takes a NumPy array and a string like "signal > 0.4",
        and returns only the data points that match.
        """
        print(f"  -> [FilterEngine] Applying rule: '{filter_string}'")

        # 1. Parse the string (e.g., splitting "signal > 0.4" into parts)
        parts = filter_string.split()
        if len(parts) != 3:
            print(
                "  -> [FilterEngine] Error: Invalid filter format. Use 'variable operator value'."
            )
            return data_array

        operator = parts[1]
        try:
            threshold = float(parts[2])
        except ValueError:
            print("  -> [FilterEngine] Error: Threshold must be a number.")
            return data_array

        # 2. Apply the mathematical filter using NumPy vectorization (Fast!)
        if operator == ">":
            filtered_data = data_array[data_array > threshold]
        elif operator == "<":
            filtered_data = data_array[data_array < threshold]
        else:
            print(f"  -> [FilterEngine] Operator '{operator}' not yet implemented.")
            return data_array

        print(
            f"  -> [FilterEngine] Filtered {len(data_array)} points down to {len(filtered_data)} points."
        )
        return filtered_data
