# serve_b.py
import ray
from ray import serve
import numpy as np
import os
import time

if not ray.is_initialized():
    ray.init(address="auto", namespace="matrix_calc")

@serve.deployment(num_replicas=1) # <--- 移除 route_prefix
class B_Service:
    def __init__(self, c_service_handle):
        print(f"B_Service initialized on PID: {os.getpid()} on node: {ray.worker.get_node_info_for_current_process()['node_ip_address']}")
        self.matrix_B = np.array([[1.0, 2.0], [3.0, 4.0]])
        print(f"B_Service: Fixed matrix B:\n{self.matrix_B}")
        self.c_service_handle = c_service_handle
        print(f"B_Service: Acquired handle to C_Service: {self.c_service_handle}")

    async def __call__(self, input_matrix: np.ndarray) -> ray.ObjectRef:
        print(f"B_Service: Received matrix from A:\n{input_matrix}")
        result_matrix_B = input_matrix @ self.matrix_B
        print(f"B_Service: Result after B's operation:\n{result_matrix_B}")

        print("B_Service: Forwarding result to C_Service...")
        final_result_ref = await self.c_service_handle.remote(result_matrix_B)
        print("B_Service: Forwarded, returning C's ObjectRef.")
        return final_result_ref

b_app = B_Service.bind(None)