import csv
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NameValidator:
    def __get__(self, instance, owner):
        return instance._name
    
    def __set__(self, instance, value):
        if not value.replace(" ", "").isalpha() or not value.istitle():
            raise ValueError("ФИО должно содержать только буквы и начинаться с заглавной буквы")
        instance._name = value

class SubjectValidator:
    def __init__(self, subject_list):
        self.subject_list = subject_list
    
    def __get__(self, instance, owner):
        return instance._subject
    
    def __set__(self, instance, value):
        if value not in self.subject_list:
            raise ValueError(f"Предмет '{value}' не разрешен")
        instance._subject = value

class Student:
    name = NameValidator()
    
    def __init__(self, name, subject_file):
        self.name = name
        self._subjects = {}
        self.load_subjects_from_csv(subject_file)
    
    def load_subjects_from_csv(self, filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                subject_name = row[1]  
                self._subjects[subject_name] = {'grades': [], 'test_results': []}
    
    def add_grade(self, grade):
        if self._subject not in self._subjects:
            raise ValueError(f"Предмет '{self._subject}' не существует для данного студента")
        if grade < 2 or grade > 5:
            raise ValueError("Оценка должна быть от 2 до 5")
        self._subjects[self._subject]['grades'].append(grade)
    
    def add_test_result(self, test_result):
        if self._subject not in self._subjects:
            raise ValueError(f"Предмет '{self._subject}' не существует для данного студента")
        if test_result < 0 or test_result > 100:
            raise ValueError("Результат теста должен быть от 0 до 100")
        self._subjects[self._subject]['test_results'].append(test_result)
    
    def get_average_grade(self):
        if self._subject not in self._subjects:
            raise ValueError(f"Предмет '{self._subject}' не существует для данного студента")
        grades = self._subjects[self._subject]['grades']
        return sum(grades) / len(grades) if grades else 0
    
    def get_average_grade_all_subjects(self):
        total_grades = [grade for subject in self._subjects.values() for grade in subject['grades']]
        return sum(total_grades) / len(total_grades) if total_grades else 0

def main():
    parser = argparse.ArgumentParser(description="Управление данными студента")
    parser.add_argument("name", help="ФИО студента")
    parser.add_argument("subject_file", help="Файл с предметами")
    args = parser.parse_args()

    try:
        student = Student(args.name, args.subject_file)
        print(f"Студент: {student.name}")

        while True:
            subject = input("Введите предмет (или 'exit' для завершения): ")
            if subject.lower() == 'exit':
                break
            
            try:
                student._subject = subject
                grade = int(input("Введите оценку (от 2 до 5): "))
                student.add_grade(grade)
                test_result = int(input("Введите результат теста (от 0 до 100): "))
                student.add_test_result(test_result)

            except ValueError as e:
                logger.error(e)

        logger.info("Средний балл по предметам:")
        for subject in student._subjects:  
            try:
                student._subject = subject
                average_grade = student.get_average_grade()
                logger.info(f"{subject}: {average_grade}")
            except ValueError as e:
                logger.error(e)

        average_grade_all_subjects = student.get_average_grade_all_subjects()
        logger.info(f"Средний балл по всем предметам: {average_grade_all_subjects:.2f}")

    except ValueError as e:
        logger.error(e)

if __name__ == "__main__":
    main()