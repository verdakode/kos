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
    """Generate OpenAPI documentation JSON file."""
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
    
    # Initialize components and schemas if they don't exist
    if "components" not in openapi_spec:
        openapi_spec["components"] = {}
    if "schemas" not in openapi_spec["components"]:
        openapi_spec["components"]["schemas"] = {}
    
    # Add paths for all available endpoints
    openapi_spec["paths"] = {
        "/imu/values": {
            "get": {
                "operationId": "getIMUValues",
                "tags": ["IMU"],
                "summary": "Get IMU Values",
                "description": "Get the latest IMU sensor values",
                "responses": {
                    "200": {
                        "description": "Current IMU sensor readings",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/IMUResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/imu/quaternion": {
            "get": {
                "operationId": "getQuaternion",
                "tags": ["IMU"],
                "summary": "Get Quaternion",
                "description": "Get the latest quaternion orientation",
                "responses": {
                    "200": {
                        "description": "Current quaternion orientation",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/IMUResponse"}
                            }
                        }
                    }
                }
            }
        }
    }
    
    # Add all models from IMU and Actuator services
    openapi_spec["components"]["schemas"].update({
        "IMUResponse": IMUResponse.model_json_schema(),
        "ActuatorResponse": ActuatorResponse.model_json_schema()
    })
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(openapi_spec, f, indent=2)
    
    print(f"OpenAPI documentation generated at: {output_path}") 