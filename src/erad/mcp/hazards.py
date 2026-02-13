"""
Historic hazard tools for ERAD MCP Server.
"""

import sqlite3

from loguru import logger

from erad.models.hazard.wind import WindModel
from erad.models.hazard.earthquake import EarthQuakeModel
from erad.models.hazard.wild_fire import FireModel

from .state import state
from .helpers import get_historic_hazard_db


async def list_historic_hurricanes_tool(args: dict) -> dict:
    """List historic hurricanes from database."""
    year = args.get("year")
    limit = args.get("limit", 50)

    try:
        db_path = get_historic_hazard_db()
        if not db_path.exists():
            return {"error": f"Historic hazard database not found at {db_path}"}

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = "SELECT DISTINCT SID, NAME, SEASON FROM historic_hurricanes"
        params = []

        if year:
            query += " WHERE SEASON = ?"
            params.append(year)

        query += " ORDER BY SEASON DESC, NAME LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        hurricanes = [{"sid": row[0], "name": row[1], "season": row[2]} for row in results]

        logger.info(f"Found {len(hurricanes)} historic hurricanes")

        return {"success": True, "count": len(hurricanes), "hurricanes": hurricanes}

    except Exception as e:
        logger.error(f"Error listing hurricanes: {e}")
        return {"error": str(e)}


async def list_historic_earthquakes_tool(args: dict) -> dict:
    """List historic earthquakes from database."""
    min_magnitude = args.get("min_magnitude")
    limit = args.get("limit", 50)

    try:
        db_path = get_historic_hazard_db()
        if not db_path.exists():
            return {"error": f"Historic hazard database not found at {db_path}"}

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = "SELECT earthquake_code, date, magnitude, latitude, longitude FROM historic_earthquakes"
        params = []

        if min_magnitude:
            query += " WHERE magnitude >= ?"
            params.append(min_magnitude)

        query += " ORDER BY magnitude DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        earthquakes = [
            {
                "earthquake_code": row[0],
                "date": row[1],
                "magnitude": row[2],
                "latitude": row[3],
                "longitude": row[4],
            }
            for row in results
        ]

        logger.info(f"Found {len(earthquakes)} historic earthquakes")

        return {"success": True, "count": len(earthquakes), "earthquakes": earthquakes}

    except Exception as e:
        logger.error(f"Error listing earthquakes: {e}")
        return {"error": str(e)}


async def list_historic_wildfires_tool(args: dict) -> dict:
    """List historic wildfires from database."""
    year = args.get("year")
    limit = args.get("limit", 50)

    try:
        db_path = get_historic_hazard_db()
        if not db_path.exists():
            return {"error": f"Historic hazard database not found at {db_path}"}

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = "SELECT DISTINCT FIRE_NAME, FIRE_YEAR FROM historic_fires"
        params = []

        if year:
            query += " WHERE FIRE_YEAR = ?"
            params.append(year)

        query += " ORDER BY FIRE_YEAR DESC, FIRE_NAME LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        wildfires = [{"fire_name": row[0], "fire_year": row[1]} for row in results]

        logger.info(f"Found {len(wildfires)} historic wildfires")

        return {"success": True, "count": len(wildfires), "wildfires": wildfires}

    except Exception as e:
        logger.error(f"Error listing wildfires: {e}")
        return {"error": str(e)}


async def load_historic_hurricane_tool(args: dict) -> dict:
    """Load historic hurricane into hazard system."""
    hazard_system_id = args["hazard_system_id"]
    hurricane_sid = args["hurricane_sid"]

    try:
        if hazard_system_id not in state.hazard_systems:
            return {"error": f"Hazard system not found: {hazard_system_id}"}

        hazard_system = state.hazard_systems[hazard_system_id]

        logger.info(f"Loading hurricane {hurricane_sid}")
        wind_model = WindModel.from_hurricane_sid(hurricane_sid)
        hazard_system.add_component(wind_model)

        return {
            "success": True,
            "hurricane_sid": hurricane_sid,
            "timestamp": wind_model.timestamp.isoformat(),
            "max_wind_speed": str(wind_model.max_wind_speed),
            "message": f"Hurricane {hurricane_sid} added to hazard system {hazard_system_id}",
        }

    except Exception as e:
        logger.error(f"Error loading hurricane: {e}")
        return {"error": str(e)}


async def load_historic_earthquake_tool(args: dict) -> dict:
    """Load historic earthquake into hazard system."""
    hazard_system_id = args["hazard_system_id"]
    earthquake_code = args["earthquake_code"]

    try:
        if hazard_system_id not in state.hazard_systems:
            return {"error": f"Hazard system not found: {hazard_system_id}"}

        hazard_system = state.hazard_systems[hazard_system_id]

        logger.info(f"Loading earthquake {earthquake_code}")
        earthquake_model = EarthQuakeModel.from_earthquake_code(earthquake_code)
        hazard_system.add_component(earthquake_model)

        return {
            "success": True,
            "earthquake_code": earthquake_code,
            "timestamp": earthquake_model.timestamp.isoformat(),
            "magnitude": earthquake_model.magnitude,
            "message": f"Earthquake {earthquake_code} added to hazard system {hazard_system_id}",
        }

    except Exception as e:
        logger.error(f"Error loading earthquake: {e}")
        return {"error": str(e)}


async def load_historic_wildfire_tool(args: dict) -> dict:
    """Load historic wildfire into hazard system."""
    hazard_system_id = args["hazard_system_id"]
    wildfire_name = args["wildfire_name"]

    try:
        if hazard_system_id not in state.hazard_systems:
            return {"error": f"Hazard system not found: {hazard_system_id}"}

        hazard_system = state.hazard_systems[hazard_system_id]

        logger.info(f"Loading wildfire {wildfire_name}")
        fire_model = FireModel.from_wildfire_name(wildfire_name)
        hazard_system.add_component(fire_model)

        return {
            "success": True,
            "wildfire_name": wildfire_name,
            "timestamp": fire_model.timestamp.isoformat(),
            "message": f"Wildfire {wildfire_name} added to hazard system {hazard_system_id}",
        }

    except Exception as e:
        logger.error(f"Error loading wildfire: {e}")
        return {"error": str(e)}
