"""
AIOps Metrics Simulator - Simule un environnement de production avec métriques et incidents
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import random
import logging
from typing import List, Dict, Any
import uuid

from src.metrics_generator import MetricsGenerator
from src.incident_simulator import IncidentSimulator

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AIOps Metrics Simulator",
    description="Simulateur de métriques et incidents pour plateforme AIOps",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialisation des générateurs
metrics_gen = MetricsGenerator()
incident_sim = IncidentSimulator()

# Store pour l'historique (en mémoire, simple pour la démo)
metrics_history = []
incidents_history = []

@app.get("/", tags=["Root"])
async def root():
    """Endpoint racine - Présentation de la plateforme"""
    return {
        "application": "AIOps Metrics Simulator",
        "version": "1.0.0",
        "status": "operational",
        "description": "Simulateur de métriques et incidents pour démonstration AIOps",
        "endpoints": {
            "health": "/health - Vérification santé",
            "metrics": "/metrics/current - Métriques actuelles",
            "metrics_history": "/metrics/history - Historique métriques",
            "simulate_incident": "/incidents/simulate - Simuler un incident",
            "incidents": "/incidents - Liste incidents simulés",
            "system_info": "/system/info - Info système simulée"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health", tags=["Monitoring"])
async def health_check():
    """Vérification de santé de l'application"""
    return {
        "status": "healthy",
        "service": "aiops-simulator",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": "100%",
        "dependencies": {
            "database": "simulated",
            "cache": "simulated",
            "external_apis": "simulated"
        }
    }

@app.get("/metrics/current", tags=["Metrics"])
async def get_current_metrics():
    """Récupère les métriques système actuelles simulées"""
    try:
        metrics = metrics_gen.generate_current_metrics()
        
        # Stocker dans l'historique
        metrics_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": metrics
        })
        
        # Garder seulement les 100 derniers points
        if len(metrics_history) > 100:
            metrics_history.pop(0)
        
        logger.info(f"Generated metrics: {metrics['overall_status']}")
        
        return JSONResponse(content=metrics)
    except Exception as e:
        logger.error(f"Error generating metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics/history", tags=["Metrics"])
async def get_metrics_history(limit: int = 20):
    """Récupère l'historique des métriques"""
    if limit > 100:
        limit = 100
    
    recent_history = metrics_history[-limit:] if metrics_history else []
    
    return {
        "count": len(recent_history),
        "limit": limit,
        "data": recent_history,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/incidents/simulate", tags=["Incidents"])
async def simulate_incident():
    """Simule un incident AIOps (anomalie détectée)"""
    try:
        incident = incident_sim.generate_incident()
        
        # Ajouter à l'historique
        incidents_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "incident": incident
        })
        
        logger.warning(f"Simulated incident: {incident['incident_type']} - Severity: {incident['severity']}")
        
        return JSONResponse(content={
            "message": "Incident simulated successfully",
            "incident": incident,
            "suggested_actions": incident_sim.get_suggested_actions(incident['incident_type']),
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error simulating incident: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/incidents", tags=["Incidents"])
async def get_incidents(limit: int = 10):
    """Liste les incidents simulés"""
    if limit > 50:
        limit = 50
    
    recent_incidents = incidents_history[-limit:] if incidents_history else []
    
    return {
        "count": len(recent_incidents),
        "limit": limit,
        "data": recent_incidents,
        "summary": {
            "total_incidents": len(incidents_history),
            "high_severity": len([i for i in incidents_history if i['incident']['severity'] == 'high']),
            "resolved": len([i for i in incidents_history if i['incident'].get('resolved', False)])
        }
    }

@app.get("/system/info", tags=["System"])
async def get_system_info():
    """Informations sur le système simulé"""
    return {
        "environment": "simulated-production",
        "cluster": "aks-aiops-dev",
        "namespace": "aiops-demo",
        "services": [
            {"name": "api-gateway", "status": "running", "version": "v1.2.3"},
            {"name": "user-service", "status": "running", "version": "v2.1.0"},
            {"name": "payment-service", "status": "degraded", "version": "v1.5.2"},
            {"name": "notification-service", "status": "running", "version": "v1.0.1"}
        ],
        "nodes": [
            {"name": "node-1", "role": "worker", "zone": "francecentral-1"},
            {"name": "node-2", "role": "worker", "zone": "francecentral-2"}
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/logs/sample", tags=["Logs"])
async def get_sample_logs(count: int = 5):
    """Génère des logs d'application simulés"""
    logs = []
    for i in range(min(count, 20)):  # Max 20 logs
        logs.append(metrics_gen.generate_log_entry())
    
    return {
        "count": len(logs),
        "logs": logs,
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)