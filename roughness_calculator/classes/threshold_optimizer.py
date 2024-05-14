from typing import List, Optional

import numpy as np
import logging

from roughness_calculator.classes.defaults import Defaults

logger = logging.getLogger(__name__)


class ThresholdOptimizer:

    @staticmethod
    def calculate_quality(manual_data: np.ndarray,
                          categorized_calculated_data: np.ndarray,
                          thresholds: List[float],
                          ) -> float:
        """
        Calculates the quality of categorization based on a comparison of manual and categorized calculated data.
        Each data point is classified into a category based on provided thresholds, and the method evaluates how well the
        categorized data matches the manual data.

        Args:
            manual_data (np.ndarray): An array of manually categorized data.
            categorized_calculated_data (np.ndarray): An array of automatically derived raw data values.
            thresholds (List[float]): A list of thresholds that define the boundaries between categories.

        Returns:
            float: The quality percentage, representing the average scoring across the data, where the scoring penalizes
            differences between manual and calculated categorizations more severely as the difference increases.
        """
        if not thresholds:
            logging.error("Thresholds list is empty or not properly defined.")
            raise ValueError("Thresholds list must be non-empty and properly defined.")

            # Ensure thresholds are a NumPy array with a float type
        if not isinstance(thresholds, np.ndarray):
            thresholds = np.array(thresholds, dtype=float)

        valid_mask = (manual_data != Defaults.NO_DATA_VALUE) & (categorized_calculated_data != Defaults.NO_DATA_VALUE)
        if not np.any(valid_mask):
            logging.error("No valid data available after excluding NO_DATA_VALUE.")
            raise ValueError("No valid data available after filtering.")

        valid_manual_data = manual_data[valid_mask]
        valid_calculated_data = categorized_calculated_data[valid_mask]

        # Digitize calculated data into categories based on thresholds
        try:
            calculated_categories = np.digitize(valid_calculated_data, thresholds, right=True)
        except Exception as e:
            logging.error(f"Error in digitizing data: {str(e)}")
            raise

        diff = np.abs(valid_manual_data - calculated_categories)
        score = np.exp(-diff)  # Exponential decay for scoring differences
        quality_percentage = np.mean(score)
        logging.info(f"Calculated quality percentage: {quality_percentage}%")

        return quality_percentage

    @staticmethod
    def calculate_optimized_thresholds(manual_data: np.ndarray,
                                       uncategorized_calculated_data: np.ndarray,
                                       number_of_categories: int) -> List[Optional[float]]:
        """
        Calculates optimized thresholds for categorization based on training and uncategorized data,
        addressing cases where initial categories might be missing.

        Args:
            manual_data (np.ndarray): Array of category identifiers from training data.
            uncategorized_calculated_data (np.ndarray): Array of corresponding raw values to categorize.
            number_of_categories (int): Total number of expected categories.

        Returns:
            List[Optional[float]]: Calculated thresholds between categories. None values indicate uncomputable thresholds.

        Raises:
            ValueError: If input data arrays are empty or if `number_of_categories` is less than 2.
        """
        if manual_data.size == 0 or uncategorized_calculated_data.size == 0:
            logging.error("Input data arrays cannot be empty.")
            raise ValueError("Input data arrays cannot be empty.")

        if number_of_categories < 2:
            logging.error("At least two categories are required to calculate thresholds.")
            raise ValueError("At least two categories are required to calculate thresholds.")

        valid_data_mask = manual_data != Defaults.NO_DATA_VALUE
        filtered_manual_data = manual_data[valid_data_mask]
        filtered_uncategorized_data = uncategorized_calculated_data[valid_data_mask]

        if filtered_manual_data.size == 0:
            logging.error("No valid data available after filtering out NO_DATA_VALUE.")
            raise ValueError("No valid data available after filtering out NO_DATA_VALUE.")

        # Initialize storage for category values
        category_values = {i: [] for i in range(number_of_categories)}
        for category in np.unique(filtered_manual_data):
            if category >= number_of_categories:
                continue  # Skip categories outside the expected range
            mask = filtered_manual_data == category
            category_values[category].extend(filtered_uncategorized_data[mask])
            logging.info(f"Category {category} gathered with {len(category_values[category])} entries.")

        # Prepare list for thresholds with initial None values
        thresholds = [None] * (number_of_categories - 1)

        # Handling the first threshold
        if category_values.get(0):  # Check if category 0 has data
            if category_values.get(1):  # And category 1 also has data
                current_95th_percentile = np.percentile(category_values[0], 95)
                next_5th_percentile = np.percentile(category_values[1], 5)
                thresholds[0] = (current_95th_percentile + next_5th_percentile) / 2
                logging.info("First threshold set at {thresholds[0]} using data from categories 0 and 1.")
            else:  # If category 0 has data but category 1 does not
                thresholds[0] = np.percentile(category_values[0], 95)
                logging.info("First threshold set at {thresholds[0]} using data from category 0 only.")
        elif category_values.get(1):  # No data in category 0, data in category 1
            min_value = np.min(category_values[1])
            thresholds[0] = max(min_value / 2, 0)  # Safeguard against negative threshold
            logging.info(f"First threshold set at {thresholds[0]} using data from category 1 only.")
        else:
            logging.warning("No data available for categories 0 and 1. First threshold not yet calculated.")

        # Calculate thresholds for the rest of the categories with available data
        for i in range(1, number_of_categories - 1):
            if category_values.get(i) and category_values.get(i + 1):
                next_5th_percentile = np.percentile(category_values[i + 1], 5)
                current_95th_percentile = np.percentile(category_values[i], 95)
                thresholds[i] = (next_5th_percentile + current_95th_percentile) / 2
                logging.info(f"Threshold between categories {i} and {i + 1} set at {thresholds[i]}.")

        # Interpolate missing thresholds where necessary
        for i in range(len(thresholds)):
            if thresholds[i] is None:
                thresholds[i] = ThresholdOptimizer.interpolate_thresholds(thresholds, i)
                logging.info(f"Interpolated threshold at index {i} set to {thresholds[i]} if applicable.")

        return thresholds

    @staticmethod
    def interpolate_thresholds(thresholds: List[Optional[float]], index: int) -> Optional[float]:
        """
        Interpolates a missing threshold using adjacent values, ensuring the interpolated value is non-negative.

        Args:
            thresholds (List[Optional[float]]): The current list of thresholds, some of which may be None.
            index (int): The index of the threshold to interpolate.

        Returns:
            Optional[float]: The interpolated threshold value, or None if it cannot be interpolated.

        Note:
            This method assumes there are valid thresholds available on either side of the missing value for interpolation.
        """
        prev = next = None
        # Search for the nearest non-None value to the left
        for j in range(index - 1, -1, -1):
            if thresholds[j] is not None:
                prev = thresholds[j]
                break
        # Search for the nearest non-None value to the right
        for k in range(index + 1, len(thresholds)):
            if thresholds[k] is not None:
                next = thresholds[k]
                break

        # Log the found values for debugging
        logging.info(f"Interpolating at index {index}: found previous threshold {prev}, next threshold {next}")

        # Calculate interpolated value
        if prev is not None and next is not None:
            interpolated_value = max((prev + next) / 2, 0)
            logging.info(f"Interpolated value between {prev} and {next} is {interpolated_value}")
            return interpolated_value
        elif prev is not None:
            interpolated_value = max(prev + Defaults.DEFAULT_CATEGORY_INCREMENT, 0)
            logging.info(f"Only previous threshold available, incremented value is {interpolated_value}")
            return interpolated_value
        elif next is not None:
            interpolated_value = max(next - Defaults.DEFAULT_CATEGORY_INCREMENT, 0)
            logging.info(f"Only next threshold available, decremented value is {interpolated_value}")
            return interpolated_value

        # Log and handle cases where interpolation is not possible
        logging.error("Unable to interpolate threshold: no adjacent thresholds available.")
        return None  # Return None if no valid interpolation is possible

