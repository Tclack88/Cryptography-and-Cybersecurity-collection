import os
from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

COMPONENTS = [
    {"id": "api-gw", "name": "API Gateway", "group": "Edge", "status": "operational"},
    {"id": "console", "name": "Web Console", "group": "Edge", "status": "operational"},
    {"id": "auth", "name": "Authentication Service", "group": "Core", "status": "operational"},
    {"id": "telemetry", "name": "Vessel Telemetry Ingest", "group": "Core", "status": "degraded"},
    {"id": "position", "name": "Position Reporting", "group": "Core", "status": "operational"},
    {"id": "notify", "name": "Notification Service", "group": "Core", "status": "operational"},
    {"id": "warehouse", "name": "Data Warehouse", "group": "Data", "status": "operational"},
    {"id": "object", "name": "Object Storage (hal-s3)", "group": "Data", "status": "operational"},
    {"id": "scheduler", "name": "Job Scheduler", "group": "Platform", "status": "operational"},
    {"id": "registry", "name": "Container Registry", "group": "Platform", "status": "operational"},
]

def get_incidents():
    flag = os.environ.get("FLAG", "SVIBGR{t3st_fl4g}")
    dt = lambda **kw: (datetime.now(timezone.utc).replace(microsecond=0) - timedelta(**kw)).isoformat().replace("+00:00", "Z")
    
    return [
        {"id": 218, "title": "Elevated 502 errors on API Gateway (eu-west-2)", "status": "resolved", "impact": "minor", "public": True, "affected": ["api-gw"], "created_at": dt(days=2), "resolved_at": dt(hours=45), "updates": [{"ts": dt(days=2), "label": "Investigating", "body": "We are seeing elevated 502 response codes from API Gateway in eu-west-2. Investigating upstream connectivity."}, {"ts": dt(hours=46), "label": "Identified", "body": "Root cause identified as a misconfigured health check on the new ingress fleet. Rolling back."}, {"ts": dt(hours=45), "label": "Resolved", "body": "Rollback complete. Error rates back to baseline. We will publish a postmortem within 5 business days."}]},
        {"id": 217, "title": "Vessel Telemetry Ingest: degraded throughput", "status": "monitoring", "impact": "minor", "public": True, "affected": ["telemetry"], "created_at": dt(hours=6), "updates": [{"ts": dt(hours=6), "label": "Investigating", "body": "Telemetry ingest is processing at approximately 70% of normal throughput. Backlog is being drained."}, {"ts": dt(hours=2), "label": "Monitoring", "body": "Throughput recovered. Monitoring queue depth."}]},
        {"id": 216, "title": "Scheduled maintenance: database failover testing", "status": "completed", "impact": "maintenance", "public": True, "affected": ["warehouse", "position"], "created_at": dt(days=7), "resolved_at": dt(days=7), "updates": [{"ts": dt(days=8), "label": "Scheduled", "body": "We will exercise failover on the warehouse primary at 02:00 UTC. Expected impact: 1-2 minutes of read-only mode."}, {"ts": dt(days=7), "label": "Completed", "body": "Failover completed with 47 seconds of read-only operation. No customer-visible errors."}]},
        {"id": 215, "title": "Authentication delays during morning peak", "status": "resolved", "impact": "minor", "public": True, "affected": ["auth"], "created_at": dt(days=14), "resolved_at": dt(days=14), "updates": [{"ts": dt(days=14), "label": "Identified", "body": "Auth latency p99 climbed to 1.2s during the 08:00-08:25 UTC peak. Cause: cold cache after deploy."}, {"ts": dt(days=14), "label": "Resolved", "body": "Cache warmed. Latency is back to baseline, under 120ms p99."}]},
        {"id": 213, "title": "Object Storage replication lag in us-east-1", "status": "resolved", "impact": "minor", "public": True, "affected": ["object"], "created_at": dt(days=23), "resolved_at": dt(days=23), "updates": [{"ts": dt(days=23), "label": "Resolved", "body": "Cross-region replication briefly exceeded 60 seconds of lag. Replication queue drained and all objects are consistent."}]},
        {"id": 219, "title": "[INTERNAL] Retro: customer-data anomaly", "status": "monitoring", "impact": "critical", "public": False, "affected": ["warehouse"], "created_at": dt(hours=72), "updates": [{"ts": dt(hours=72), "label": "Identified", "body": "Anomalous read pattern from service account svc-analytics-ro touched customer rows outside the scoped tenant."}, {"ts": dt(hours=70), "label": "Containment", "body": "Service account rotated. Tenant isolation policy patched. Comms drafted but not sent pending Legal review."}, {"ts": dt(hours=36), "label": "Postmortem", "body": f"Action item tracking token, do not share externally: {flag}"}]},
        {"id": 214, "title": "[INTERNAL] Pen test finding: incident feed authorization", "status": "investigating", "impact": "major", "public": False, "affected": ["api-gw"], "created_at": dt(days=11), "updates": [{"ts": dt(days=11), "label": "Filed", "body": "Third-party assessment reproduced improper object filtering on GET /api/incidents."}, {"ts": dt(days=10), "label": "Owner", "body": "Ticket assigned to platform-edge. Public consumers should not be able to select internal incident visibility."}]},
        {"id": 212, "title": "[INTERNAL] Staging credential leak, resolved", "status": "resolved", "impact": "major", "public": False, "affected": ["auth"], "created_at": dt(days=28), "resolved_at": dt(days=27), "updates": [{"ts": dt(days=28), "label": "Identified", "body": "Engineer pushed a staging .env file to a public gist. Keys rotated within 14 minutes."}, {"ts": dt(days=27), "label": "Resolved", "body": "All rotated credentials confirmed in use. Gist deleted."}]}
    ]

