"""Noxfile."""
import nox
from nox.sessions import Session

# Reuse virtualenvs to allow working offline
nox.options.envdir = '.nox_cache'
nox.options.reuse_existing_virtualenvs = True


# Specify which locations to check
locations = ['src', 'tests', 'noxfile.py', 'docs/conf.py']


# Specify the code linter frameworks and arguments
linter_installs = [
    'flake8==3.8.3',
    'flake8-annotations==2.2.1',    # type hints
    'flake8-bandit==2.1.2',         # ?
    'flake8-bugbear==20.1.4',       # ?
    'flake8-docstrings==1.5.0',     # same as pydocstyle
    'flake8-import-order==0.18.1',  # checks for sorted imports
    'darglint==1.5.1',              # checks docs for argument validity etc
    'mccabe==0.6.1',                # code complexity
    'pyflakes==2.2.0',
]
linter_ignores = [
    'D202',  # 'No blank lines allowed after function docstring'
    'D203',  # '1 blank line required before class docstring'
    'D213',  # 'Multi-line docstrings should start at the second line'
    'D415',  # 'First line should end with one of ['.', '?', '!']'
    'I202',  # 'Additional newline in a group of imports'
    'I001',  # 'Import in the wrong position'
    'I003',  # 'Expected 1 blank line in imports, found 0'
    'I004',  # 'Unexpected blank line in imports'
    'I100',  # 'Import statements are in the wrong order'
    'W503',  # 'line break before operator'
]
linter_excludes = [
    '**/*_test.py',
    '**/test_*.py',
]
linter_args = [
    '--config=ignore',
    '--import-order-style=google',
    '--docstring-style=google',
    '--max-complexity=10',
    '--max-line-length=80',
]


# Specify the static type checker frameworks and arguments
pytype_installs = [
    'pytype==2020.06.01',
]
pytype_excludes = [
    '**/*_test.py',
    '**/test_*.py',
]
pytype_args = [
    '--disable=import-error',
]


# Specify the testing frameworks and arguments
test_installs = [
    'xdoctest==0.15.0',
    'pygments==2.7.1',
    'pytest==5.4.3',
    'pytest-cov==2.10.0',
]


# Specify the docs generation framework and arguments
docs_installs = [
    'sphinx==3.2.1',
    'sphinx-autodoc-typehints==1.11.0',
]


@nox.session(python=['3.8'])
def lint(session: Session) -> None:
    """Lint using flake8.

    Args:
        session (Session): Nox session.
    """
    args = session.posargs or (
        ['--ignore=' + ','.join(linter_ignores)]
        + ['--exclude=' + ','.join(linter_excludes)]
        + linter_args
        + locations
    )

    session.install(*linter_installs)
    session.run('flake8', *args)


@nox.session(python=['3.8'])
def typecheck(session: Session) -> None:
    """Do static type checking with pytype.

    Args:
        session (Session): Nox session.
    """
    args = session.posargs or (
        ['--exclude=' + ','.join(pytype_excludes)]
        + pytype_args
        + locations
    )

    session.install(*pytype_installs)
    session.run('pytype', *args)


@nox.session(python=['3.6', '3.7', '3.8'])
def test(session: Session) -> None:
    """Run tests with PyTest and XDoctest.

    Args:
        session (Session): Nox session.
    """
    args = session.posargs or locations

    session.install(*test_installs)
    session.run('python', '-m', 'xdoctest', *args)

    session.install('-r', 'requirements.txt')
    session.run('python', '-m', 'pytest', '--cov=src/', '--cov-fail-under=80')


@nox.session(python=['3.8'])
def coverage(session: Session) -> None:
    """Upload coverage data to CodeCov.

    Args:
        session (Session): Nox session.
    """
    session.install('coverage', 'codecov')
    session.run('coverage', 'xml', '--fail-under=0')
    session.run('codecov', *session.posargs)


@nox.session(python=['3.8'])
def docs(session: Session) -> None:
    """Build the documentation with Sphinx.

    Args:
        session (Session): Nox session.
    """
    session.install(*docs_installs)
    session.install('-r', 'requirements.txt')
    session.run('sphinx-build', 'docs', 'docs/_build')


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
            setupcfg.write(f'\t{arg},\n')

        setupcfg.write('exclude=\n')
        for arg in linter_excludes:
            setupcfg.write(f'\t{arg},\n')

        # PyType stuff
        setupcfg.write('\n[pytype]\n')
        for arg in pytype_args:
            setupcfg.write(f'{arg[2:]}\n')

        setupcfg.write('exclude=\n')
        for arg in pytype_excludes:
            setupcfg.write(f'\t{arg},\n')


def write_dev_requirements() -> None:
    """Write the installs to a dev_requirements.txt file.

    Linters and such don't need to be specified in the main requirements file
    because they have nothing to do with the actual requirements of the program
    """
    with open('dev_requirements.txt', 'w') as devreq:
        for package in (
                linter_installs
                + pytype_installs
                + test_installs
                + docs_installs):
            devreq.write(f'{package}\n')


write_setup_cfg()
write_dev_requirements()
