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
    
    # Add Python method documentation instead of HTTP paths
    openapi_spec["paths"] = {
        "/kos.get_imu_data": {
            "get": {
                "operationId": "get_imu_data",
                "tags": ["IMU"],
                "summary": "Get IMU Data",
                "description": "Get IMU sensor data",
                "x-readme": {
                    "code-samples": [
                        {
                            "language": "python",
                            "code": "kos = KOS()\ndata = kos.get_imu_data()"
                        }
                    ]
                },
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
        "/kos.get_actuator_state": {
            "get": {
                "operationId": "get_actuator_state",
                "tags": ["Actuator"],
                "summary": "Get Actuator State",
                "description": "Get current actuator state",
                "x-readme": {
                    "code-samples": [
                        {
                            "language": "python",
                            "code": "kos = KOS()\nstate = kos.get_actuator_state()"
                        }
                    ]
                },
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