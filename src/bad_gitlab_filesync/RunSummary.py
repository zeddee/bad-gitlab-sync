
class RunSummary():
    def __init__(self, success: int=0, warnings: int=0, errors: int=0):
        """Simple object to store number of occurrences
        for these states:

        - `success`: When we've successfully retrieved and written a file.
        - `warning`: A handled failure. Where we want to let the rest of
          the script run, but warn that a failure has occurred.
        - `error`: Errors. Technically, is never used as all errors currently
          trigger an exception (except where they're handled as `warning`s),
          so there is no opportunity to print the RunSummary.
        """
        self.success = success
        self.warnings = warnings
        self.errors = errors

    def __str__(self) -> str:
        return f"RunSummary(success:{self.success}, warnings:{self.warnings}, errors:{self.errors})"