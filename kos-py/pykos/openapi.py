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
    
    # Initialize components and schemas
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
        "/imu/calibrate": {
            "post": {
                "operationId": "calibrateIMU",
                "tags": ["IMU"],
                "summary": "Calibrate IMU",
                "description": "Start IMU calibration process",
                "responses": {
                    "200": {
                        "description": "Calibration started successfully"
                    }
                }
            }
        },
        "/actuator/state": {
            "get": {
                "operationId": "getActuatorState",
                "tags": ["Actuator"],
                "summary": "Get Actuator State",
                "description": "Get current actuator state",
                "responses": {
                    "200": {
                        "description": "Current actuator state",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ActuatorResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/actuator/command": {
            "post": {
                "operationId": "commandActuators",
                "tags": ["Actuator"],
                "summary": "Command Actuators",
                "description": "Send commands to multiple actuators",
                "responses": {
                    "200": {
                        "description": "Commands sent successfully"
                    }
                }
            }
        }
    }
    
    # Add schemas
    openapi_spec["components"]["schemas"].update({
        "IMUResponse": IMUResponse.model_json_schema(),
        "ActuatorResponse": ActuatorResponse.model_json_schema()
    })
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(openapi_spec, f, indent=2)
    
    print(f"OpenAPI documentation generated at: {output_path}") 