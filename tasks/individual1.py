#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Для своего варианта лабораторной работы 2.17 необходимо реализовать хранение данных в
базе данных SQLite3.
"""

import sqlite3
import typing as t
from pathlib import Path
import argparse


def create_db(database_path: Path) -> None:
    """
    Создать базу данных.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    # Создать таблицу с ФИО студентов
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS student_name (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
        )
        """
    )
    # Создать таблицу с полной информацией о студентах
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        groupt INTEGER NOT NULL,
        grade TEXT NOT NULL,
        FOREIGN KEY(student_id) REFERENCES student_name(student_id)
        )
        """
    )
    conn.close()


def add_student(
        database_path: Path,
        name: str,
        groupt: int,
        grade: str
) -> None:
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    # Получить идентификатор студента в базе данных.
    # Если такой записи нет, то добавить информацию о студенте
    cursor.execute(
        """
        SELECT student_id FROM student_name WHERE name = ?
        """,
        (name,)
    )
    row = cursor.fetchone()
    if row is None:
        cursor.execute(
            """
            INSERT INTO student_name (name) VALUES (?)
            """,
            (name,)
        )
        student_id = cursor.lastrowid
    else:
        student_id = row[0]

        # Добавить информацию о новом продукте.
    cursor.execute(
        """
        INSERT INTO students (student_id, groupt, grade)
        VALUES (?, ?, ?)
        """,
        (student_id, groupt, grade)
    )
    conn.commit()
    conn.close()


def display(students: t.List[t.Dict[str, t.Any]]) -> None:
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


def select_student(database_path: Path) -> t.List[t.Dict[str, t.Any]]:
    """
    Выбрать всех студентов.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT student_name.name, students.groupt, students.grade
        FROM students
        INNER JOIN student_name ON student_name.student_id = students.student_id
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "name": row[0],
            "groupt": row[1],
            "grade": row[2],

        }
        for row in rows
    ]


def select_students(database_path: Path, name: str) -> t.List[t.Dict[str, t.Any]]:
    """
    Выбрать студента
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT student_name.name, students.groupt, students.grade
        FROM students
        INNER JOIN student_name ON student_name.student_id = students.student_id
        WHERE student_name.name == ?
        """,
        (name,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "name": row[0],
            "groupt": row[1],
            "grade": row[2],
        }
        for row in rows
    ]


def main(command_line=None):
    """
    Основная функция программы
    """
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "--db",
        action="store",
        required=False,
        default=str(Path.home() / "students.db"),
        help="The data file name"
    )
    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("shops")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")
    # Создать субпарсер для добавления магазина.
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
        parents=[file_parser],
        help="Display all product"
    )
    # Создать субпарсер для выбора работников.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
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
    db_path = Path(args.db)
    create_db(db_path)
    if args.command == "add":
        add_student(db_path, args.name, args.group, args.grade)
    elif args.command == "select":
        display(select_students(db_path,args.name))
    elif args.command == "display":
        display(select_student(db_path))
    pass


if __name__ == '__main__':
    main()