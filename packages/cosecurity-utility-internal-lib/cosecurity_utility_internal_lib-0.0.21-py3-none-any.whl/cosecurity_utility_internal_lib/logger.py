import logging

from typing import Any


def create_logger(obj:Any):
    """
    Method to create a log manager

    Parameters:
        obj (Any): source object

    Returns:
        np.ndarray: return the specific logger for the object passed via parameter
    """
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    return logging.getLogger(type(obj).__name__)
