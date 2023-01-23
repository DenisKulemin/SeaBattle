"""Module contains validation schemas for checking api input ana output data."""
import inflection
from marshmallow import Schema, fields as ma_fields, post_dump, validate


def camelaze(param):
    """This method converts marshmallow fields to camel case."""
    return inflection.camelize(param, False)


class InputSchema(Schema):
    """
    Class validation schema, that use snake case names for internal work and camel case for external.
    Used for validation input data in requests.
    """

    def on_bind_field(self, field_name: str, field_obj: ma_fields.Field) -> None:
        """Method for snake/camel cases matching."""
        field_obj.data_key = camelaze(field_obj.data_key or field_name)


class OutputSchema(Schema):
    """
    Class validation schema, that use snake case names for internal work but returns camel case names after dump.
    Used for validation output data in requests.
    """

    @post_dump
    def camelize_keys(self, in_data: dict, **kwargs) -> dict:
        # pylint: disable=unused-argument
        # **kwargs needed for correct work post_dump decorator.

        """
        Method that convert snake case keys into camel case keys.
        Args:
            in_data: Dictionary with dumped data.

        Returns:
            dict: Dictionary with keys in camel case.
        """
        return {camelaze(key): value for key, value in in_data.items()}


class CreateNewGameOutputSchema(OutputSchema):
    """Class for validation '/new-game' response."""
    game_id = ma_fields.UUID(required=True)
    player_id = ma_fields.UUID(required=True)
    message = ma_fields.Str(required=True)


class GameStartInputSchema(InputSchema):
    """Class for validation '/game-start' input."""
    game_id = ma_fields.UUID(required=True)
    player_id = ma_fields.UUID(required=True)


class GameStartOutputSchema(OutputSchema):
    """Class for validation '/game-start' output."""
    game_id = ma_fields.UUID(required=True)
    player_id = ma_fields.UUID(required=True)
    is_player_move = ma_fields.Bool(required=True)
    message = ma_fields.Str(required=True)


class CoordinateSchema(Schema):
    """Class for validation pair of coordinates."""
    x = ma_fields.Int(required=True, validate=validate.Range(min=1, max=10))
    y = ma_fields.Int(required=True, validate=validate.Range(min=1, max=10))


class CreateNewShipInputSchema(InputSchema):
    """Class for validation '/new-ship' input."""
    game_id = ma_fields.UUID(required=True)
    player_id = ma_fields.UUID(required=True)
    coordinates = ma_fields.List(
        ma_fields.Tuple(
            (ma_fields.Int(required=True, validate=validate.Range(min=1, max=10)),
             ma_fields.Int(required=True, validate=validate.Range(min=1, max=10))),
            required=True),
        required=True
    )


class CreateNewShipOutputSchema(OutputSchema):
    """Class for validation '/new-ship' output."""
    game_id = ma_fields.UUID(required=True)
    player_id = ma_fields.UUID(required=True)
    coordinates = ma_fields.List(
        ma_fields.List(ma_fields.Int(required=True, validate=validate.Range(min=1, max=10)), required=True),
        required=True
    )
    message = ma_fields.Str(required=True)


class PlayerShootInputSchema(InputSchema):
    """Class for validation '/player-shoot' input."""
    game_id = ma_fields.UUID(required=True)
    player_id = ma_fields.UUID(required=True)
    coordinate = ma_fields.Tuple(
        (ma_fields.Int(required=True, validate=validate.Range(min=1, max=10)),
         ma_fields.Int(required=True, validate=validate.Range(min=1, max=10))),
        required=True
    )


class PlayerShootOutputSchema(OutputSchema):
    """Class for validation '/player-shoot' output."""
    game_id = ma_fields.UUID(required=True)
    player_id = ma_fields.UUID(required=True)
    coordinates = ma_fields.List(
        ma_fields.List(ma_fields.Int(required=True, validate=validate.Range(min=1, max=10)), required=True),
        required=True
    )
    shooting_results = ma_fields.List(ma_fields.Str(required=True), required=True)
    is_killed = ma_fields.Bool(required=True)
    is_player_move = ma_fields.Bool(required=True)
    is_game_over = ma_fields.Bool(required=True)


class EnemyShootInputSchema(InputSchema):
    """Class for validation '/enemy-shoot' input."""
    game_id = ma_fields.UUID(required=True)
    player_id = ma_fields.UUID(required=True)


class EnemyShootOutputSchema(OutputSchema):
    """Class for validation '/enemy-shoot' output."""
    game_id = ma_fields.UUID(required=True)
    player_id = ma_fields.UUID(required=True)
    coordinates = ma_fields.List(
        ma_fields.List(ma_fields.Int(required=True, validate=validate.Range(min=1, max=10)), required=True),
        required=True
    )
    shooting_results = ma_fields.List(ma_fields.Str(required=True), required=True)
    is_killed = ma_fields.Bool(required=True)
    is_player_move = ma_fields.Bool(required=True)
    is_game_over = ma_fields.Bool(required=True)
