"""Module contains game error classes."""


class GameError(Exception):
    """Base game error class."""


class NotStartedGameError(GameError):
    """Raises if we request an action, that cannot be made before game started."""


class StartedGameError(GameError):
    """Raises if we request an action, that cannot be made after game started."""


class NotYourTurnError(GameError):
    """Raises if someone shoots when it's not their turn."""


class GameOverError(GameError):
    """Raises if player try to do anything after game is over."""
