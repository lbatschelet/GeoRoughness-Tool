from typing import Final, Optional, List


class Defaults:
    """
    A class used to define default values for the whole package.

    Attributes
    ----------
    OUTPUT_DIR : Optional[str]
        The default output directory. None means the output will be written to the current directory.
    WINDOW_SIZE : float
        The default window size for processing.
    BAND_NUMBER : int
        The default band number to process in the GeoTIFF file.
    HIGH_VALUE_THRESHOLD : float
        The default high value threshold for categorizing data.
    CATEGORY_THRESHOLDS : Optional[List[float]]
        The default category thresholds for categorizing data. None means no categorization will be applied.
    NO_DATA_VALUE : int
        The default value to use for nodata pixels.
    DTYPE : str
        The default data type for the output data.
    DEFAULT_CATEGORY_INCREMENT : float
        The default increment to use when interpolating missing category thresholds.
    LOG_UPDATE_INTERVAL : int
        The default interval for updating the log window.
    """
    OUTPUT_DIR: Final[Optional[str]] = None
    WINDOW_SIZE: Final[float] = 1.0
    BAND_NUMBER: Final[int] = 1
    HIGH_VALUE_THRESHOLD: Final[float] = 10.0
    CATEGORY_THRESHOLDS: Final[Optional[List[float]]] = None
    NO_DATA_VALUE: Final[int] = -9999
    DTYPE: Final[str] = 'float32'
    DEFAULT_CATEGORY_INCREMENT: Final[float] = 0.1
    LOG_UPDATE_INTERVAL: Final[int] = 1000
