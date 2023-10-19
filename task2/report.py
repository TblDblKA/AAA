from sys import argv  # to check arguments of script
from os.path import exists  # to check whether the input file exists
import filecmp  # to check whether an input and output file are the same
from typing import TextIO, Dict, Set, List
from collections import defaultdict

INPUT_FILE = 'test.csv'
SEPARATOR = ';'
OUTPUT_FILE = 'result.csv'


def validate_files(input_filename: str, output_filename: str, separator: str) -> None:
    """
    Checks that input file is correct csv file with correct amount and type of fields.

    :param input_filename: name of input file of a report
    :type input_filename: str
    :param output_filename: name of output file of a report
    :type output_filename: str
    :param separator:  symbol of separator in csv-file
    :type separator: str
    :return: None
    :raises ValueError: when input file has wrong format: not 6 columns or 6th column is not a number; or when input
        and output files are same
    """
    if exists(output_filename) and filecmp.cmp(input_filename, output_filename):
        raise ValueError('Input and output files are the same')

    if exists(input_filename):
        extension = input_filename.split('.')[-1]
        if extension != 'csv':
            raise ValueError('Your input file is not .csv file')
    else:
        raise ValueError('Your input file doesn\'t exist')
    with open(input_filename, "r", encoding="utf8") as file:
        line = file.readline()
        line = file.readline()
        splitted_line = line.split(separator)
        try:
            int(splitted_line[5])
            if len(splitted_line) != 6:
                raise ValueError()
        except (ValueError, IndexError):
            raise ValueError('Your input file has wrong format')


def parse_parameters() -> tuple[str, str, str]:
    """
    Parses parameters of script and checks if there is a correct input file after '-if' or '--input-file' parameter,
    output file after '-of' or '--output-file' and separator after '-s' or '--separator'.
        Default value for input file is stored in global const INPUT_FILE.
        Default value for output file is stored in global const OUTPUT_FILE.
        Default value for separator is stored in global const SEPARATOR.

    :return: input filename, output filename, separator
    :rtype: str, str, str
    :raises AttributeError: when there are errors in list of parameters
    :raises ValueError: when input or output file are not correct
    """
    if len(argv) == 1:
        validate_files(INPUT_FILE, OUTPUT_FILE, SEPARATOR)
        return INPUT_FILE, OUTPUT_FILE, SEPARATOR
    parameters_options = {
        'input_filename': {
            'keys': ['-if', '--input-file'],
            'index': 0,
            'value': INPUT_FILE
        },
        'output_filename': {
            'keys': ['-of', '--output-file'],
            'index': 0,
            'value': OUTPUT_FILE
        },
        'separator': {
            'keys': ['-s', '--separator'],
            'index': 0,
            'value': SEPARATOR
        }
    }
    for fact_parameter_index, fact_parameter_value in enumerate(argv):
        for param_name, param_options in parameters_options.items():
            if fact_parameter_value in param_options['keys']:
                if parameters_options[param_name]['index'] != 0:
                    raise AttributeError(f'Your script has more than one {param_name}')
                parameters_options[param_name]['index'] = fact_parameter_index

    for param_name, param_options in parameters_options.items():
        param_index = parameters_options[param_name]['index']
        if param_index + 1 == len(argv):
            raise AttributeError(f'Your script parameters have no {param_name}')
        if param_index != 0:
            parameters_options[param_name]['value'] = argv[param_index + 1]

    input_filename = parameters_options['input_filename']['value']
    output_filename = parameters_options['output_filename']['value']
    separator = parameters_options['separator']['value']

    validate_files(input_filename, output_filename, separator)

    return input_filename, output_filename, separator


def get_menu_option() -> str:
    """
    Prints an invitation message to enter a number of menu item. If item is not correct, offers to enter another
    value.

    :return: number of chosen menu item
    :rtype: str
    :raises ValueError: when user enters not correct number menu item
    """
    print('Выберите режим работы программы.')
    print('1. Вывести иерархию команд, т.е. департамент и все команды, которые входят в него.')
    print('2. Вывести сводный отчёт по департаментам: название, численность, "вилка" зарплат.')
    print('3. Сохранить сводный отчёт из пункта 2. в виде csv-файла.')
    print('Введите одно число.')
    option = input()
    correct_option_flag = option in ['1', '2', '3']
    if not correct_option_flag:
        raise ValueError('Вы ввели некорректное значение для пункта меню.')
    return option


