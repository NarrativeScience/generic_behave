from behave.__main__ import main as behave_main


def lambda_handler(event, context):
    try:
        exit_code = behave_main(
            "--tags=tests-replicated "
            "-D environment='https://replicated-test.n-s.internal/' "
            "tests_replicated/src/ns_tests_replicated"
        )
        return {
            "status_code": 200,
            "exit_code": exit_code,
            "body": "SUCCESS"
        }
    except:
        return {
            "status_code": 400,
            "body": "FAILURE"
        }



if __name__ == "__main__":
    print(lambda_handler(None, None))
