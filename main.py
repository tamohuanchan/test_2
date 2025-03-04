import psycopg2
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:pass@192.168.0.139:5434/task_1")
time.sleep(5)

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            position VARCHAR(100) NOT NULL,
            salary INTEGER NOT NULL
        );
    """)
    conn.commit()

    employees = [
        {"name": "Иван", "position": "разработчик", "salary": 55000},
        {"name": "Анна", "position": "аналитик", "salary": 48000},
        {"name": "Петр", "position": "тестировщик", "salary": 52000},
    ]
    for emp in employees:
        cursor.execute(
            "INSERT INTO employees (name, position, salary) VALUES (%s, %s, %s);",
            (emp["name"], emp["position"], emp["salary"])
        )
    conn.commit()

    cursor.execute("SELECT name, position, salary FROM employees;")
    all_employees = cursor.fetchall()

    high_salary_employees = [emp[0] for emp in all_employees if emp[2] > 50000]
    print("Сотрудники с зарплатой больше 50 000:", high_salary_employees)


    total_salary = sum(emp[2] for emp in all_employees)
    average_salary = round(total_salary / len(all_employees) if all_employees else 0, 2)
    print("Средняя зарплата всех сотрудников:", average_salary)

    cursor.execute("SELECT name, position, salary FROM employees ORDER BY salary DESC;")
    sorted_employees = cursor.fetchall()
    print("Сотрудники, отсортированные по зарплате:")
    for emp in sorted_employees:
        print(f"{emp[0]} - {emp[2]}")

    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print("Ошибка при работе с БД:", e)