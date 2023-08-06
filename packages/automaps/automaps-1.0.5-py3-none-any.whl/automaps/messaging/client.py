from copy import copy
from typing import Dict, Iterable, Tuple, Union

import zmq

import automapsconf


def ask_registry_for_idle_worker(frontend_uuid: str):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{automapsconf.PORT_REGISTRY}")

    socket.send_json({"command": "get_idle_worker", "frontend_uuid": frontend_uuid})

    message_from_registry = socket.recv_json()

    return message_from_registry


def ask_worker_for_steps(
    maptype_dict_key: str, job_uuid: str, worker_port: int
) -> Iterable[str]:
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{worker_port}")

    socket.send_json(
        {"event": "init_job", "init": maptype_dict_key, "job_uuid": job_uuid}
    )

    message_from_worker = socket.recv_json()

    return message_from_worker["steps"]


def send_job_finished_confirmation_to_worker(job_uuid: str, worker_port: int):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{worker_port}")

    socket.send_json({"event": "job_finished", "job_uuid": job_uuid})

    message_from_worker = socket.recv_json()

    return message_from_worker


def send_job_cancellation_to_worker(job_uuid: str, worker_port: int):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{worker_port}")

    socket.send_json({"event": "job_cancelled", "job_uuid": job_uuid})

    message_from_worker = socket.recv_json()

    return message_from_worker


def send_task_to_worker(
    maptype_dict_key: str,
    data: dict,
    print_layout: Union[str, Tuple[str, Dict[str, str]]],
    step: str,
    job_uuid: str,
    worker_port: int,
) -> dict:
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{worker_port}")

    data = copy(data)
    data["maptype_dict_key"] = maptype_dict_key
    data["step"] = step
    data["job_uuid"] = job_uuid
    data["event"] = "process_step"

    if isinstance(print_layout, str):
        data["print_layout"] = print_layout
    elif isinstance(print_layout, tuple) or isinstance(print_layout, list):
        print_layout = tuple(print_layout)  # type: ignore
        assert len(print_layout) == 2
        assert isinstance(print_layout[0], str)
        assert isinstance(print_layout[1], dict)
        data["print_layout"] = print_layout[1][data[print_layout[0]]]
    else:
        raise ValueError(
            f"MapType {maptype_dict_key} argument 'print_layout' has "
            f"wrong data type. It should be Union[str, Tuple[str, "
            f"Dict[str, str]]]."
        )

    socket.send_json(data)

    message_from_worker = socket.recv_json()

    return message_from_worker
