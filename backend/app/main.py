from fastapi import FastAPI
from kubernetes import client, config
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- CORS EKLENDİ ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Frontend -> backend erişimi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1) Kubernetes Config Yükleme ---
def load_kube():
    try:
        config.load_kube_config()   # Lokal geliştirme
    except Exception:
        config.load_incluster_config()  # Pod içinde çalışırken

# --- 2) CPU ve RAM Parsing Fonksiyonları ---
def parse_cpu(cpu_str):
    # nano cores (n)
    if cpu_str.endswith("n"):
        return int(cpu_str[:-1]) / 1_000_000_000

    # micro cores (u)
    if cpu_str.endswith("u"):
        return int(cpu_str[:-1]) / 1_000_000

    # millicores (m)
    if cpu_str.endswith("m"):
        return int(cpu_str[:-1]) / 1000

    # core (float)
    try:
        return float(cpu_str)
    except:
        return 0


def parse_memory(mem_str):
    if mem_str.endswith("Ki"):
        return int(mem_str[:-2]) * 1024 / (1024**3)  # Ki → GB
    if mem_str.endswith("Mi"):
        return int(mem_str[:-2]) / 1024             # Mi → GB
    if mem_str.endswith("Gi"):
        return int(mem_str[:-2])                    # Gi → GB
    return 0


CPU_PRICE = 0.045   # $/core-hour
MEM_PRICE = 0.005   # $/GB-hour


# --- 3) /pods/usage ---
@app.get("/pods/usage")
def pods_usage():
    load_kube()

    metrics_api = client.CustomObjectsApi()
    data = metrics_api.list_cluster_custom_object(
        group="metrics.k8s.io",
        version="v1beta1",
        plural="pods"
    )

    results = []
    for item in data["items"]:
        ns = item["metadata"]["namespace"]
        name = item["metadata"]["name"]
        cont = item["containers"][0]

        results.append({
            "namespace": ns,
            "pod": name,
            "cpu": cont["usage"]["cpu"],
            "memory": cont["usage"]["memory"]
        })

    return {"pods": results}


# --- 4) /pods/cost ---
@app.get("/pods/cost")
def pods_cost():
    load_kube()
    metrics_api = client.CustomObjectsApi()

    data = metrics_api.list_cluster_custom_object(
        group="metrics.k8s.io",
        version="v1beta1",
        plural="pods"
    )

    results = []

    for item in data["items"]:
        pod = item["metadata"]["name"]
        ns = item["metadata"]["namespace"]
        cont = item["containers"][0]

        cpu = parse_cpu(cont["usage"]["cpu"])
        mem = parse_memory(cont["usage"]["memory"])

        cost_cpu = cpu * CPU_PRICE
        cost_mem = mem * MEM_PRICE
        total = cost_cpu + cost_mem

        results.append({
            "namespace": ns,
            "pod": pod,
            "cpu_cores": cpu,
            "memory_gb": mem,
            "cpu_cost_per_hour": cost_cpu,
            "memory_cost_per_hour": cost_mem,
            "total_cost_per_hour": total
        })

    return {"costs": results}


# --- 5) Namespace bazlı toplam maliyet ---
@app.get("/namespaces/cost")
def namespace_cost():
    load_kube()
    metrics_api = client.CustomObjectsApi()

    data = metrics_api.list_cluster_custom_object(
        group="metrics.k8s.io",
        version="v1beta1",
        plural="pods"
    )

    ns_totals = {}

    for item in data["items"]:
        ns = item["metadata"]["namespace"]
        cont = item["containers"][0]

        cpu = parse_cpu(cont["usage"]["cpu"])
        mem = parse_memory(cont["usage"]["memory"])

        cost_cpu = cpu * CPU_PRICE
        cost_mem = mem * MEM_PRICE
        total = cost_cpu + cost_mem

        if ns not in ns_totals:
            ns_totals[ns] = {
                "cpu_cores": 0,
                "memory_gb": 0,
                "cpu_cost_per_hour": 0,
                "memory_cost_per_hour": 0,
                "total_cost_per_hour": 0
            }

        ns_totals[ns]["cpu_cores"] += cpu
        ns_totals[ns]["memory_gb"] += mem
        ns_totals[ns]["cpu_cost_per_hour"] += cost_cpu
        ns_totals[ns]["memory_cost_per_hour"] += cost_mem
        ns_totals[ns]["total_cost_per_hour"] += total

    return ns_totals
