import time

import clickhouse_driver

from fake_data import insert_rows


def get_metrics(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function: {func.__name__}")
        print(f"Execution time: {execution_time:.4f} seconds")
        return result

    return wrapper


@get_metrics
def insert_1000_rows(conn):
    insert_rows(conn, "test", 1000)


@get_metrics
def insert_10000_rows(conn):
    insert_rows(conn, "test", 10000)


@get_metrics
def get_rows_count(cursor):
    cursor.execute("SELECT COUNT(*) FROM test;")
    cnt = cursor.fetchone()[0]
    return cnt


@get_metrics
def get_all_users_count(cursor):
    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM test;")
    cnt = cursor.fetchone()[0]
    return cnt


@get_metrics
def get_all_films_count(cursor):
    cursor.execute("SELECT COUNT(DISTINCT film_id) FROM test;")
    cnt = cursor.fetchone()[0]
    return cnt


@get_metrics
def get_total_view_time(cursor):
    cursor.execute("SELECT user_id, SUM(view_time) FROM test GROUP BY user_id;")
    result = cursor.fetchall()
    return result


@get_metrics
def get_total_film_views(cursor):
    cursor.execute(
        """SELECT t1.film_id, count(*) from
    (SELECT user_id, film_id, MAX(view_time) FROM test
    GROUP BY user_id, film_id) t1
    GROUP BY t1.film_id;
    """
    )
    film = cursor.fetchone()[0]
    return film


if __name__ == "__main__":
    conn = clickhouse_driver.connect(host="localhost", database="default")

    cursor = conn.cursor()

    insert_1000_rows(conn)
    insert_10000_rows(conn)
    get_rows_count(cursor)
    get_all_users_count(cursor)
    get_all_films_count(cursor)
    get_total_view_time(cursor)
    get_total_film_views(cursor)

    conn.close()
