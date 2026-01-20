"""
Générateur de métriques réalistes pour simulation AIOps
"""
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
import uuid

class MetricsGenerator:
    def __init__(self):
        self.services = ["api-gateway", "user-service", "payment-service", "notification-service"]
        self.metrics_base = {
            "api-gateway": {"cpu": 40, "memory": 60, "latency": 50},
            "user-service": {"cpu": 30, "memory": 50, "latency": 30},
            "payment-service": {"cpu": 60, "memory": 70, "latency": 100},
            "notification-service": {"cpu": 25, "memory": 40, "latency": 20}
        }
    
    def generate_current_metrics(self) -> Dict[str, Any]:
        """Génère des métriques système actuelles réalistes"""
        # Ajouter de la variation aléatoire
        variation = random.uniform(-15, 15)
        
        metrics = {}
        overall_cpu = 0
        overall_memory = 0
        overall_latency = 0
        
        for service in self.services:
            base = self.metrics_base[service]
            
            # Simuler des patterns réels (ex: payment-service a souvent plus de CPU)
            if service == "payment-service" and random.random() > 0.7:
                cpu_spike = random.uniform(20, 40)
                latency_spike = random.uniform(50, 150)
            else:
                cpu_spike = 0
                latency_spike = 0
            
            service_metrics = {
                "cpu_usage_percent": max(5, min(95, base["cpu"] + variation + cpu_spike)),
                "memory_usage_percent": max(10, min(90, base["memory"] + random.uniform(-10, 10))),
                "latency_ms": max(10, base["latency"] + random.uniform(-20, 20) + latency_spike),
                "request_rate": random.randint(100, 1000),
                "error_rate": random.uniform(0.1, 2.5),  # 0.1% à 2.5%
                "pod_count": random.randint(2, 5)
            }
            
            metrics[service] = service_metrics
            
            # Calcul des moyennes globales
            overall_cpu += service_metrics["cpu_usage_percent"]
            overall_memory += service_metrics["memory_usage_percent"]
            overall_latency += service_metrics["latency_ms"]
        
        # Métriques système globales
        num_services = len(self.services)
        
        # Détecter une anomalie potentielle (1 chance sur 4)
        has_anomaly = random.random() > 0.75
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "services": metrics,
            "system_wide": {
                "total_cpu_usage_percent": round(overall_cpu / num_services, 2),
                "total_memory_usage_percent": round(overall_memory / num_services, 2),
                "average_latency_ms": round(overall_latency / num_services, 2),
                "total_requests_per_second": random.randint(2000, 5000),
                "active_connections": random.randint(500, 2000)
            },
            "anomaly_detection": {
                "has_anomaly": has_anomaly,
                "anomaly_score": random.uniform(0, 1) if has_anomaly else random.uniform(0, 0.3),
                "suspected_service": random.choice(self.services) if has_anomaly else None
            },
            "overall_status": "degraded" if has_anomaly else "healthy"
        }
    
    def generate_log_entry(self) -> Dict[str, Any]:
        """Génère une entrée de log réaliste"""
        log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
        levels_weights = [0.7, 0.15, 0.1, 0.05]  # INFO plus fréquent
        
        log_level = random.choices(log_levels, weights=levels_weights)[0]
        
        templates = {
            "INFO": [
                "User {user_id} logged in successfully",
                "Processed request {request_id} in {time}ms",
                "Cache updated for key: {key}",
                "Database connection pool size: {size}",
                "Scheduled task {task_name} completed"
            ],
            "WARNING": [
                "High memory usage detected in pod {pod_name}",
                "Response time above threshold for endpoint {endpoint}",
                "Retrying connection to {service} (attempt {attempt})",
                "Cache miss rate increased to {rate}%"
            ],
            "ERROR": [
                "Failed to connect to database: {error}",
                "Payment processing failed for order {order_id}",
                "External API {api_name} returned 5xx error",
                "Kubernetes pod {pod_name} crash loop detected"
            ],
            "DEBUG": [
                "Entering function {function_name}",
                "Variable {var_name} value: {value}",
                "Starting processing of batch {batch_id}"
            ]
        }
        
        message_template = random.choice(templates[log_level])
        
        # Remplir les variables du template
        message = message_template.format(
            user_id=f"user-{random.randint(1000, 9999)}",
            request_id=str(uuid.uuid4())[:8],
            time=random.randint(10, 500),
            key=f"cache_key_{random.randint(1, 100)}",
            size=random.randint(10, 50),
            task_name=random.choice(["cleanup", "backup", "report"]),
            pod_name=f"pod-{random.choice(['a', 'b', 'c'])}-{random.randint(1, 10)}",
            endpoint=random.choice(["/api/users", "/api/payments", "/api/notifications"]),
            service=random.choice(["redis", "database", "payment-gateway"]),
            attempt=random.randint(1, 3),
            rate=random.uniform(5, 25),
            error=random.choice(["connection timeout", "authentication failed", "query execution error"]),
            order_id=f"order-{random.randint(10000, 99999)}",
            api_name=random.choice(["stripe", "sendgrid", "auth0"]),
            function_name=random.choice(["process_payment", "validate_user", "send_notification"]),
            var_name=random.choice(["user_count", "total_amount", "retry_count"]),
            value=random.randint(1, 100),
            batch_id=random.randint(1, 1000)
        )
        
        return {
            "timestamp": (datetime.utcnow() - timedelta(seconds=random.randint(0, 300))).isoformat(),
            "level": log_level,
            "message": message,
            "service": random.choice(self.services),
            "trace_id": f"trace-{str(uuid.uuid4())[:8]}",
            "span_id": f"span-{random.randint(1000, 9999)}",
            "host": f"host-{random.choice(['a', 'b', 'c'])}",
            "namespace": "aiops-demo"
        }