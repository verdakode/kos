"""OpenAPI documentation generator for PyKOS."""

import json
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Initialize FastAPI app for readme.io documentation
app = FastAPI(
    title="PyKOS API Documentation",
    version="1.0.0",
    description="Python client for controlling robots through KOS"
)

class IMUResponse(BaseModel):
    """IMU service response model."""
    
    acceleration: list[float] = Field(..., description="Acceleration values in m/s^2")
    angular_velocity: list[float] = Field(..., description="Angular velocity values in rad/s")
    orientation: list[float] = Field(..., description="Orientation quaternion")

class ActuatorResponse(BaseModel):
    """Actuator service response model."""
    
    position: float = Field(..., description="Current position")
    velocity: float = Field(..., description="Current velocity")
    torque: float = Field(..., description="Current torque")

def generate_docs(output_path: str = "docs/openapi.json"):
    """Generate OpenAPI documentation JSON file.
    
    Args:
        output_path: Path where the OpenAPI JSON file should be saved
    """
    openapi_spec = app.openapi()
    
    # Add readme.io specific metadata
    openapi_spec["info"]["x-readme"] = {
        "samples-languages": ["python"],
        "explorer-enabled": True,
        "categories": [
            {
                "name": "IMU",
                "description": "IMU sensor operations"
            },
            {
                "name": "Actuator",
                "description": "Actuator control operations"
            }
        ]
    }
    
    # Add components section if it doesn't exist
    if "components" not in openapi_spec:
        openapi_spec["components"] = {"schemas": {}}
    
    # Add all models to the components/schemas section
    openapi_spec["components"]["schemas"].update({
        "IMUResponse": {
            "type": "object",
            "properties": {
                "acceleration": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "Acceleration values in m/s^2"
                },
                "angular_velocity": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "Angular velocity values in rad/s"
                },
                "orientation": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "Orientation quaternion"
                }
            }
        },
        "ActuatorResponse": {
            "type": "object",
            "properties": {
                "position": {
                    "type": "number",
                    "description": "Current position"
                },
                "velocity": {
                    "type": "number",
                    "description": "Current velocity"
                },
                "torque": {
                    "type": "number",
                    "description": "Current torque"
                }
            }
        }
    })
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(openapi_spec, f, indent=2)
    
    print(f"OpenAPI documentation generated at: {output_path}") 