@app.after_request
def set_headers(response):
    response.headers.update({"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"})
    return response

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/status")
def api_status():
    stats = [c["status"] for c in COMPONENTS]
    overall = "major_outage" if "outage" in stats else "partial_degradation" if "degraded" in stats else "operational"
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return jsonify({"overall": overall, "updated_at": now})

@app.get("/api/components")
def api_components():
    return jsonify({"components": COMPONENTS})

@app.get("/api/uptime")
def api_uptime():
    today = datetime.now(timezone.utc).date()
    series = []
    for i, comp in enumerate(COMPONENTS):
        # Seeded Random Inline
        state = len(comp["id"]) * 7919 + i * 31
        days = []
        for offset in range(89, -1, -1):
            state = (state * 9301 + 49297) % 233280
            roll = state / 233280
            status = "operational"
            if comp["id"] == "telemetry" and offset <= 1: status = "degraded"
            elif roll > 0.985: status = "outage"
            elif roll > 0.95: status = "degraded"
            days.append({"date": (today - timedelta(days=offset)).isoformat(), "status": status})
        
        uptime = f"{((len(days) - sum(1 for d in days if d['status'] != 'operational')) / len(days)) * 100:.3f}"
        series.append({"component_id": comp["id"], "days": days, "uptime_pct": uptime})
    return jsonify({"range_days": 90, "series": series})

@app.get("/api/incidents")
def api_incidents():
    v = request.args.get("public")
    data = get_incidents()
    
    if v is None: selected = data
    elif v.lower() in {"1", "true", "yes"}: selected = [i for i in data if i["public"]]
    elif v.lower() in {"0", "false", "no"}: selected = [i for i in data if not i["public"]]
    else: selected = [i for i in data if i["public"]]

    return jsonify({"count": len(selected), "incidents": sorted(selected, key=lambda x: x["created_at"], reverse=True)})

@app.get("/api/subscribers/count")
def api_subscribers_count():
    return jsonify({"email": 18421, "webhook": 312, "rss": 2104})

@app.errorhandler(404)
@app.errorhandler(405)
def handle_error(e):
    return jsonify({"error": e.name.lower()}), e.code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
