from jinja2 import FileSystemLoader, Environment


def render(template_name, folder='templates', static_url='/static/', **kwargs):
    """
    :param static_url: basic folder for static
    :param template_name: Template name
    :param folder: Folder for searching template
    :param kwargs: Params for template
    :return:
    """
    # Set environment for templates loading
    env = Environment()

    # Loads templates from dir in the file system
    env.loader = FileSystemLoader(folder)

    env.globals['static'] = static_url

    # Use template that is chosen
    template = env.get_template(template_name)
        
    # Rendering template with params
    return template.render(**kwargs)
