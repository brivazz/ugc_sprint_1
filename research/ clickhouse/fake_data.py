import clickhouse_driver


def insert_rows(conn, table_name, num_rows):
    with conn.cursor() as cursor:
        insert_statement = f"INSERT INTO {table_name} (id, user_id, film_id, view_time, event_time) VALUES"

        for i in range(1, num_rows + 1):
            user_id = "rand()"
            film_id = "rand()"
            view_time = "rand()"
            event_time = "today()"

            insert_statement += (
                f" ({i}, {user_id}, {film_id}, {view_time}, {event_time}),"
            )

            if i % 10000 == 0:
                insert_statement = insert_statement[:-1]

                cursor.execute(insert_statement)

                insert_statement = f"INSERT INTO {table_name} (id, user_id, film_id, view_time, event_time) VALUES"

        conn.commit()


if __name__ == "__main__":
    conn = clickhouse_driver.connect(host="localhost", database="default")

    cursor = conn.cursor()

    insert_rows(conn, "test", 10000000)

    cursor.execute("SELECT COUNT(*) FROM test")
    count = cursor.fetchone()[0]
    print(f"Total rows in the table: {count}")

    conn.close()