def generate_hierarchy(file: TextIO, separator: str) -> Dict[str, Set[str]]:
    """
    Generate hierarchy of teams by departments.

    :param file: input file to parse
    :type file: TextIO
    :param separator: separator of the csv file
    :type: str
    :return: dict with hierarchy, where key of item is the name of department, and value is a set of teams in this
        department
    :rtype: Dict[str, Set[str]]
    """
    departments_list = defaultdict(set)
    for line_number, line in enumerate(file):
        if line_number == 0:
            continue
        _, department, team, *_ = line.split(separator)
        departments_list[department].add(team)
    return departments_list


def print_department_hierarchy(departments_list: dict) -> None:
    """
    Prints hierarchy of teams by departments, generated in generate_hierarchy().
    :param departments_list: dict with keys as department name and value as teams in that department.
    :type: Dict[str, Set[str]]
    :return: None
    """
    for department in departments_list.keys():
        print(f'Департамент: {department}')
        for team in departments_list[department]:
            print(f'\tКоманда: {team}')


def generate_report_by_department(file: TextIO, separator: str) -> List[Dict[str, str | int] | float]:
    """
    Generate report about each department: amount of people in it, difference between min and max salary and average
    salary of employees.
    :param file: input csv file
    :type file: TextIO
    :param separator: symbol of separator in csv file
    :type separator: str
    :return: list of dicts, where every item has the following keys:
        Название: name of department,
        Численность: amount of people in the department,
        Вилка зарплат: difference between min and max salary,
        Средняя зарплата: average salary of employees
    :rtype: List[Dict[str, str | int | float]]
    """
    departments_dict = defaultdict(list)
    for line_number, line in enumerate(file):
        if line_number == 0:
            continue
        _, department, *_, salary = line.split(separator)
        departments_dict[department].append(int(salary))
    departments_list = []
    for department, salaries in departments_dict.items():
        departments_list.append({
            'Название': department,
            'Численность': len(salaries),
            'Вилка зарплат': f'{min(salaries)} - {max(salaries)}',
            'Средняя зарплата': sum(salaries) / len(salaries)
        })
    return departments_list


def print_department_report(departments_list: List[Dict[str, str | int] | float]) -> None:
    """
    Prints a report about each department, which was generated in generate_report_by_department().
    :param departments_list: list of dicts, where each item describes each department
    :type departments_list: list[dict]
    :return: None
    """
    for department in departments_list:
        for property_name, property_value in department.items():
            print(f'{property_name}: {property_value}')
        print()  # to make printed data more readable


def save_department_report(departments_list: [dict], output_filename: str, separator: str) -> None:
    """
    Saves a report about each department, which was generated in generate_report_by_department(), in a file named
    output_filename.

    :param departments_list: list of dicts, where each item describes each department
    :type departments_list: list[dict]
    :param output_filename: name of an output file
    :type output_filename: str
    :param separator: separator of a csv file
    :type separator: str
    :return: None
    """
    with open(output_filename, 'w+', encoding='utf8') as new_file:
        line = ''
        for property_name in departments_list[0]:
            line += f'{property_name}{separator}'
        line = line[:-1]
        new_file.write(f'{line}\n')
        for department in departments_list:
            line = ''
            for property_value in department.values():
                line += f'{property_value}{separator}'
            line = line[:-1]
            new_file.write(f'{line}\n')


def generate_report(input_filename: str, output_filename: str, separator: str, option: str) -> None:
    """
    General generator of a report.

    :param input_filename: name of an input csv file, which have information about departments
    :type input_filename: str
    :param output_filename: name of an output file, where we need to store our information, if user chooses 3rd menu
        option
    :type output_filename: str
    :param separator: separator of a csv file
    :type separator: str
    :param option: number of option in menu the user chose
    :type option: str
    :return: None
    """
    with open(input_filename, "r", encoding="utf8") as file:
        if option == '1':
            departments_hierarchy = generate_hierarchy(file, separator)
            print_department_hierarchy(departments_hierarchy)
        else:
            departments_report = generate_report_by_department(file, separator)
            if option == '2':
                print_department_report(departments_report)
            else:
                save_department_report(departments_report, output_filename, separator)


if __name__ == '__main__':
    input_file, output_file, separator = parse_parameters()
    menu_option = get_menu_option()
    generate_report(input_file, output_file, separator, menu_option)
