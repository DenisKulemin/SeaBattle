# SeaBattle

## Code style checker

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
