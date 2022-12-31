# SeaBattle

## Contest
- [1. Running application locally](#1-running-application-locally)
- [2. Running tests](#2-running-tests)
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

1) Run all tests:

```commandline
pytest
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
