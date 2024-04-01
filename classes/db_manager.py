import psycopg2
from utils.config import config


class DBManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def execute_query(self, query) -> list:
        conn = psycopg2.connect(dbname=self.db_name, **config())
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()

        return result

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        result = self.execute_query("SELECT employers.name, COUNT(vacancies.id) AS vacancies_count "
                                    "FROM employers "
                                    "LEFT JOIN vacancies ON employers.id = vacancies.employer "
                                    "GROUP BY employers.name"
                                    )
        return result

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        result = self.execute_query("SELECT employers.name, vacancies.name, salary_from, salary_to, url "
                                    "FROM vacancies "
                                    "LEFT JOIN employers ON vacancies.employer = employers.id "
                                    )
        return result

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        result = self.execute_query("SELECT vacancies.name, ROUND(AVG(salary_from), 0) AS avg_salary_from, "
                                    "ROUND(AVG(salary_to), 0) AS avg_salary_to "
                                    "FROM vacancies "
                                    "GROUP BY vacancies.name "
                                    "ORDER BY avg_salary_from DESC"
                                    )
        return result

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        result = self.execute_query("SELECT vacancies.name, salary_from "
                                    "FROM vacancies "
                                    "WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies) "
                                    "ORDER BY salary_from DESC"
                                    )
        return result

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        query = f"SELECT vacancies.name FROM vacancies WHERE vacancies.name LIKE '%{keyword}%' GROUP BY vacancies.name"
        result = self.execute_query(query)
        return result
