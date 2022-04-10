#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Самостоятельно изучите работу с пакетом python-psycopg2 для работы с базами данных
PostgreSQL. Для своего варианта лабораторной работы 2.17 необходимо реализовать
возможность хранения данных в базе данных СУБД PostgreSQL.
"""

import psycopg2
import typing as t
import argparse


def connect():
    conn = psycopg2.connect(
        user="postgres",
        password="b0brov5572",
        host="127.0.0.1",
        port="5432",
        database = "postgres"
    )

    return conn


def display(students: t.List[t.Dict[str, t.Any]]) -> None:
    """
    Отобразить список студентов
    """
    if students:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "No",
                "ФИО",
                "Группа",
                "Успеваемость"
            )
        )
        print(line)
        for idx, student in enumerate(students, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('groupt', ''),
                    student.get('grade', 0)

                )
            )
            print(line)
        else:
            print("Список пуст")


def create_db() -> None:
    """
    Создать базу данных.
    """
    cursor = connect().cursor()
    # Создать таблицу с ФИО студентов
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS student (
        student_id serial,
        PRIMARY KEY(student_id),
        name TEXT NOT NULL
        )
        """
    )
    # Создать таблицу с полной информацией о студентах
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
        student_id serial,
        PRIMARY KEY(student_id),
        groupt INTEGER NOT NULL,
        grade TEXT NOT NULL,
        FOREIGN KEY(student_id) REFERENCES student(student_id)
        ON DELETE CASCADE ON UPDATE CASCADE
        )
        """
    )


def add_student(
        name: str,
        groupt: int,
        grade: str
) -> None:
    cursor = connect().cursor()
    # Получить идентификатор студента в базе данных.
    # Если такой записи нет, то добавить информацию о студенте
    cursor.execute(
        """
        SELECT student_id FROM student WHERE name = %s;
        """,
        (name,)
    )
    row = cursor.fetchone()
    if row is None:

        cursor.execute(
            """
            INSERT INTO student (name) VALUES (%s)
            """,
            (name,)
        )
        student_id = cursor.lastrowid
    else:
        student_id = row[0]

        # Добавить информацию о новом продукте.
    cursor.execute(
        """
        INSERT INTO students (student_id, grade, groupt)
        VALUES (%s, %s, %s)
        """,
        (student_id, grade, groupt)
    )
    connect().commit()


def select_student():
    """
    Выбрать всех студентов.
    """
    cursor = connect().cursor()
    cursor.execute(
        """
        SELECT student.name, students.groupt, students.grade
        FROM students
        INNER JOIN student ON student.student_id = students.student_id
        """
    )
    rows = cursor.fetchall()
    connect().close()
    return [
        {
            "name": row[0],
            "groupt": row[1],
            "grade": row[2],

        }
        for row in rows
    ]


def select_students(name) -> t.List[t.Dict[str, t.Any]]:
    """
    Выбрать студента
    """
    cursor = connect().cursor()
    cursor.execute(
        """
        SELECT student.name, students.groupt, students.grade
        FROM students
        INNER JOIN student ON student_name.student_id = students.student_id
        WHERE student_name.name = %s
        """,
        (name,)
    )
    rows = cursor.fetchall()
    connect().close()
    return [
        {
            "name": row[0],
            "groupt": row[1],
            "grade": row[2],
        }
        for row in rows
    ]


def main(command_line=None):
    parser = argparse.ArgumentParser("students")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления магазина.
    add = subparsers.add_parser(
        "add",
        help="Add a new student"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The students's name"
    )
    add.add_argument(
        "-g",
        "--group",
        action="store",
        type=int,
        help="The student's group"
    )
    add.add_argument(
        "-gr",
        "--grade",
        action="store",
        required=True,
        help="The student's grade"
    )
    _ = subparsers.add_parser(
        "display",
        help="Display all product"
    )
    # Создать субпарсер для выбора работников.
    select = subparsers.add_parser(
        "select",
        help="Select the shops"
    )
    select.add_argument(
        "-s",
        "--select",
        action="store",
        required=True,
        help="The shop's name"
    )
    args = parser.parse_args(command_line)
    create_db()
    if args.command == "add":
        add_student(args.name, args.group, args.grade)
    elif args.command == "select":
        display(select_students(args.name))
    elif args.command == "display":
        display(select_student())
    pass


if __name__ == '__main__':
    main()