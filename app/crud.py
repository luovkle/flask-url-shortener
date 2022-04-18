from secrets import token_urlsafe

import psycopg2.extras
from flask import current_app


class CRUDUrl:
    def __get_url(self, db, original_url) -> str | None:
        with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = "SELECT * FROM urls WHERE original = %s;"
            cur.execute(sql, (original_url,))
            url_shortened = cur.fetchone()
            return url_shortened

    def create(self, db, original_url) -> str | None:
        url_data = self.__get_url(db, original_url)
        if url_data:
            return url_data["original"]
        with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = "INSERT INTO urls (original, shortened) VALUES (%s, %s);"
            url_shortened = f"{current_app.config['CURRENT_HOST']}/{token_urlsafe(7)}"
            cur.execute(sql, (original_url, url_shortened))
            db.commit()
            return url_shortened

    def read(self, db, url_shortened) -> str | None:
        with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = "SELECT * FROM urls WHERE shortened = %s;"
            cur.execute(sql, (url_shortened,))
            url_data = cur.fetchone()
            return url_data["original"] if url_data else None


crud_url = CRUDUrl()
