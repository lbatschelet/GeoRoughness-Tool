from typing import List

import numpy as np
from scipy.optimize import minimize

from roughness_calculator.classes.defaults import Defaults


class ThresholdOptimizer:

    @staticmethod
    def calculate_quality(manual_data: np.ndarray,
                          categorized_calculated_data: np.ndarray,
                          number_of_categories: int
                          ) -> float:
        # Create a mask of the pixels that are actually categorized in both the manual data and the calculated data
        mask = (manual_data != Defaults.NO_DATA_VALUE) & (categorized_calculated_data != Defaults.NO_DATA_VALUE)

        # Apply the mask to the manual data and the calculated data
        masked_manual_data = manual_data[mask]
        masked_categorized_calculated_data = categorized_calculated_data[mask]

        # Calculate the difference between the manual category and the calculated category
        diff = np.abs(masked_manual_data - masked_categorized_calculated_data)

        # Implement an exponential scoring system
        max_diff = number_of_categories - 1
        score = np.exp(-diff / max_diff)

        # Exclude zero scores from the calculation of the quality percentage
        non_zero_scores = score[score != 0]

        # Calculate the quality percentage
        quality_percentage = np.mean(non_zero_scores)

        return quality_percentage

    @staticmethod
    def calculate_optimized_thresholds(manual_data: np.ndarray,
                                       uncategorized_calculated_data: np.ndarray,
                                       category_thresholds: List[float],
                                       ) -> List[float]:
        # Define a loss function that calculates the quality of the categorized data for a given set of thresholds
        def loss_function(thresholds: np.ndarray) -> float:
            categorized_calculated_data = np.digitize(uncategorized_calculated_data, thresholds)
            return -ThresholdOptimizer.calculate_quality(manual_data,
                                                         categorized_calculated_data,
                                                         len(category_thresholds))

        # Convert the list of floats to a numpy array
        category_thresholds_array = np.array(category_thresholds)

        # Use an optimization algorithm to find the thresholds that minimize the loss function
        result = minimize(loss_function, category_thresholds_array, method='Nelder-Mead')

        # Convert the result to a list of floats
        return result.x.tolist()
