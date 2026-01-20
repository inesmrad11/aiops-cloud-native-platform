"""
Simulateur d'incidents pour démonstration AIOps
"""
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List

class IncidentSimulator:
    def __init__(self):
        self.incident_types = [
            "cpu_spike",
            "memory_leak", 
            "high_latency",
            "service_outage",
            "database_slow_queries",
            "network_partition",
            "disk_io_bottleneck",
            "api_rate_limit",
            "cache_miss_storm",
            "dependency_failure"
        ]
        
        self.services = ["api-gateway", "user-service", "payment-service", "notification-service"]
    
    def generate_incident(self) -> Dict[str, Any]:
        """Génère un incident réaliste"""
        incident_type = random.choice(self.incident_types)
        severity = random.choices(["low", "medium", "high"], weights=[0.5, 0.35, 0.15])[0]
        affected_service = random.choice(self.services)
        
        incident_templates = {
            "cpu_spike": {
                "title": f"CPU Spike detected in {affected_service}",
                "description": f"CPU usage increased to {random.randint(85, 99)}% in {affected_service} pods",
                "indicators": ["high_cpu_usage", "increased_errors", "slow_response"]
            },
            "memory_leak": {
                "title": f"Potential Memory Leak in {affected_service}",
                "description": f"Memory usage growing steadily over time, currently at {random.randint(88, 98)}%",
                "indicators": ["rising_memory", "increased_gc", "pod_restarts"]
            },
            "high_latency": {
                "title": f"High Latency detected for {affected_service}",
                "description": f"P95 latency increased to {random.randint(500, 2000)}ms",
                "indicators": ["slow_requests", "timeout_errors", "queue_backlog"]
            },
            "service_outage": {
                "title": f"Partial Outage: {affected_service}",
                "description": f"{random.randint(30, 70)}% of {affected_service} pods are not responding",
                "indicators": ["high_error_rate", "zero_traffic", "health_check_fails"]
            },
            "database_slow_queries": {
                "title": "Database Performance Degradation",
                "description": f"Slow queries detected, avg query time: {random.randint(200, 1000)}ms",
                "indicators": ["slow_queries", "connection_pool_exhausted", "lock_wait_time"]
            }
        }
        
        # Utiliser le template ou créer un générique
        if incident_type in incident_templates:
            template = incident_templates[incident_type]
        else:
            template = {
                "title": f"{incident_type.replace('_', ' ').title()} detected",
                "description": f"Incident of type {incident_type} affecting {affected_service}",
                "indicators": ["monitoring_alert", "metric_anomaly", "user_report"]
            }
        
        # Temps de détection (simule un délai entre l'incident et la détection)
        incident_start = datetime.utcnow() - timedelta(minutes=random.randint(5, 60))
        
        return {
            "incident_id": f"inc-{random.randint(10000, 99999)}",
            "incident_type": incident_type,
            "title": template["title"],
            "description": template["description"],
            "severity": severity,
            "affected_service": affected_service,
            "indicators": template["indicators"],
            "detection_time": datetime.utcnow().isoformat(),
            "incident_start_time": incident_start.isoformat(),
            "status": "detected",  # detected, investigating, resolved
            "assigned_team": random.choice(["sre-team", "backend-team", "database-team"]),
            "priority": {"low": "P3", "medium": "P2", "high": "P1"}[severity]
        }
    
    def get_suggested_actions(self, incident_type: str) -> List[str]:
        """Retourne des actions suggérées basées sur le type d'incident"""
        actions_map = {
            "cpu_spike": [
                "Check pod resource limits",
                "Analyze recent code deployments",
                "Scale horizontally the affected service",
                "Review monitoring dashboards for correlation"
            ],
            "memory_leak": [
                "Analyze heap dumps",
                "Check for unbounded collections",
                "Review garbage collector logs",
                "Consider restarting affected pods"
            ],
            "high_latency": [
                "Check downstream dependencies",
                "Review database query performance",
                "Analyze network metrics",
                "Check for rate limiting"
            ],
            "service_outage": [
                "Check Kubernetes pod status",
                "Verify service configuration",
                "Check dependency health",
                "Review recent changes"
            ],
            "database_slow_queries": [
                "Check database load",
                "Review query execution plans",
                "Check for missing indexes",
                "Analyze lock contention"
            ]
        }
        
        return actions_map.get(incident_type, [
            "Review application logs",
            "Check system metrics",
            "Verify configuration",
            "Consult runbooks"
        ])