from behave.__main__ import main as behave_main


def lambda_handler(event, context):
    try:
        exit_code = behave_main(
            "--tags=tests-replicated "
            "-D environment='https://replicated-test.n-s.internal/' "
            f"-D viz_version={event['version']} "
            "--logging-level=DEBUG "
            "ns_tests_replicated"
        )
        if exit_code == 0:
            return {
                "status_code": 200,
                "exit_code": exit_code,
                "body": "test ran with SUCCESS"
            }
        else:
            return{
                "status_code": 200,
                "exit_code": exit_code,
                "body": "test ran but FAILED"
            }
    except:
        return {
            "status_code": 400,
            "body": "FAILURE"
        }


if __name__ == "__main__":
    print(lambda_handler(None, None))
