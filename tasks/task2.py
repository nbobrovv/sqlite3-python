#! /usr/bin/env python3
# -*-coding: utf-8 -*-

import argparse
import psycopg2

def selecting(con, student):
    cur= con.cursor()
    cur.execute(f"""SELECT * FROM students WHERE "Успеваемость" = '{student}'""")
    print(cur.fetchall())


def table(con):
    cur= con.cursor()
    cur.execute("SELECT * FROM students")
    print(cur.fetchall())


def adding(con, name, group, grade):
    cur= con.cursor()
    cur.execute(f"""INSERT INTO students("ФИО", "Группа", "Успеваемость") 
    VALUES('{name}', '{group}', '{grade}');""")
    con.commit()


def sql_table(con):
    cursor_obj = con.cursor()
    cursor_obj.execute(
    """
    CREATE TABLE IF NOT EXISTS students (
    "ФИО" text,
    "Группа" text,
    "Успеваемость" text)
    """
    )
    con.commit()


def main(command_line=None):
    try:
        parser = argparse.ArgumentParser("students")
        parser.add_argument(
            "--version",
            action="version",
            help="The main parser",
            version="%(prog)s 0.1.0"
        )

        subparsers = parser.add_subparsers(dest="command")

        # Создать субпарсер для добавления студента.
        add = subparsers.add_parser(
            "add",
            help="Add a new student"
        )
        add.add_argument(
            "-n",
            "--name",
            action="store",
            required=True,
            help="The student's name"
        )
        add.add_argument(
            "-g",
            "--group",
            type=int,
            action="store",
            help="The student's group"
        )
        add.add_argument(
            "-gr",
            "--grade",
            action="store",
            required=True,
            help="The student's grade"
        )

        # Создать субпарсер для отображения всех студентов.
        _ = subparsers.add_parser(
            "display",
            help="Display all students"
        )

        # Создать субпарсер для выбора студентов.
        select = subparsers.add_parser(
            "select",
            help="Select the students"
        )
        select.add_argument(
            "-s",
            "--select",
            action="store",
            required=True,
            help="The required select"
        )

        args = parser.parse_args(command_line)
        connection = psycopg2.connect(
            user="postgres",
            password="b0brov5572",
            host="127.0.0.1",
            port="5432",
            database="mydatabase"
        )
        sql_table(connection)
        if args.command == "add":
            adding(connection, args.name, args.group, args.grade)
        elif args.command == 'display':
            table(connection)
        elif args.command == "select":
            selecting(connection, args.select)
    finally:
        connection.close()


if __name__ == '__main__':
    main()