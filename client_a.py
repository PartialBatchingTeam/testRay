# client_a.py
import ray
from ray import serve
import numpy as np
import time
import os

# 导入服务定义
from serve_c import C_Service
from serve_b import B_Service

# 1. 初始化 Ray 集群 (在单机模拟中，直接启动本地集群)
# Ray Client 端口 10001 和 Dashboard 端口 8265 默认会使用
if not ray.is_initialized():
    print("Client A: Initializing local Ray cluster...")
    ray.init(address="auto", namespace="matrix_calc") # "auto" 会连接到已存在的Ray，或启动一个新的本地Ray

print(f"Client A: Ray initialized. Head node address: {ray.get_processing_info().node.node_ip_address}")
# 对于本地集群，Dashboard 通常在 127.0.0.1:8265
print(f"Client A: Ray dashboard available at: http://127.0.0.1:8265")

# 2. 部署服务
print("Client A: Deploying C_Service...")
c_deployment = C_Service.bind()
c_app_handle = serve.run(c_deployment, name="C_App", route_prefix="/c_service")
print(f"Client A: C_Service deployed as 'C_App'. Handle: {c_app_handle}")

print("Client A: Deploying B_Service...")
b_deployment = B_Service.bind(c_app_handle)
b_app_handle = serve.run(b_deployment, name="B_App", route_prefix="/b_service")
print(f"Client A: B_Service deployed as 'B_App'. Handle: {b_app_handle}")

# 等待服务启动并变得可用
print("Client A: Waiting for deployments to be ready (5 seconds)...")
time.sleep(5)

print("\n--- Ray Cluster Status (Optional, for debugging) ---")
print(f"Current node IP: {ray.get_processing_info().node.node_ip_address}")
print(f"All nodes in cluster: {ray.nodes()}")
print("----------------------------------------------------\n")


# 3. A 机器生成初始矩阵
initial_matrix_A = np.array([[1.0, 2.0], [3.0, 4.0]])
print(f"\nClient A: Initial matrix generated:\n{initial_matrix_A}")

# 4. A 机器将矩阵发送给 B 机器
print("Client A: Sending initial matrix to B_Service...")
result_ref = b_app_handle.remote(initial_matrix_A)

# 5. A 机器等待并接收最终结果
print("Client A: Waiting for final result from C_Service (via B_Service)...")
final_result_matrix = ray.get(result_ref)

print("\n------------------------------------------------")
print(f"Client A: Final result received from C_Service:\n{final_result_matrix}")
print("------------------------------------------------")

# 6. 关闭 Ray Serve 应用
print("Client A: Shutting down Ray Serve apps...")
serve.shutdown()
print("Client A: Ray Serve apps shut down.")

# 7. 关闭 Ray 集群 (仅在本地测试时需要，生产集群通常不会由客户端关闭)
ray.shutdown()
print("Client A: Ray cluster shut down.")