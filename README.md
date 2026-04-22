# RHINO-OS — UGV Fleet Command & Control

**Open-source ground operations platform for Unmanned Ground Vehicle fleets.**

Built for modular UGVs like the Sirko-S1. Manages logistics, mine-laying, TROPIYA demining, reconnaissance and electronic warfare from a single tactical HUD.

> The ground equivalent of ARES-OS (FPV drones) — same philosophy, different domain.

## Live Demo
👉 [ares-os-app-7bb72773.base44.app/RhinoDemo](https://ares-os-app-7bb72773.base44.app/RhinoDemo)

## Features

| Module | Capability |
|--------|-----------|
| **Fleet HUD** | Real-time status of up to 20 UGVs — battery, speed, signal, payload |
| **Mission Dispatcher** | One-tap dispatch — selects module type, priority, payload description |
| **Module Switcher** | Logistics / Miner / Demining / Manipulator / Recon / EW |
| **Battery Manager** | Auto RTB trigger when battery drops below threshold |
| **TROPIYA Calculator** | Corridor length + safe distance from charge count + angle |
| **Tactical Map** | GPS-based topographic sector view with mission paths |
| **Mission Registry** | Full log of planned / active / completed / aborted missions |
| **Multi-channel comms** | LTE, Starlink, LRS, RFD, LoRa — all tracked per vehicle |

## Supported Modules

### 📦 Logistics
- Working payload: 130kg | Max: 200kg
- Range: up to 8km (LRS), 50km (Starlink)
- Auto route planning to waypoints

### 💣 Miner
- TM-62 (4 units), TM-124 (4 units), PTM-U (12 units)
- Sequential controlled drop via servo mechanism
- Area denial mission planning

### 🧹 Demining — TROPIYA
- Rocket-launched detonating cord
- Corridor clearance calculator: `corridor_m = charges × 12 × sin(angle) × 0.95`
- Safe distance: `safe_m = charges × 6.5`

### 🦾 Manipulator (SKIF)
- 2-DOF (elbow + grip) · CAN protocol
- Lift: 50kg | Tow: 150kg
- Remote hazardous material handling

### 👁 Recon
- Thermal imager + laser rangefinder + high-res optical
- Long-duration area surveillance
- 22Ah battery config for extended missions

### 📡 EW
- Electronic warfare payload
- Configurable frequency range
- Integrates with Silvus mesh radio

## Architecture

```
Field Operator (tablet/phone)
        ↓
RHINO-OS HUD (browser-based)
  → Fleet status polling (4s interval)
  → Mission dispatch → vehicle assignment
  → Battery monitor → auto RTB at threshold
  → TROPIYA corridor calculator
        ↓
Vehicle telemetry link (LTE / Starlink / LRS)
        ↓
UGV on-board controller (MAVLink / proprietary)
        ↓
Physical mission execution (edge autonomous)
```

## Vehicle Entities

```json
{
  "vehicle_id": "RHN-01",
  "status": "InMission",
  "module": "Logistics",
  "battery_pct": 78,
  "battery_ah": 60,
  "lat": 48.3755,
  "lon": 31.1583,
  "speed_kmh": 6.4,
  "payload_kg": 130,
  "signal_channel": "LRS",
  "signal_strength": 78,
  "range_km": 13,
  "mission_id": "MSN-001",
  "alert": ""
}
```

## Roadmap

| Phase | Item | Status |
|-------|------|--------|
| Q2 2026 | RHINO-OS field test with Sirko-S1 unit | 🔜 |
| Q2 2026 | MAVLink telemetry integration | 🔜 |
| Q3 2026 | Automatic waypoint generation from grid coordinates | 🔜 |
| Q3 2026 | Multi-vehicle convoy mode | 🔜 |
| Q4 2026 | TROPIYA pattern optimizer (terrain-aware) | 🔜 |
| Q4 2026 | Integration with ARES-OS for joint air/ground ops | 🔜 |

## License
MIT — free forever. No commercial agenda.

## Contact
worldindustries.tech | info@worldindustries.tech
