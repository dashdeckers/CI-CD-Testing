"""Noxfile."""
import nox
from nox.sessions import Session


# Reuse virtualenvs to allow working offline
nox.options.envdir = '.nox_cache/'
nox.options.reuse_existing_virtualenvs = True

# Specify which locations to check
locations = ['src', 'tests', 'noxfile.py', 'docs/conf.py']


# Specify the code linter frameworks and arguments
linter_installs = [
    'flake8',
    'flake8-annotations',    # type hints and annotations
    'flake8-docstrings',     # same as pydocstyle
    'darglint',              # checks docs for argument validity etc
    'mccabe',                # code complexity
]
linter_ignores = [
    'I',     # Any import related complaints
    'W503',  # 'line break before binary operator'
]
linter_excludes = [
    'tests/',
]
linter_args = [
    # '--config=ignore',
    '--docstring-style=google',
    '--max-complexity=8',
    '--max-line-length=80',
]


# Specify the static type checker frameworks and arguments
pytype_installs = [
    'pytype',
]
pytype_excludes = [
    'tests/',
]
pytype_args = [
    '--disable=import-error',
]


# Specify the testing frameworks and arguments
test_installs = [
    'pytest',      # run tests
    'pytest-cov',  # determine test coverage
]
doc_test_installs = [
    'xdoctest',    # check examples in docstrings
    'pygments',    # colorful terminal output
]


# Specify the docs generation framework and arguments
docs_installs = [
    'sphinx',                    # generate docs automatically
    'sphinx-autodoc-typehints',  # include typehints in the docs
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


@nox.session(python=['3.8'])
def test_docs(session: Session) -> None:
    """Run doctests with XDoctest.

    Args:
        session (Session): Nox session.
    """
    args = session.posargs or locations

    session.install(*doc_test_installs)
    session.run('python', '-m', 'xdoctest', *args)


@nox.session(python=['3.8'])
def test(session: Session) -> None:
    """Run tests with PyTest.

    Args:
        session (Session): Nox session.
    """
    args = session.posargs or [
        '--cov=src/',
        '--cov-fail-under=50',
        # '--rootdir=src/',
        # '--ignore=src/main.py'
    ]

    session.install('-r', 'requirements.txt')
    session.run('python', '-m', 'pytest', *args)


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
