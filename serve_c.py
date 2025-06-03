# serve_c.py
import ray
from ray import serve
import numpy as np
import os

if not ray.is_initialized():
    ray.init(address="auto", namespace="matrix_calc")

@serve.deployment(num_replicas=1) # <--- 移除 route_prefix
class C_Service:
    def __init__(self):
        print(f"C_Service initialized on PID: {os.getpid()} on node: {ray.worker.get_node_info_for_current_process()['node_ip_address']}")
        self.matrix_C = np.array([[0.5, 0.1], [0.2, 0.8]])
        print(f"C_Service: Fixed matrix C:\n{self.matrix_C}")

    async def __call__(self, input_matrix: np.ndarray) -> np.ndarray:
        print(f"C_Service: Received matrix from B:\n{input_matrix}")
        result_matrix_C = input_matrix @ self.matrix_C
        print(f"C_Service: Result after C's operation:\n{result_matrix_C}")
        return result_matrix_C

c_app = C_Service.bind()