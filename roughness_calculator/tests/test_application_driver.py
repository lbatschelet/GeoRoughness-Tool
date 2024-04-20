import unittest
from roughness_calculator.classes.application_driver import ApplicationDriver


class TestApplicationDriver(unittest.TestCase):
    def setUp(self):
        """Set up test variables."""
        self.input_path = ('/Users/lukasbatschelet/Library/CloudStorage/OneDrive-UniversitaetBern/Studium/FS24/'
                           'Geoprocessing-II/Projektarbeit_Fotogrammetrie/20240415_Grundlagen/202311xx_Rohdaten/'
                           '20231116_DEM_Sammler_Obermad_0.05m.tif')
        self.output_dir = ('/Users/lukasbatschelet/Library/CloudStorage/OneDrive-UniversitaetBern/Studium/FS24/'
                           'Geoprocessing-II/Projektarbeit_Fotogrammetrie/05_Output')

    def test_default_parameters(self):
        """Test the application with default parameters."""
        driver = ApplicationDriver(self.input_path, self.output_dir)
        driver.run()
        # Assertions to verify output

    def test_custom_window_size(self):
        """Test the application with a custom window size."""
        window_size = 0.5
        driver = ApplicationDriver(self.input_path, self.output_dir, window_size=window_size)
        driver.run()
        # Assertions to verify output

    def test_with_thresholds(self):
        """Test the application with categorical thresholds."""
        categorical_thresholds = [0.01, 0.016, 0.02, 0.03, 0.04]
        driver = ApplicationDriver(self.input_path, self.output_dir, categorical_thresholds=categorical_thresholds)
        driver.run()
        # Assertions to verify output

    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()
