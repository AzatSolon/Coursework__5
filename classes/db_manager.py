import psycopg2
from utils.config import config


class DBManager:
    """
    Класс для работы с информацией из Базы Данных
    """
    def __init__(self):
        self.params_db = config()

    def create_database(self, database_name):
        """
        Создание базы данных.
        """

        conn = psycopg2.connect(dbname='postgres', **self.params_db)
        conn.autocommit = True

        cur = conn.cursor()

        cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
        cur.execute(f'CREATE DATABASE {database_name}')

        cur.close()
        conn.close()

    def create_tables(self, database_name):
        """
        Создание таблиц companies и vacancies в созданной базе данных
        """

        with psycopg2.connect(dbname=database_name, **self.params_db) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE companies (
                    company_id SERIAL PRIMARY KEY,
                    company_name VARCHAR UNIQUE
                    )
                    """)

                cur.execute("""
                        CREATE TABLE vacancies 
                        (vacancy_id serial,
                        vacancy_name VARCHAR(255) NOT NULL,
                        salary int,
                        company_name text REFERENCES companies(company_name) NOT NULL,
                        vacancy_url VARCHAR(255),
                        foreign key(company_name) references companies(company_name)
                        )
                        """)

        conn.close()

    def save_info_to_database(self, database_name, employers_dict, vacancies_list):
        """
        Напонялет базу данных.
        """
        with psycopg2.connect(dbname=database_name, **self.params_db) as conn:
            with conn.cursor() as cur:
                for employer in employers_dict:
                    cur.execute(
                        f"INSERT INTO companies(company_name) values ('{employer}')")
                for vacancy in vacancies_list:
                    cur.execute(
                        f"INSERT INTO vacancies(vacancy_name, salary, company_name, vacancy_url) values "
                        f"('{vacancy['vacancy_name']}', '{int(vacancy['salary'])}', "
                        f"'{vacancy['employer']}', '{vacancy['url']}')")

        conn.close()

    def get_companies_and_vacancies_count(self, database_name):
        """
        Возвращает список всех компаний и количество вакансий у каждой компании.
        """
        with psycopg2.connect(dbname=database_name, **self.params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT company_name, COUNT(vacancy_name) from vacancies GROUP BY company_name')
                answer = cur.fetchall()
        conn.close()
        return answer

    def get_all_vacancies(self, database_name):
        """
        Возвращает список всех вакансий
        """
        with psycopg2.connect(dbname=database_name, **self.params_db) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT company_name, vacancy_name, salary, vacancy_url FROM companies JOIN vacancies using (company_name)')
                answer = cur.fetchall()
        conn.close()
        return answer

    def get_avg_salary(self, database_name):
        """
        Возвращает среднюю зарплату по всем вакансиям hh.ru
        """
        with psycopg2.connect(dbname=database_name, **self.params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT avg(salary) from vacancies')
                answer = cur.fetchall()
        conn.close()
        return answer

    def get_vacancies_salary_higher_avg(self, database_name):
        """
        Возвращает список всех вакансий и их зарплаты, у которых зарплата выше средней по всем вакансиям
        """
        with psycopg2.connect(dbname=database_name, **self.params_db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT vacancy_name, salary from vacancies WHERE salary > (SELECT AVG(salary) from vacancies)')
                answer = cur.fetchall()
        conn.close()
        return answer

    def get_vacancies_with_keyword(self, database_name, keyword):
        """
        Получает список всех вакансий, в названии которых содержится ключивое слово.
        """

        with psycopg2.connect(dbname=database_name, **self.params_db) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT vacancy_name, salary, vacancy_url from vacancies WHERE vacancy_name LIKE '%{keyword}%'")
                answer = cur.fetchall()
        conn.close()
        return answer
