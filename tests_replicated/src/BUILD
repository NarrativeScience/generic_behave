python_library(
    name="lib",
    dependencies=[
        "3rdparty/python:ansicolor",
        "3rdparty/python:behave",
        "3rdparty/python:boto3",
        "3rdparty/python:requests",
        "src",
    ],
    sources=["ns_tests_replicated/**/*"],
    tags={".", "code", "python"},
)
python_binary(
    name="tests_replicated",
    dependencies=[":lib"],
    source="ns_tests_replicated/behave_cli.py",
    tags={".", "code", "python"},
)
