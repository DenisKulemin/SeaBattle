# SeaBattle

## Contest
- [1. Running application locally](#1-running-application-locally)
- [2. Running tests](#2-running-tests)
  - [2.1 Running unit and integration tests](#21-running-unit-and-integration-tests)
  - [2.2 Check coverage](#22-check-coverage)
  - [2.3 Running performance tests](#23-running-performance-tests)
- [3. Code style checker](#3-code-style-checker)

## 1. Running application locally

1) Build docker container:

```commandline
cd docker
docker compose -f compose.yaml build
```

2) Run docker container:

```commandline
docker compose -f compose.yaml run --rm seabattle bash
```

3) Run game:

```commandline
python seabattle/game.py
```

## 2. Running tests

### 2.1 Running unit and integration tests

Before running tests - enter to the seabattle container.

1) Run all tests:

```commandline
pytest
```

Example of report:
```text
platform linux -- Python 3.11.1, pytest-7.2.1, pluggy-1.0.0
rootdir: /home/seabattle
collected 109 items

tests/integration_tests/api_test.py ................................................                      [ 44%]
tests/integration_tests/game_test.py .........                                                            [ 52%]
tests/unit_tests/battlefield_test.py ...................                                                  [ 69%]
tests/unit_tests/bot_test.py .                                                                            [ 70%]
tests/unit_tests/cell_test.py ..                                                                          [ 72%]
tests/unit_tests/player_test.py .......................                                                   [ 93%]
tests/unit_tests/ship_test.py .......                                                                     [100%]

============================================== 109 passed in 3.44s ==============================================
```

2) Run specific tests:

- specific folder with tests:

    ```commandline
    poerty run pytest <path to folder>
    ```

    Example:

    ```commandline
    pytest ./tests/utit_tests
    ```

- specific file with tests:

    ```commandline
    pytest <path to file>
    ```

    Example:

    ```commandline
    pytest ./tests/utit_tests/cell_test.py
    ```

- specific test:

    ```commandline
    pytest <path to file without extension>::<test function name>
    ```

    Example:

    ```commandline
    pytest ./tests/utit_tests/cell_test::test_cell_creation
    ```

### 2.2 Check coverage

1) Run tests with coverage:

```commandline
coverage run -m pytest
```

2) Check the report:

```commandline
coverage report -m
```

Example of report:
```text
Name                                          Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------------------------
seabattle/game.py                                72      0     20      0   100%
seabattle/game_errors/api_errors.py               3      0      0      0   100%
seabattle/game_errors/battlefield_errors.py       7      0      0      0   100%
seabattle/game_errors/game_errors.py              5      0      0      0   100%
seabattle/game_errors/ship_errors.py              4      0      0      0   100%
seabattle/game_objects/1.py                       0      0      0      0   100%
seabattle/game_objects/battlefield.py            68      0     40      0   100%
seabattle/game_objects/bot.py                    31      0     22      0   100%
seabattle/game_objects/cell.py                   17      0      2      0   100%
seabattle/game_objects/player.py                101      0     56      0   100%
seabattle/game_objects/ship.py                   32      0     20      0   100%
seabattle/helpers/constants.py                   24      0      4      0   100%
```

3) If needed, you can add different parameters for coverage module in .coveragerc file.

### 2.3 Running performance tests

Run the tests (use -d option for quiet running):

```commandline
cd docker
docker compose -f compose.yaml -f compose.load_test.yaml -f compose.override_seabattle.yaml up
```

Example of results.

```text
docker-master-1     | 2023-01-27 20:22:24,934 [MainThread] [app: seabattle_load_test] INFO     - seabattle_test.py - _ - line 91 - TEST SUCCEED.
docker-master-1     | [2023-01-27 20:22:24,934] 467de199cf69/INFO/locust.main: Shutting down (exit code 0)
docker-master-1     | Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
docker-master-1     | --------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
docker-master-1     | POST     /enemy-shoot                                                                   15656     0(0.00%) |    170      65     297    170 |  260.94        0.00
docker-master-1     | POST     /exit                                                                            205     0(0.00%) |    155      97     192    160 |    3.42        0.00
docker-master-1     | POST     /game-start                                                                      303     0(0.00%) |    173      95     363    170 |    5.05        0.00
docker-master-1     | POST     /new-game                                                                        304     0(0.00%) |    138      29     420     95 |    5.07        0.00
docker-master-1     | POST     /new-ship                                                                       3035     0(0.00%) |    157      42     360    160 |   50.58        0.00
docker-master-1     | POST     /player-shoot                                                                  14504     0(0.00%) |    169      59     360    170 |  241.74        0.00
docker-master-1     | --------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
docker-master-1     |          Aggregated                                                                     34007     0(0.00%) |    168      29     420    170 |  566.79        0.00
docker-master-1     |
docker-master-1     | Response time percentiles (approximated)
docker-master-1     | Type     Name                                                                                  50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
docker-master-1     | --------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
docker-master-1     | POST     /enemy-shoot                                                                          170    170    180    180    190    200    210    220    250    290    300  15656
docker-master-1     | POST     /exit                                                                                 160    160    170    170    170    180    190    190    190    190    190    205
docker-master-1     | POST     /game-start                                                                           170    170    180    190    230    290    330    340    360    360    360    303
docker-master-1     | POST     /new-game                                                                              95    110    190    210    260    350    400    410    420    420    420    304
docker-master-1     | POST     /new-ship                                                                             160    170    170    180    190    200    230    270    350    360    360   3035
docker-master-1     | POST     /player-shoot                                                                         170    170    180    180    190    200    210    220    250    300    360  14504
docker-master-1     | --------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
docker-master-1     |          Aggregated                                                                            170    170    180    180    190    200    220    230    310    410    420  34007

```

## 3. Code style checker

Using code style based on the
[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
with max line length = 120 characters.
To ensure coding style is OK and to discover typical issues we use [pre-commit](https://pre-commit.com)
for check before committing.

1) Install pre-commit:

```commandline
pip install pre-commit
```

2) Initiate pre-commit:

```commandline
pre-commit install
```

3) Check file/files:

```commandline
pre-commit run --all-files
```

or

```commandline
pre-commit run --files <files>
```

Pre-commit will run automatically every time when you use **git commit** command
(for all added in commit files).
If you need to commit something despite the pre-commit check, use **-n** option (**--no-verify**)
