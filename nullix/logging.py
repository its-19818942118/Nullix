# nullix/logging.py

import logging

from rich.logging import RichHandler


class Logger:
    """Logger class to configure and provide a logger instance."""

    def __init__(self, name: str = "rich") -> None:
        """Initialize the logger with RichHandler.

        Parameters
        ----------
        name : str
            The name of the logger.
        """
        self.logger = logging.getLogger(name)
        self._configure_logger()

    def _configure_logger(self) -> None:
        """Configure the logger with RichHandler."""
        logging.basicConfig(
            level="INFO",
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler(rich_tracebacks=True)],
        )

    def get_logger(self) -> logging.Logger:
        """Get the configured logger instance.

        Returns
        -------
        logging.Logger
            The configured logger instance.
        """
        return self.logger


if __name__ == "__main__":
    # Test the logger configuration
    test_logger = Logger().get_logger()
    test_logger.info("Logger is configured correctly: %s", "Test message")
