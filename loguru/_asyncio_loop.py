import asyncio


def load_loop_functions():
    def get_task_loop(task):
        return task.get_loop()

    get_running_loop = asyncio.get_running_loop
    return get_task_loop, get_running_loop


get_task_loop, get_running_loop = load_loop_functions()
