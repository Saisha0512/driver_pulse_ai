"""
data_loader.py
--------------
Centralised, cached data loading for all pages.
Person A (Aayush) owns this file — Saisha calls it via session_state.
"""

import pandas as pd
import streamlit as st
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def _path(filename: str) -> str:
    return os.path.join(DATA_DIR, filename)


def _safe_read(filename: str) -> pd.DataFrame:
    """Returns empty DataFrame if file doesn't exist yet."""
    try:
        return pd.read_csv(_path(filename))
    except FileNotFoundError:
        return pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_all_data():
    """Load and lightly clean all CSVs. Cached for the session."""

    # ── REQUIRED (your files — must exist) ──
    drivers  = pd.read_csv(_path("drivers.csv"))
    trips    = pd.read_csv(_path("trips.csv"))
    acc      = pd.read_csv(_path("accelerometer_data.csv"))
    aud      = pd.read_csv(_path("audio_intensity_data.csv"))
    flags    = pd.read_csv(_path("flagged_moments.csv"))

    # ── OPTIONAL (Aanvi's files — safe if missing) ──
    goals     = _safe_read("driver_goals.csv")
    velocity  = _safe_read("earnings_velocity_log.csv")
    summaries = _safe_read("trip_summaries.csv")

    # ── FIX: join driver_id into sensor tables via trip_id ──
    trip_driver_map = trips[["trip_id", "driver_id"]]
    acc = acc.merge(trip_driver_map, on="trip_id", how="left")
    aud = aud.merge(trip_driver_map, on="trip_id", how="left")

    # ── Parse timestamps ──
    for df, col in [(acc, "timestamp"), (aud, "timestamp"), (flags, "timestamp"),
                    (trips, "date")]:
        try:
            df[col] = pd.to_datetime(df[col], errors="coerce")
        except Exception:
            pass

    # Only parse these if the files actually loaded
    for df, col in [(goals, "date"), (velocity, "timestamp")]:
        if not df.empty:
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
            except Exception:
                pass

    return {
        "drivers":   drivers,
        "trips":     trips,
        "acc":       acc,
        "aud":       aud,
        "flags":     flags,
        "goals":     goals,
        "velocity":  velocity,
        "summaries": summaries,
    }


def get_driver_data(driver_id: str, data: dict) -> dict:
    """Filter all datasets to a specific driver_id."""
    trips_df = data["trips"]
    trip_ids = trips_df[trips_df["driver_id"] == driver_id]["trip_id"].tolist()

    def safe_filter_driver(df: pd.DataFrame) -> pd.DataFrame:
        """Filter by driver_id — returns empty DataFrame safely if missing."""
        if df.empty or "driver_id" not in df.columns:
            return pd.DataFrame()
        return df[df["driver_id"] == driver_id]

    def safe_filter_trips(df: pd.DataFrame) -> pd.DataFrame:
        """Filter by trip_id list — returns empty DataFrame safely if missing."""
        if df.empty or "trip_id" not in df.columns:
            return pd.DataFrame()
        return df[df["trip_id"].isin(trip_ids)]

    return {
        "driver":    data["drivers"][data["drivers"]["driver_id"] == driver_id].iloc[0].to_dict()
                     if (data["drivers"]["driver_id"] == driver_id).any() else {},
        "trips":     trips_df[trips_df["driver_id"] == driver_id],

        # acc and aud now have driver_id after the merge — filter directly
        "acc":       safe_filter_driver(data["acc"]),
        "aud":       safe_filter_driver(data["aud"]),

        "flags":     data["flags"][
                         (data["flags"]["driver_id"] == driver_id) |
                         (data["flags"]["trip_id"].isin(trip_ids))
                     ] if not data["flags"].empty else pd.DataFrame(),
        "goals":     safe_filter_driver(data["goals"]),
        "velocity":  safe_filter_driver(data["velocity"]),
        "summaries": safe_filter_driver(data["summaries"]),
        "trip_ids":  trip_ids,
    }


def get_drivers_with_sensor_data(data: dict) -> list:
    """
    Returns only driver IDs that have actual accelerometer data.
    Used by the dropdown in 2_My_Safety.py so blank pages never show.
    """
    if data["acc"].empty or "driver_id" not in data["acc"].columns:
        return sorted(data["drivers"]["driver_id"].tolist())
    acc_driver_ids = set(data["acc"]["driver_id"].dropna().unique())
    return sorted([
        d for d in data["drivers"]["driver_id"].tolist()
        if d in acc_driver_ids
    ])