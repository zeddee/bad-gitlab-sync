
class RunSummary():
    def __init__(self, success: int=0, warnings: int=0, errors: int=0):
        """Simple object to store number of occurrences
        for these log levels: logging.success, logging.warning, logging.error
        """
        self.success = success
        self.warnings = warnings
        self.errors = errors

    def __str__(self) -> str:
        return f"RunSummary(success:{self.success}, warnings:{self.warnings}, errors:{self.errors})"