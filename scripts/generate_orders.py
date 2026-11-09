"""
Simulates a day of activity in the source system so every pipeline run has new work:
new orders come in, and some existing orders change status.
"""
import os
import random
import pymysql


def main(new_orders=150, status_changes=60):
    con = pymysql.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        autocommit=True,
    )
    with con.cursor() as cur:
        cur.execute("SELECT MAX(customer_id) FROM customers")
        max_customer = cur.fetchone()[0]

        rows = [
            (random.randint(1, max_customer),
             random.choice(["pending", "pending", "shipped", "completed"]),
             round(random.uniform(10, 250), 2))
            for _ in range(new_orders)
        ]
        cur.executemany(
            "INSERT INTO orders (customer_id, order_date, status, amount, updated_at) "
            "VALUES (%s, NOW(), %s, %s, NOW())", rows)

        # move some open orders forward, which the pipeline has to pick up as updates
        cur.execute(
            "UPDATE orders SET status = CASE status WHEN 'pending' THEN 'shipped' ELSE 'completed' END, "
            "updated_at = NOW() WHERE status IN ('pending', 'shipped') ORDER BY RAND() LIMIT %s",
            (status_changes,))
        print(f"Inserted {new_orders} orders, updated {cur.rowcount} orders")
    con.close()


if __name__ == "__main__":
    main()
