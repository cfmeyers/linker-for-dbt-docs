def make_link(project_name, model_name):
    if '.' in model_name:
        file_name = model_name.replace('.', '_', 1)
        display_name = model_name
    else:
        file_name = model_name
        display_name = model_name.replace('_', '.', 1)
    return f'<a href="#!/model/model.{project_name}.{file_name}">{display_name}</a>'


if __name__ == '__main__':
    pass
