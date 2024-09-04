# nullix/utils/detector.py

from typing import Optional

import distro

from nullix.logging import Logger

logger = Logger().get_logger()


class DistroDetector:
    """
    Class to detect the Linux distribution.

    This class provides a static method to detect the current Linux distribution
    using the `distro` library.

    Methods
    -------
    detect() : Optional[str]
        Detect the current Linux distribution.
    """

    @staticmethod
    def detect() -> Optional[str]:
        """
        Detect the current Linux distribution.

        This method attempts to identify the Linux distribution by first checking
        the distribution family using `distro.like()`. If that's empty or None,
        it falls back to using `distro.id()`.

        Returns
        -------
        Optional[str]
            The name of the detected Linux distribution, or None if not detected.

        Notes
        -----
        The detection process prioritizes the distribution family (from `distro.like()`)
        over the specific distribution ID (from `distro.id()`). This approach helps in
        identifying the broader distribution family, which can be useful for compatibility
        checks or system-specific operations.

        If `distro.like()` returns a space-separated list, only the first item is used.

        Examples
        --------
        >>> DistroDetector.detect()
        'ubuntu'

        >>> DistroDetector.detect()
        'fedora'

        >>> DistroDetector.detect()
        None
        """
        distro_like = distro.like().lower()
        distro_id = distro.id().lower()

        logger.debug("Detected distro.like(): %s", distro_like)
        logger.debug("Detected distro.id(): %s", distro_id)

        if distro_like and distro_like.strip():
            # Use the first item in distro_like if it's a space-separated list
            detected = distro_like.split()[0].lower()
        elif distro_id:
            detected = distro_id.lower()
        else:
            logger.warning("Unable to detect Linux distribution")
            return None

        logger.info("Detected distribution: %s", detected)
        return detected


if __name__ == "__main__":
    detected_distro = DistroDetector.detect()
    print(f"Detected distribution: {detected_distro or 'Unknown'}")
