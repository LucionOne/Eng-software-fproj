import logging
import sys

def setup_logging(log_file="logs\\DEBUG.log", warning_file="logs\\WARNING.log"):
    """Configures the root logger"""
    formatter = logging.Formatter(
        "%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(warning_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    # Root logger
    root = logging.getLogger()    
    root.setLevel(logging.DEBUG)        
    root.addHandler(console)
    root.addHandler(file_handler)
