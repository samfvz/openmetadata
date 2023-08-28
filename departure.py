from prefect import flow, task
from prefect.context import get_run_context


@task(name="[Department1] Get Parameters Task")
def get_parameters():
    params = {
        "cpu": 6,
        "ram": 32,
        "notebook": "/some/path/notebook"
    }
    result = "AAAAAA"

    return result


@flow(name="[Department1] Main Flow")
def department1_flow():
    get_parameters(return_state=True)
    # state = get_parameters(return_state=True)
    # print(f"sate_result: {state.result()}")
    # flow_run_context = get_run_context()
    # flow_run_context.flow_run.context['custom_params']: state.result()
    # print(flow_run_context.flow_run)
    # return "AAAAAAAAAA"


if __name__ == "__main__":
    flow_run_state = department1_flow()
    print(flow_run_state)