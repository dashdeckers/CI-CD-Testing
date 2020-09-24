"""Noxfile."""
import nox
from nox.sessions import Session

# Reuse virtualenvs to allow working offline
nox.options.envdir = ".nox_cache"
nox.options.reuse_existing_virtualenvs = True

# Specify which locations to check
locations = ["src", "tests", "noxfile.py"]

# TODO:

# Readthedocs generation and xdoctest example testing
### https://cjolowicz.github.io/posts/hypermodern-python-05-documentation/#running-documentation-examples-with-xdoctest  # noqa

# View layer (ST3) likes .cfg (find a way to derive it from noxfile)
# Check layer (nox) is fine (could do with a git prehook tho)
# CI/CD layer (GitHub) is fine (does the push still push tho? branches?)

# Make the pip installs somehow easily accessible
# Make the args easily accessible --> setup.cfg


@nox.session(python=["3.8"])
def flake8(session: Session) -> None:
    """Lint using flake8.

    Args:
        session (Session): Nox session.
    """
    linters = (
        "flake8==3.8.3",
        "flake8-annotations==2.2.1",    # type hints
        "flake8-bandit==2.1.2",         # ?
        "flake8-bugbear==20.1.4",       # ?
        "flake8-docstrings==1.5.0",     # same as pydocstyle
        "flake8-import-order==0.18.1",  # checks for sorted imports
        "darglint==1.5.1",              # checks docs for argument validity etc
        "mccabe==0.6.1",                # code complexity
        "pyflakes==2.2.0",
    )

    docstring_args = [f"--ignore={code}" for code in [
        "D100",  # 'Missing docstring in ... public module'
        # "D101",  # '... public class'
        # "D102",  # '... public method'
        # "D103",  # '... public function'
        # "D104",  # '... public package'
        # "D105",  # '... magic method'
        "D106",  # '... public nested class'
        "D107",  # '... __init__'
        "D202",  # 'No blank lines allowed after function docstring'
        "D203",  # '1 blank line required before class docstring'
        "D213",  # 'Multi-line docstrings should start at the second line'
        "D415",  # 'First line should end with one of [".", "?", "!"]'
    ]]

    other_args = [
        "--import-order-style=google",
        "--docstring-style=google",
        "--max-complexity=10",
        "--max-line-length=80",

        "--ignore=I202",  # Temporary
    ]

    args = session.posargs or docstring_args + other_args + locations

    session.install(*linters)
    session.run("flake8", *args)


@nox.session(python=["3.8"])
def pytype(session: Session) -> None:
    """Do static type checking with pytype.

    Args:
        session (Session): Nox session.
    """
    pytype_args = [
        "--disable=import-error",
        "--exclude=**/*_test.py",
        "--exclude=**/test_*.py",
    ]
    args = session.posargs or pytype_args + locations

    session.install("pytype==2020.06.01")
    session.run("pytype", *args)


@nox.session(python=["3.6", "3.7", "3.8"])
def pytest(session: Session) -> None:
    """Run tests with PyTest.

    Args:
        session (Session): Nox session.
    """
    session.install("pytest==5.4.3", "pytest-cov==2.10.0")
    session.install("-r", "requirements.txt")
    session.run("pytest", "--cov=src/")
