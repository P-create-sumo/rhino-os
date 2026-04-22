"""
TROPIYA Demining System — Corridor Calculator
Computes safe clearance corridor and minimum safe distance
for RHINO-OS UGV demining operations.
"""

import math


def calculate_tropiya(charges: int, angle_deg: float) -> dict:
    """
    Calculate TROPIYA corridor clearance parameters.

    Args:
        charges: Number of detonating cord charges (1-12)
        angle_deg: Deployment angle in degrees (15-90)

    Returns:
        dict with corridor_m, safe_distance_m, area_m2, recommended_standoff_m
    """
    angle_rad = math.radians(angle_deg)
    corridor_m = round(charges * 12 * math.sin(angle_rad) * 0.95)
    safe_distance_m = round(charges * 6.5)
    area_m2 = round(corridor_m * charges * 1.2)
    standoff_m = safe_distance_m + 15  # buffer for shrapnel

    return {
        "charges": charges,
        "angle_deg": angle_deg,
        "corridor_m": corridor_m,
        "safe_distance_m": safe_distance_m,
        "area_cleared_m2": area_m2,
        "recommended_standoff_m": standoff_m,
        "suitable_for_infantry": corridor_m >= 4,
        "suitable_for_vehicles": corridor_m >= 6,
    }


def mission_plan(target_width_m: float, angle_deg: float = 60) -> dict:
    """
    Calculate number of TROPIYA charges needed for a target corridor width.

    Args:
        target_width_m: Required corridor width in meters
        angle_deg: Deployment angle

    Returns:
        dict with required charges and full mission parameters
    """
    angle_rad = math.radians(angle_deg)
    charges_needed = math.ceil(target_width_m / (12 * math.sin(angle_rad) * 0.95))
    charges_needed = max(1, min(12, charges_needed))
    return calculate_tropiya(charges_needed, angle_deg)


if __name__ == "__main__":
    print("TROPIYA Calculator — RHINO-OS")
    print("=" * 40)
    for c in [2, 4, 6, 8, 12]:
        result = calculate_tropiya(c, 60)
        print(f"Charges: {c:2d} | Corridor: {result['corridor_m']:3d}m | Safe dist: {result['safe_distance_m']:3d}m | Area: {result['area_cleared_m2']:4d}m²")

    print("\nMission planning — 8m corridor needed:")
    plan = mission_plan(8.0)
    print(f"  Charges required: {plan['charges']}")
    print(f"  Actual corridor: {plan['corridor_m']}m")
    print(f"  Safe distance: {plan['safe_distance_m']}m")
