from typing import List

import numpy as np

from roughness_calculator.classes.defaults import Defaults


class ThresholdOptimizer:

    @staticmethod
    def calculate_quality(manual_data: np.ndarray,
                          categorized_calculated_data: np.ndarray,
                          thresholds: List[float],
                          ) -> float:
        """
        Calculates the quality of categorization based on a comparison of manual and categorized calculated data.

        Args:
            manual_data (np.ndarray): An array of manually categorized data.
            categorized_calculated_data (np.ndarray): An array of automatically categorized data.
            thresholds (List[float]): A list of thresholds that define the boundaries between categories.

        Returns:
            float: The quality percentage, representing the average scoring across the data, where the scoring penalizes
            differences between manual and calculated categorizations more severely as the difference increases.
        """
        # Create a mask of the pixels that are actually categorized in both the manual data and the calculated data
        mask = (manual_data != Defaults.NO_DATA_VALUE) & (categorized_calculated_data != Defaults.NO_DATA_VALUE)

        # Apply the mask to the manual data and the calculated data
        masked_manual_data = manual_data[mask]
        masked_categorized_calculated_data = categorized_calculated_data[mask]

        # Calculate the absolute difference between the manual category and the calculated category
        diff = np.abs(masked_manual_data - masked_categorized_calculated_data)

        # Using a quadratic error to penalize larger errors more heavily
        score = 1 - (diff ** 2 / (len(thresholds) - 1) ** 2)

        # Calculate the quality percentage, including all points
        quality_percentage = np.mean(score)

        return quality_percentage

    @staticmethod
    def calculate_optimized_thresholds(manual_data: np.ndarray,
                                       uncategorized_calculated_data: np.ndarray,
                                       number_of_categories: int
                                       ) -> List[float]:
        """
        Suggests optimized thresholds for categorization based on training data and uncategorized calculated data.
        It uses percentiles to minimize the influence of outliers and ensures a more robust
        categorization threshold setting.

        Args:
            manual_data (np.ndarray): An array where each element is a category identifier for training data.
            uncategorized_calculated_data (np.ndarray): An array of raw values associated with each training data point.
            number_of_categories (int): The total number of categories including both ends of the value spectrum.

        Returns:
            List[float]: A list of calculated thresholds that define the boundaries between categories, aimed to
            minimize misclassification.
        """
        # Initialize a dictionary to store the values for each category
        category_values = {i: [] for i in range(number_of_categories)}

        # Gather values for each category based on the manual data
        for category in range(number_of_categories):
            mask = manual_data == category
            category_values[category].extend(uncategorized_calculated_data[mask])

        # Compute bounds for each category using percentiles
        thresholds = []
        for i in range(number_of_categories):
            if category_values[i]:  # Ensure there are values to process
                if i == 0:
                    # Calculate the first threshold as a logical point between the lowest value of the first category and zero
                    min_value = np.min(category_values[i])
                    thresholds.append(
                        min_value / 2)  # Example: midpoint between zero and the minimum value of the first category
                if i < number_of_categories - 1:
                    # Calculate the next threshold as the average of the 95th percentile of the current category and the
                    # 5th percentile of the next category
                    next_5th_percentile = np.percentile(category_values[i + 1], 5)
                    current_95th_percentile = np.percentile(category_values[i], 95)
                    thresholds.append((next_5th_percentile + current_95th_percentile) / 2)

        # Calculate the top threshold as a point above the maximum value of the last category
        if category_values[number_of_categories - 1]:
            max_value_last_category = np.max(category_values[number_of_categories - 1])
            # Assume the dataset's maximum value as a logical upper bound, e.g., 110% of the maximum observed value
            logical_upper_bound = max_value_last_category * 1.1
            thresholds.append(logical_upper_bound)

        return thresholds
