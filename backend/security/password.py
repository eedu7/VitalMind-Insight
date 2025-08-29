import bcrypt


class Password:
    @staticmethod
    def hash_password(password: str, rounds: int = 12) -> str:
        """
        Hash a plain-text password using bcrypt.

        Args:
            password (str): The plain-text password to be hashed.
            rounds (int, optional): The cost factor for bcrypt (default=12).
                                    Higher values increase security but slow
                                    performance.

        Returns:
            str: A bcrypt hash of the password (UTF-8 encoded).

        Raises:
            ValueError: If the password is empty or None.
        """

        if not password:
            raise ValueError("Password cannot be empty or None.")

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds))
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify if a plain-text password matches a bcrypt hashed password.

        Args:
            plain_password (str): The plain-text password to check.
            hashed_password (str): The previously hashed password.

        Returns:
            bool: True if the password matches the hash, False otherwise.

        Raises:
            ValueError: If either argument is empty or None.
        """
        if not plain_password or not hashed_password:
            raise ValueError("Passwords cannot be empty or None")
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
