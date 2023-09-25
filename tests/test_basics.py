import unittest

from flask import current_app
from sqlalchemy import inspect

from flaskblog import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_app_debug_mode(self):
        self.assertFalse(current_app.config['DEBUG'])

    def test_check_db_in_memory(self):
        self.assertEqual(current_app.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///:memory:')

    def test_database_structure(self):
        # Получаем объект для инспекции базы данных
        inspector = inspect(db.engine)

        # Получаем список всех таблиц в базе данных
        tables = inspector.get_table_names()

        # Проходим по таблицам и получаем информацию о структуре каждой
        for table_name in tables:
            columns = inspector.get_columns(table_name)
            print(f"Table: {table_name}")
            for column in columns:
                print(f"  Column: {column['name']} - Type: {column['type']}")
