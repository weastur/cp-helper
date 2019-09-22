import os
import shutil


AUX_TEMPLATES_FOLDER = 'templates/aux'
CODE_TEMPLATES_FOLDER = 'templates/code'


def generate_folder_structure(contest, problems):
    os.mkdir(str(contest))
    for problem_name in problems.keys():
        os.mkdir(os.path.join(str(contest), problem_name))


def generate_test_files(contest, problems):
    for problem_name, problem_tests in problems.items():
        base_path = os.path.join(str(contest), problem_name)
        for num, test in enumerate(problem_tests, start=1):
            with open(os.path.join(base_path, f'{num}.in'), 'w') as test_in:
                test_in.write(test['input'])
            with open(os.path.join(base_path, f'{num}.out'), 'w') as test_out:
                test_out.write(test['output'])


def copy_templates(platform, contest, problems):
    for directory in [AUX_TEMPLATES_FOLDER, CODE_TEMPLATES_FOLDER]:
        for problem_name, problem_tests in problems.items():
            base_path = os.path.join(str(contest), problem_name)
            templates_path = os.path.join(platform, directory)
            for filename in os.listdir(templates_path):
                full_filename = os.path.join(templates_path, filename)
                shutil.copy(full_filename, base_path)
