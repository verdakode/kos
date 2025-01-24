"""OpenAPI documentation generator for PyKOS."""

import json
from pathlib import Path
from pydantic import BaseModel, Field

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
    openapi_spec = {
        "openapi": "3.1.0",
        "info": {
            "title": "PyKOS Python Client Documentation",
            "description": "Python client library for controlling robots through KOS",
            "version": "1.0.0",
            "x-readme": {
                "samples-languages": ["python"],
                "explorer-enabled": True,
                "categories": [
                    {"name": "Setup", "description": "Client initialization and setup"},
                    {"name": "IMU", "description": "IMU sensor operations"},
                    {"name": "Actuator", "description": "Actuator control operations"}
                ]
            }
        },
        "paths": {
            "/python/kos/init": {
                "get": {
                    "tags": ["Setup"],
                    "summary": "Initialize KOS Client",
                    "description": "Create a new KOS client instance",
                    "x-readme": {
                        "code-samples": [{
                            "language": "python",
                            "code": "# Connect to local KOS instance\nkos = KOS()\n\n# Connect to remote KOS instance\nkos = KOS(ip='192.168.1.100', port=50051)"
                        }]
                    }
                }
            },
            "/python/imu/values": {
                "get": {
                    "tags": ["IMU"],
                    "summary": "Get IMU Values",
                    "description": "Get the latest IMU sensor values",
                    "x-readme": {
                        "code-samples": [{
                            "language": "python",
                            "code": "values = kos.imu.get_imu_values()"
                        }]
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
            }
        },
        "components": {
            "schemas": {
                "IMUResponse": IMUResponse.model_json_schema(),
                "ActuatorResponse": ActuatorResponse.model_json_schema()
            }
        }
    }
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(openapi_spec, f, indent=2)
    
    print(f"API documentation generated at: {output_path}") 