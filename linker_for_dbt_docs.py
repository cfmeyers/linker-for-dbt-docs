import glob
import os
import re


def make_link(project_name, model_name):
    if '.' in model_name:
        file_name = model_name.replace('.', '_', 1)
        display_name = model_name
    else:
        file_name = model_name
        display_name = model_name.replace('_', '.', 1)
    return f'<a href="#!/model/model.{project_name}.{file_name}">{display_name}</a>'


def collect_linkable_file_names(absolute_path):
    file_names = [
        f for f in glob.glob(absolute_path + "/models/**/*.sql", recursive=True)
    ]
    return set([os.path.basename(name).split('.')[0] for name in file_names])


def make_link_map(model_names, project_name):
    link_map = {}
    for model_name in model_names:
        link_map[model_name] = make_link(project_name, model_name)
    return link_map


def insert_links_in_line(link_map, line):
    for model_name, link in link_map.items():
        alternate_name = model_name.replace('_', '.')
        line = re.sub(model_name + '|' + alternate_name, link, line)
    return line


if __name__ == '__main__':
    pass
