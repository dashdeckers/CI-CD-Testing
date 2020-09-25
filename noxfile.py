"""Noxfile."""
import nox
from nox.sessions import Session

# TODO:

# Use branches and restrict master so its not possible to merge failing
# Put a coverage badge
# Readthedocs generation and xdoctest example testing
### https://cjolowicz.github.io/posts/hypermodern-python-05-documentation/#running-documentation-examples-with-xdoctest  # noqa


# Reuse virtualenvs to allow working offline
nox.options.envdir = ".nox_cache"
nox.options.reuse_existing_virtualenvs = True


# Specify which locations to check
locations = ["src", "tests", "noxfile.py"]


# Specify code linters and arguments
linter_installs = [
    "flake8==3.8.3",
    "flake8-annotations==2.2.1",    # type hints
    "flake8-bandit==2.1.2",         # ?
    "flake8-bugbear==20.1.4",       # ?
    "flake8-docstrings==1.5.0",     # same as pydocstyle
    "flake8-import-order==0.18.1",  # checks for sorted imports
    "darglint==1.5.1",              # checks docs for argument validity etc
    "mccabe==0.6.1",                # code complexity
    "pyflakes==2.2.0",
]
linter_ignores = [f"--ignore={code}" for code in [
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
    "I202",  # 'Additional newline in a group of imports'
]]
linter_args = [
    "--import-order-style=google",
    "--docstring-style=google",
    "--max-complexity=10",
    "--max-line-length=80",
]
linter_excludes = [
    "--exclude=**/*_test.py",
    "--exclude=**/test_*.py",
]


# Specify static type checker and arguments
pytype_installs = [
    "pytype==2020.06.01",
]
pytype_excludes = [
    "--exclude=**/*_test.py",
    "--exclude=**/test_*.py",
]
pytype_args = [
    "--disable=import-error",
]


# Specify test framework and arguments
pytest_installs = [
    "pytest==5.4.3",
    "pytest-cov==2.10.0",
]


@nox.session(python=["3.8"])
def flake8(session: Session) -> None:
    """Lint using flake8.

    Args:
        session (Session): Nox session.
    """
    args = session.posargs or linter_ignores + linter_args + locations

    session.install(*linter_installs)
    session.run("flake8", *args)


@nox.session(python=["3.8"])
def pytype(session: Session) -> None:
    """Do static type checking with pytype.

    Args:
        session (Session): Nox session.
    """
    args = session.posargs or pytype_args + locations

    session.install(*pytype_installs)
    session.run("pytype", *args)


@nox.session(python=["3.6", "3.7", "3.8"])
def pytest(session: Session) -> None:
    """Run tests with PyTest.

    Args:
        session (Session): Nox session.
    """
    session.install(*pytest_installs)
    session.install("-r", "requirements.txt")
    session.run("pytest", "--cov=src/")


def write_setup_cfg() -> None:
    """Write the args to a setup.cfg file.

    This file is useful for telling text-editor linters what to highlight and
    what to ignore.
    """
    with open('setup.cfg', 'w') as setupcfg:
        # Flake8 stuff
        setupcfg.write('\n[flake8]\n')
        for arg in linter_args:
            setupcfg.write(f'{arg[2:]}\n')

        setupcfg.write('ignore=\n')
        for arg in linter_ignores:
            setupcfg.write(f'\t{arg[9:]},\n')

        setupcfg.write('exclude=\n')
        for arg in linter_excludes:
            setupcfg.write(f'\t{arg[10:]},\n')

        # PyType stuff
        setupcfg.write('\n[pytype]\n')
        for arg in pytype_args:
            setupcfg.write(f'{arg[2:]}\n')

        setupcfg.write('exclude=\n')
        for arg in pytype_excludes:
            setupcfg.write(f'\t{arg[10:]},\n')


def write_dev_requirements() -> None:
    """Write the installs to a dev_requirements.txt file.

    Linters and such don't need to be specified in the main requirements file
    because they have nothing to do with the actual requirements of the program
    """
    with open('dev_requirements.txt', 'w') as devreq:
        for package in linter_installs + pytype_installs + pytest_installs:
            devreq.write(f'{package}\n')


write_setup_cfg()
write_dev_requirements()
