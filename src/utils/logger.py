# src/utils/logger.py
import logging
import sys

def setup_logger(name="job-radar"):
    """Configures and returns a logger for the project."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Consol output with UTF-8 support
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(name)s]: %(message)s',
            datefmt='%H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Logic for Windows encoding fix if needed
        if sys.platform == "win32":
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except AttributeError:
                pass
                
    return logger

# Global instance for easy access
logger = setup_logger()
