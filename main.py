from classes.hh_parser import HHparser
from classes.db_manager import DBManager


def main():
    # Get info about employers
    response = HHparser()

    employers_dict = response.list_employers
    employers_all_vacancies = response.get_vacancies()

    # Create database
    database = DBManager()
    database.create_database('parser')

    # Create tables
    database.create_tables('parser')

    # Save info to database
    database.save_info_to_database('parser', employers_dict, employers_all_vacancies)
    while True:

        new = input(
            '1 - список всех компаний и кол-во вакансий у каждой компании\n'
            '2 - список всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки на вакансию\n'
            '3 - средняя зарплата по вакансиям\n'
            '4 - список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
            '5 - список вакансий, в названии которых содержится ключевое слово "..."\n'
            'Выход - закончить\n'
        )

        if new == '1':
            print("Список компаний и количество вакансий в компаниях:")
            for row in database.get_companies_and_vacancies_count('parser'):
                print(f"{row[0]} - {row[1]}")
        elif new == '2':
            print("Список всех вакансий с указанием названия компании:")
            for row in database.get_all_vacancies('parser'):
                print(f"Название:{row[0]} - Вакансия:{row[1]} - url:{row[3]}")
        elif new == '3':
            print("Получает среднюю зарплату по вакансиям:")
            for row in database.get_avg_salary('parser'):
                print(f"Средняя зарплата по все вакансиям :{row[0]}")
        elif new == '4':
            print("Список всех вакансий, у которых зарплата выше средней по всем вакансиям:")
            for row in database.get_vacancies_salary_higher_avg('parser'):
                print(f"{row[0]} - Зарплата:{row[1]}")
        elif new == '5':
            keyword = str(input('Найти: '))
            print("Список всех вакансий, в названии которых содержатся переданное ключевое слово:")
            for row in database.get_vacancies_with_keyword('parser', keyword.title()):
                print(f"Вакансия:{row[0]} - Зарплата:{row[1]} - url:{row[2]}")

        elif new == 'Выход':
            break


if __name__ == '__main__':
    main()
