"""Functions for globally common environment actions used by before and after behave hooks

Keeping this file clean with only global functions is very important for dependency management.
We do not want to load dependencies in test environments that are not needed. Specific functions for
very specific actions should be kept somewhere else.
"""
# Ignoring prints in this file
# flake8: noqa
import logging

import ansicolor
from behave.model import Feature, Scenario
from behave.runner import Context
import coloredlogs

# initialize a logger
LOGGER = logging.getLogger(__name__)


def setup_logging(ctx: Context) -> None:
    """Function that sets up logging by setting the behave logger. Creates a custom logging format

    Args:
        ctx: The behave context Object

    """
    default_field_styles = dict(
        asctime=dict(color=100),
        hostname=dict(color="magenta"),
        levelname=dict(color=53, bold=True),
        name=dict(color="blue"),
        programname=dict(color="cyan"),
        username=dict(color="yellow"),
    )

    default_level_styles = dict(
        spam=dict(color="green", faint=True),
        debug=dict(color=25),  # DeepSkyBlue4
        verbose=dict(color="green"),
        info=dict(color=248),
        notice=dict(color="magenta"),
        warning=dict(color=172),
        success=dict(color="green", bold=True),
        error=dict(color=196),
        critical=dict(color=52, bold=True),
    )

    # Custom format for logging levels DEBUG and higher
    coloredlogs.install(
        level=ctx.config.logging_level,
        logger=logging.getLogger(),
        fmt=ctx.config.logging_format,
        datefmt=ctx.config.logging_datefmt,
        field_styles=default_field_styles,
        level_styles=default_level_styles,
    )

    # Override the requests loggers and set to WARNING only
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("botocore.hooks").setLevel(logging.WARNING)
    logging.getLogger("botocore.loaders").setLevel(logging.WARNING)
    logging.getLogger("botocore.endpoint").setLevel(logging.WARNING)
    logging.getLogger("botocore.client").setLevel(logging.WARNING)
    logging.getLogger("botocore.credentials").setLevel(logging.WARNING)
    logging.getLogger("botocore.auth").setLevel(logging.WARNING)
    logging.getLogger("botocore.parsers").setLevel(logging.WARNING)
    logging.getLogger("botocore.retryhandler").setLevel(logging.WARNING)
    logging.getLogger("behave-debug").setLevel(logging.DEBUG)

    # Log the log mode
    LOGGER.debug(f"Logging initialized. Log mode: {ctx.config.logging_level}")


def set_user_data(ctx: Context) -> None:
    """Grabs behave user data from the config file and saves it to the context

    Args:
        ctx: The behave context

    """
    LOGGER.debug("Setting user data from the behave.ini config")
    user_data = ctx.config.userdata
    ctx.environment = user_data.get("environment", "ci")
    LOGGER.debug(f"User data: {user_data}")


def run_setup_tags(ctx: Context, feature: Feature) -> None:
    """Handles setup and teardown tags on scenarios in feature files.

     If @setup or @teardown is present it handles them separately than normal tags.
     These tags will be run before and after entire feature by inserting the steps into
     behave runner via the step executor attached to the context. This is the only way to
     do this so the setup and teardown "scenario" is not counted towards the test results.

     @setup tags are run now in this function.
     @teardown tags are placed on the context in the root layer to be run in the `after feature` hook

    Args:
        ctx: The behave context
        feature: The behave feature

    """
    remaining_scenarios = []
    ctx.teardown_scenarios = []
    # Check each feature to see if we have setup or teardown tags. Else they are normal scenarios
    for scenario in feature.scenarios:
        # Pipe the feature and scenario into the context so we can use it downstream in child steps
        ctx.feature = feature
        ctx.scenario = scenario
        if "setup" in scenario.tags:
            LOGGER.debug(
                "Setup scenario detected. Running it before the rest of the feature."
            )
            print(
                f"\n  {ansicolor.yellow('@setup')}\n  Scenario: {scenario.name}"
            )  # noqa
            # Run the steps in the setup scenario as setup
            execute_scenario_by_steps(ctx, scenario)
        elif "teardown" in scenario.tags:
            LOGGER.debug(
                "Teardown scenario detected. Saving it so we can run as cleanup after the rest of the feature."
            )
            ctx.teardown_scenarios.append(scenario)
        else:
            remaining_scenarios.append(scenario)
    feature.scenarios = remaining_scenarios


def run_teardown_tags(ctx: Context, feature: Feature) -> None:
    """Run all the teardown scenarios that were identified in `before_feature`

    Args:
        ctx: The behave context
        feature: The behave feature object

    """
    for scenario in ctx.teardown_scenarios:
        LOGGER.debug(
            "Teardown scenario found in teardown list. Running it now that our feature is complete."
        )
        # Pipe the scenario into the context so we can use it downstream in child steps
        ctx.feature = feature
        ctx.scenario = scenario
        # Execute the steps of each scenario as teardown
        print(
            f"\n  {ansicolor.yellow('@teardown')}\n  Scenario: {scenario.name}"
        )  # noqa
        execute_scenario_by_steps(ctx, scenario)


def execute_scenario_by_steps(ctx: Context, scenario: Scenario) -> None:
    """Step executor for setup and teardown tagged scenarios

    Args:
        ctx: The behave context
        scenario: The behave scenario object

    """
    # Set an empty list of steps to run
    parsed_steps = []
    # For each step put the step in the parsed list
    for step in scenario.steps:
        parsed_steps.append(f"{step.keyword} {step.name}")
        # check to see if we have a table with our step. If we do make sure we put the headings
        # and rows into the parsed steps list so we execute the full step
        if step.table:
            heading_string = ""
            for heading in step.table.headings:
                heading_string += f"{heading}|"
            parsed_steps.append(f"|{heading_string}")
            for row in step.table.rows:
                row_string = "|".join(row.cells)
                parsed_steps.append(f"|{row_string}|")
    steps_string = "\n".join(parsed_steps)
    for step in parsed_steps:
        print(ansicolor.green(f"    {step}"))  # noqa
    print("\n")  # noqa
    ctx.execute_steps(steps_string)
