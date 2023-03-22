"""Module contains validation schemas for checking api input ana output data."""
import inflection
from marshmallow import Schema, fields as ma_fields, validate, pre_load


def camelaze(param):
    """This method converts marshmallow fields to camel case."""
    return inflection.camelize(param, False)


class InputSchema(Schema):
    """
    Class validation schema, that use snake case names for internal work and camel case for external
    (load camel case names and turn into snake case for further processing in game).
    After validation returns SNAKE case keys.
    Used for validation input data in requests.
    """

    def on_bind_field(self, field_name: str, field_obj: ma_fields.Field) -> None:
        """Method for snake/camel cases matching."""
        field_obj.data_key = camelaze(field_obj.data_key or field_name)


class OutputSchema(InputSchema):
    """
    Class validation schema, that use snake case names for internal work and camel case for external
    (load snake case names and turn into camel case for returning the client).
    After validation returns CAMEL case keys.
    Used for validation output data in requests.
    """

    @pre_load
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


class CellSchema(OutputSchema):
    """Class for validation coordinates and cell sings in responses."""
    x = ma_fields.Int(required=True, validate=validate.Range(min=1, max=10, min_inclusive=True, max_inclusive=True))
    y = ma_fields.Int(required=True, validate=validate.Range(min=1, max=10, min_inclusive=True, max_inclusive=True))
    sign = ma_fields.Str(required=True)


class FleetStructureSchema(OutputSchema):
    """Class for validation fleet structure response."""
    patrol_boat = ma_fields.Int(required=True,
                                validate=validate.Range(min=0, max=4, min_inclusive=True, max_inclusive=True))
    submarine = ma_fields.Int(required=True,
                              validate=validate.Range(min=0, max=3, min_inclusive=True, max_inclusive=True))
    destroyer = ma_fields.Int(required=True,
                              validate=validate.Range(min=0, max=2, min_inclusive=True, max_inclusive=True))
    battleship = ma_fields.Int(required=True,
                               validate=validate.Range(min=0, max=1, min_inclusive=True, max_inclusive=True))


class CreateGameInfoOutputSchema(OutputSchema):
    """Class for validation responses with game information."""
    game_id = ma_fields.UUID(required=True)
    player_id = ma_fields.UUID(required=True)
    is_player_move = ma_fields.Bool(required=True)
    is_game_over = ma_fields.Bool(required=True)
    player_battle_field_cells = ma_fields.Nested(CellSchema(many=True), required=True)
    player_fleet = ma_fields.Nested(FleetStructureSchema(), required=True)
    enemy_battle_field_cells = ma_fields.Nested(CellSchema(many=True), required=True)
    enemy_fleet = ma_fields.Nested(FleetStructureSchema(), required=True)
    winner = ma_fields.Str(required=True)


class GameStartInputSchema(InputSchema):
    """Class for validation '/game-start' input."""
    game_id = ma_fields.UUID(required=True)
    player_id = ma_fields.UUID(required=True)


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
    player_ship_cells = ma_fields.Nested(CellSchema(many=True), required=True)
    player_fleet = ma_fields.Nested(FleetStructureSchema(), required=True)


class PlayerShootInputSchema(InputSchema):
    """Class for validation '/player-shoot' input."""
    game_id = ma_fields.UUID(required=True)
    player_id = ma_fields.UUID(required=True)
    coordinate = ma_fields.Tuple(
        (ma_fields.Int(required=True, validate=validate.Range(min=1, max=10)),
         ma_fields.Int(required=True, validate=validate.Range(min=1, max=10))),
        required=True
    )


class EnemyShootInputSchema(InputSchema):
    """Class for validation '/enemy-shoot' input."""
    game_id = ma_fields.UUID(required=True)
    player_id = ma_fields.UUID(required=True)
