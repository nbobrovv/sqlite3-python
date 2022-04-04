#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sqlite3
from sqlite3 import Error


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


def sql_connection(file):
    try:
        con = sqlite3.connect(file)
        return con
    except Error:
        print(Error)


def sql_table(con):
    cursor_obj = con.cursor()
    cursor_obj.execute(
    """
    CREATE TABLE IF NOT EXISTS students (
    "№" integer PRIMARY KEY autoincrement,
    "ФИО" text,
    "Группа" text,
    "Успеваемость" text)
    """
    )
    con.commit()


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Создать основной парсер командной строки.
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
        parents=[file_parser],
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
        parents=[file_parser],
        help="Display all students"
    )

    # Создать субпарсер для выбора студентов.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
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
    con = sql_connection(args.filename)
    sql_table(con)
    if args.command == "add":
        adding(con, args.name, args.group, args.grade)
    elif args.command == 'display':
        table(con)
    elif args.command == "select":
        selecting(con, args.select)
    con.close()


if __name__ == '__main__':
    main()