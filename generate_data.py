import csv
import random
from itertools import cycle

random_full_names = [
    "Иванов Иван Иванович",
    "Петров Сидор Петрович",
    "Михайлова Мария Владимировна",
    "Смирнов Александр Дмитриевич",
    "Кузнецова Елена Александровна",
    "Попов Дмитрий Алексеевич",
    "Васильева Ольга Ивановна",
    "Морозов Владимир Павлович",
    "Николаева Анна Сергеевна",
    "Федоров Сергей Дмитриевич"
]

num_students = 10

def add_subjects_to_csv(filename, subjects):
    with open(filename, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for subject in subjects:
            writer.writerow(["", subject])  

def main():
    print("Выберите, хотите ли добавить новые предметы:")
    print("1. Добавить рандомные предметы (Математика, Физика, Русский язык)")
    print("2. Ввести предметы вручную")
    
    choice = input("Введите номер варианта (1 или 2): ")

    if choice == '1':
        # List of random subjects
        random_subjects = ["Математика", "Физика", "Русский язык"]
        random.shuffle(random_full_names)
        random_subjects = cycle(random_subjects)

    elif choice == '2':
        num_new_subjects = input("Введите количество новых предметов: ")
        try:
            num_new_subjects = int(num_new_subjects)
            new_subjects = []
            for i in range(num_new_subjects):
                subject_name = input(f"Введите название предмета {i + 1}: ")
                new_subjects.append(subject_name)
            random_subjects = cycle(new_subjects)
        except ValueError:
            print("Некорректный ввод числа предметов. Завершение программы.")
            return

    else:
        print("Некорректный выбор. Завершение программы.")
        return

    with open("subjects.csv", mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ФИО", "Предмет"]) 
        for i in range(num_students):
            writer.writerow([random_full_names[i], next(random_subjects)])

    print(f"{num_students} рандомных ФИО студентов и предметов успешно добавлены в файл 'subjects.csv'.")

    if choice == '2':
        add_subjects_to_csv("subjects.csv", new_subjects)
        print(f"{num_new_subjects} новых предметов успешно добавлены в файл 'subjects.csv'.")

if __name__ == "__main__":
    main()