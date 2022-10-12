import os
import sys

import click
from flask_migrate import Migrate, upgrade

from app import create_app, db
from app.models import Role, User

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


COV = None
if os.environ.get("FLASK_COVERAGE"):
    import coverage

    COV = coverage.coverage(branch=True, include="app/*")
    COV.start()


@app.cli.command()
@click.option(
    "--coverage/--no-coverage", default=False, help="Run tests under coverage"
)
@click.argument("test_names", nargs=-1)
def test(coverage, test_names):
    """Run the unit tests."""
    if coverage and not os.environ.get("FLASK_COVERAGE"):
        os.environ["FLASK_COVERAGE"] = "1"
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import unittest

    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)

    if COV:
        COV.stop()
        COV.save()
        print("Coverage summary:")
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, "tmp/coverage")
        COV.html_report(directory=covdir)
        print(f"HTML Version: file://{covdir!r}/index.html")
        COV.erase()


@app.cli.command()
@click.option(
    "--length",
    default=25,
    help="Number of functions to include in the profiler report.",
)
@click.option(
    "--profile-dir", default=None, help="Directory where profiler saves the report."
)
def profile(length, profile_dir):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware

    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app, restrictions=[length], profile_dir=profile_dir
    )
    app.run(debug=False)


@app.cli.command()
def deploy():
    """Run deployment tasks"""
    # migrate db to latest version
    upgrade()

    # create or update user Roles
    Role.insert_roles()

    # ensure all users follow themselves
    User.add_self_follows()
