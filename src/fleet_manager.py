"""
RHINO-OS Fleet Manager
Manages UGV fleet state, dispatches missions, monitors battery.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from math import radians, cos, sin, asin, sqrt


@dataclass
class UGV:
    vehicle_id: str
    status: str = "Standby"   # Standby | InMission | RTB | Charging | Lost
    module: str = "Logistics"  # Logistics | Miner | Demining | Manipulator | Recon | EW
    battery_pct: float = 100.0
    battery_ah: float = 60.0
    lat: float = 0.0
    lon: float = 0.0
    speed_kmh: float = 0.0
    payload_kg: float = 0.0
    signal_channel: str = "LTE"
    mission_id: Optional[str] = None
    alert: str = ""


@dataclass
class Mission:
    mission_id: str
    type: str
    status: str = "Planned"
    assigned_vehicle_id: Optional[str] = None
    payload_desc: str = ""
    priority: str = "HIGH"
    distance_km: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    completed_at: Optional[str] = None


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return R * 2 * asin(sqrt(a))


class FleetManager:
    def __init__(self, rtb_threshold: float = 20.0):
        self.fleet: List[UGV] = []
        self.missions: List[Mission] = []
        self.rtb_threshold = rtb_threshold  # battery % to trigger auto-RTB

    def add_vehicle(self, ugv: UGV):
        self.fleet.append(ugv)

    def dispatch_nearest(self, mission: Mission, target_lat: float, target_lon: float) -> Optional[UGV]:
        """Find nearest Standby vehicle with enough battery and dispatch it."""
        available = [v for v in self.fleet if v.status == "Standby" and v.battery_pct > self.rtb_threshold]
        if not available:
            print(f"[FLEET] No available vehicle for mission {mission.mission_id}")
            return None
        nearest = min(available, key=lambda v: haversine_km(target_lat, target_lon, v.lat, v.lon))
        dist = haversine_km(target_lat, target_lon, nearest.lat, nearest.lon)
        nearest.status = "InMission"
        nearest.mission_id = mission.mission_id
        nearest.module = mission.type
        mission.assigned_vehicle_id = nearest.vehicle_id
        mission.status = "Active"
        self.missions.append(mission)
        print(f"[FLEET] {nearest.vehicle_id} dispatched → {mission.mission_id} ({dist:.2f}km)")
        return nearest

    def update_battery(self, vehicle_id: str, new_pct: float):
        """Update battery and trigger RTB if below threshold."""
        v = next((x for x in self.fleet if x.vehicle_id == vehicle_id), None)
        if not v: return
        v.battery_pct = new_pct
        if new_pct <= self.rtb_threshold and v.status == "InMission":
            v.status = "RTB"
            v.alert = f"LOW BATTERY ({new_pct:.0f}%) — RTB AUTO"
            if v.mission_id:
                m = next((x for x in self.missions if x.mission_id == v.mission_id), None)
                if m: m.status = "Aborted"
            print(f"[FLEET] {vehicle_id} auto-RTB triggered at {new_pct:.0f}%")

    def complete_mission(self, mission_id: str):
        m = next((x for x in self.missions if x.mission_id == mission_id), None)
        if not m: return
        m.status = "Completed"
        m.completed_at = datetime.utcnow().isoformat()
        if m.assigned_vehicle_id:
            v = next((x for x in self.fleet if x.vehicle_id == m.assigned_vehicle_id), None)
            if v:
                v.status = "RTB"
                v.mission_id = None
        print(f"[FLEET] Mission {mission_id} completed")

    def status_report(self):
        print(f"\n{'='*50}")
        print(f"FLEET STATUS — {datetime.utcnow().strftime('%H:%M:%S UTC')}")
        print(f"{'='*50}")
        for v in self.fleet:
            print(f"  {v.vehicle_id:8s} | {v.status:10s} | {v.module:12s} | BAT {v.battery_pct:5.1f}% | {v.alert or 'OK'}")
        print(f"\nMISSIONS: {len([m for m in self.missions if m.status=='Active'])} active / {len(self.missions)} total")


if __name__ == "__main__":
    fm = FleetManager(rtb_threshold=20.0)
    fm.add_vehicle(UGV("RHN-01", lat=48.380, lon=31.165, battery_pct=98))
    fm.add_vehicle(UGV("RHN-02", lat=48.375, lon=31.158, battery_pct=71))
    fm.add_vehicle(UGV("RHN-03", lat=48.381, lon=31.162, battery_pct=100))

    m1 = Mission("MSN-001", type="Logistics", payload_desc="130kg ammo → Alpha", priority="HIGH", distance_km=0.6)
    fm.dispatch_nearest(m1, target_lat=48.376, target_lon=31.160)

    fm.update_battery("RHN-02", 18.5)  # trigger auto-RTB
    fm.status_report()
