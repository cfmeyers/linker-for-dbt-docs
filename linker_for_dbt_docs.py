import argparse
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
        alternate_name = model_name.replace('_', '.', 1)
        link_map[alternate_name] = make_link(project_name, model_name)
    return link_map


def tokenize_line(line):
    tokens = []
    for token in re.split(r'(<a.*>.*</a>)', line):
        tokens.append(token)
    return tokens


def build_model_match_pattern(model_names):
    sorted_by_length = sorted(model_names, key=lambda x: -1 * len(x))
    return r'(' + r'|'.join(sorted_by_length) + ')'


def recursively_sub_anchors(finished_text, remaining_text, link_map, pattern):
    if not remaining_text:
        return finished_text
    tokens = [t for t in tokenize_line(remaining_text) if t]

    head, tail = tokens[0], tokens[1:]
    remaining_text = ''.join(tail)

    if head.startswith('<a'):
        finished_text += head
        return recursively_sub_anchors(finished_text, remaining_text, link_map, pattern)

    match = re.search(pattern, head)
    if match:
        link = link_map[match.group(1)]
        head = re.sub(match.group(1), link, head, 1)
        tokens = re.split('(' + link + ')', head, 1)
        finished_text += ''.join(tokens[:2])
        remaining_text = ''.join(tokens[2:])
        return recursively_sub_anchors(finished_text, remaining_text, link_map, pattern)
    else:
        finished_text += head
        return recursively_sub_anchors(finished_text, remaining_text, link_map, pattern)


def insert_links_in_line(link_map, line):
    pattern = build_model_match_pattern(link_map.keys())
    return recursively_sub_anchors('', line, link_map, pattern)


def get_dbt_project_path(absolute_path):
    parent_dir = os.path.abspath(os.path.join(absolute_path, os.pardir))
    file_names = [f for f in glob.glob(parent_dir + "/dbt_project.yml", recursive=True)]
    if file_names:
        return parent_dir
    else:
        return get_dbt_project_path(parent_dir)


def get_project_name(project_path):
    return project_path.split('/')[-1]


def parse_args():
    parser = argparse.ArgumentParser(description="Make anchor tags for your dbt docs")
    parser.add_argument(
        '-p',
        '--path',
        help="absolute path to file to be modified",
        type=str,
        required=True,
    )
    return parser.parse_args()


def re_write_file(absolute_path):
    project_path = get_dbt_project_path(absolute_path)
    project_name = get_project_name(project_path)
    model_names = collect_linkable_file_names(project_path)
    link_map = make_link_map(model_names, project_name)

    transformed_lines = []
    with open(absolute_path) as f:
        for line in f:
            transformed_lines.append(insert_links_in_line(link_map, line))

    with open(absolute_path, 'w') as f:
        f.writelines(transformed_lines)


if __name__ == '__main__':
    path = parse_args().path
    re_write_file(path)
