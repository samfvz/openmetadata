# https://discourse.prefect.io/t/passing-context-when-triggering-a-deployment-from-an-automation/2850/3
from prefect import flow, task, context
from prefect.deployments import Deployment


@task(name="[Generic] Print passed parameters")
def print_hello(name):
    msg = f"Hello {name}!"
    print(msg)
    return msg


@flow(name="[Generic] Main Flow")
def hello_world(parameters):
    # c = context.get_run_context()
    print(f"===== Parameters ====:{parameters}")
    # flow_id = c.flow_run.flow_id
    # print(flow_id)
    # message = print_hello(name)


def deploy():
    deployment = Deployment.build_from_flow(
        flow=hello_world,
        name="generic-deployment"
    )
    deployment.apply()


if __name__ == "__main__":
    deploy()