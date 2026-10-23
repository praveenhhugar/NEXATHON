# DECEPTOR AI: Shared Contract
Nobody changes a field name without telling the team.

## Data shapes
EVENT (sim -> backend)
{ "id": 1, "time": "2026-10-23T10:00:01", "source": "sim-1", "path": "/.env", "action": "GET", "payload": "" }

ASSESSMENT (Observer)
{ "event_id": 1, "risk": 55, "intent": "credential_harvesting", "confidence": 0.8, "mitre": "T1552" }

DECISION (Planner)
{ "id": 1, "action": "deploy_decoy", "strategy": "fake_config_trail", "reason": "...", "validated": true }

RESULT (Executor + Verifier)
{ "decision_id": 1, "status": "success", "honeytoken_hit": false, "steps_to_engage": null }

## Allowed actions (whitelist)
deploy_decoy, switch_strategy, plant_honeytoken, raise_logging, continue_monitoring

## Strategies
fake_admin_portal, fake_config_trail, fake_cloud_page

## Intents
normal, credential_harvesting, admin_probing, cloud_recon

## Routes
POST /event, GET /state, GET /ledger, GET /events, GET /strategies,
POST /token/verify, POST /simulate/start, POST /reset