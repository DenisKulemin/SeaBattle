"""Module contains load test for seabattle endpoints."""
import random
from locust import HttpUser, task, between, events

SHIPS_COORDINATES = (
    [[10, 1], [10, 2], [10, 3], [10, 4]],
    [[10, 6], [10, 7], [10, 8]],
    [[1, 2], [2, 2], [3, 2]],
    [[8, 1], [8, 2]],
    [[8, 5], [8, 6]],
    [[8, 8], [8, 9]],
    [[6, 1]],
    [[6, 3]],
    [[6, 5]],
    [[6, 7]]
)

COORDINATES_FOR_SHOOTING = [[x, y] for x in range(1, 11) for y in range(1, 11)]


class SeabattleUser(HttpUser):
    """Class contains load tests for seabattle endpoints."""
    wait_time = between(1, 1)

    @task(1)
    def test_game(self):
        """Method tests the whole seabattle game throw its endpoints."""
        response = self.client.post("/new-game")
        game_info = response.json()
        game_info.pop("message")

        for ship_coordinates in SHIPS_COORDINATES:
            _ = self.client.post("/new-ship", json={**game_info, "coordinates": ship_coordinates})

        result = self.client.post("/game-start", json=game_info)
        result = result.json()
        is_player_move = result["isPlayerMove"]

        coordinates_for_shooting = [
            [x, y] for x in range(1, 11)
            for y in range(1, 11)
        ]
        is_game_over = False
        while coordinates_for_shooting and not is_game_over:
            if is_player_move:
                coordinate_for_shooting = random.choice(coordinates_for_shooting)
                result = self.client.post("/player-shoot",
                                          json={**game_info, "coordinate": coordinate_for_shooting}).json()
                is_player_move = result["isPlayerMove"]
                is_game_over = result["isGameOver"]
                for coordinate in result["coordinates"]:
                    if coordinate in coordinates_for_shooting:
                        coordinates_for_shooting.remove(coordinate)
            else:
                result = self.client.post("/enemy-shoot", json=game_info).json()
                is_player_move = result["isPlayerMove"]
                is_game_over = result["isGameOver"]

        _ = self.client.post("/exit", json=game_info)


@events.quitting.add_listener
def _(environment, **kwargs):
    # pylint: disable=unused-argument

    """Method checks load test stats and change exit code if any of stats out of range."""
    fail_ratio = 0.01
    average_response_time = 300
    percentile = 0.95
    response_time_percentile_time = 600

    if environment.stats.total.fail_ratio > fail_ratio:
        print(f"Test failed due to failure ration > {fail_ratio * 100}%.")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > average_response_time:
        print(f"Test failed due to average response time > {average_response_time} ms.")
        environment.process_exit_code = 1
    elif environment.stats.total.get_response_time_percentile(percentile) > response_time_percentile_time:
        print(f"Test failed due to 95th percentile response time > {response_time_percentile_time} ms.")
        environment.process_exit_code = 1
    else:
        print("TEST SUCCEED.")
        environment.process_exit_code = 0
