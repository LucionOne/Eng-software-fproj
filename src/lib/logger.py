import logging
import os
import sys

def setup_logging(log_file="logs\\DEBUG.log", warning_file="logs\\WARNING.log"):
    """Configures the root logger"""
    os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)
    os.makedirs(os.path.dirname(warning_file) or ".", exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    # Debug file handler
    debug_handler = logging.FileHandler(log_file)
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    # Warning file handler
    warning_handler = logging.FileHandler(warning_file)
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(formatter)

    # Root logger
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers.clear()
    root.addHandler(console)
    root.addHandler(debug_handler)
    root.addHandler(warning_handler)
