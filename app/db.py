import click
import psycopg2
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            user=current_app.config["POSTGRES_USER"],
            password=current_app.config["POSTGRES_PASSWORD"],
            host=current_app.config["POSTGRES_HOST"],
            database=current_app.config["POSTGRES_DATABASE"],
        )
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db:
        db.close()


@click.command("init-db")
@with_appcontext
def init_db_command():
    with current_app.open_resource("schema.sql") as f:
        db = get_db()
        with db.cursor() as cur:
            cur.execute(f.read().decode("utf-8"))
        db.commit()
    click.echo("Database has been initialized")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
