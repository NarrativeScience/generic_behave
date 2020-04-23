python_library(
    name="lambda-python-{{ cookiecutter.project_name }}-lib",
    sources=globs("lambda_handler/**/*"),
    dependencies=[
        # Add dependencies here
        {% if cookiecutter.is_cf_custom_resource == "yes" -%}
        "lib/cf_custom_resources/src",
        {% endif -%}
        "lib/python_core/src",
        "lib/python_logger/src",
        # Example third-party dependency:
        # "3rdparty/python:requests",
    ],
)
python_binary(
    name="lambda-python-{{ cookiecutter.project_name }}-bin",
    source="lambda_handler/lambda_handler.py",
    dependencies=[":lambda-python-{{ cookiecutter.project_name }}-lib"],
)
python_awslambda(
    name="lambda-python-{{ cookiecutter.project_name }}",
    binary=":lambda-python-{{ cookiecutter.project_name }}-bin",
    handler="lambda_handler.lambda_handler:lambda_handler",
)
