from cookiecutter.main import cookiecutter

from aoricaan_cli.src.utils.debugger import Debug


def generate_templates(package):
    """
    Generates the templates for the project.
    """
    try:
        cookiecutter(template=package)
    except Exception as e:
        Debug.error(f"{e}")
        Debug.error(f"The template could not be generated.")


def generate_standard_template():
    """
    Generates the standard template for the project.
    """
    generate_templates("https://github.com/aoricaan/apm-template.git")
