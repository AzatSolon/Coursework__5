import requests


class HHparser:
    """
    Класс для работы с API HH.ru и заполнение таблиц в BD
    """

    list_employers = {'МегаФон': '3127',
                      'МТС': '3776',
                      'билайн': '4934',
                      'СБЕР': '3529',
                      'Банк ВТБ (ПАО)': '4181',
                      'Тинькофф': '78638',
                      'АШАН Ритейл Россия': '54979',
                      '2ГИС': '64174',
                      'Газпромбанк': '3388',
                      'Ozon': '2180'}

    @staticmethod
    def get_request(employer_id) -> dict:
        """
        Возвращает список по критериям запроса(наличия вакансии и заработной платы).
        """
        params = {
            "page": 1,
            "per_page": 100,
            "employer_id": employer_id,
            "only_with_salary": True,
            "area": 113,
            "only_with_vacancies": True
        }
        return requests.get("https://api.hh.ru/vacancies/", params=params).json()['items']

    def get_vacancies(self):
        """
        Возвращает список работодателей
        """
        vacancies_list = []
        for employer in self.list_employers:
            emp_vacancies = self.get_request(self.list_employers[employer])
            for vacancy in emp_vacancies:
                if vacancy['salary']['from'] is None:
                    salary = 0
                else:
                    salary = vacancy['salary']['from']
                vacancies_list.append(
                    {'url': vacancy['alternate_url'], 'salary': salary,
                     'vacancy_name': vacancy['name'], 'employer': employer})
        return vacancies_list
