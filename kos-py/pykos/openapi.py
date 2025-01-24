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

class CalibrationMetadata(BaseModel):
    """Calibration metadata model."""
    status: str = Field(..., description="Current calibration status")

def generate_docs(output_path: str = "docs/openapi.json"):
    """Generate OpenAPI documentation JSON file."""
    openapi_spec = app.openapi()
    
    # Add readme.io specific metadata
    openapi_spec["info"]["x-readme"] = {
        "samples-languages": ["python"],
        "explorer-enabled": True,
        "categories": [
            {
                "name": "Setup",
                "description": "Client initialization and setup"
            },
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
    
    # Add Python method documentation
    openapi_spec["paths"] = {
        "/KOS.__init__": {
            "post": {
                "operationId": "initialize",
                "tags": ["Setup"],
                "summary": "Initialize KOS Client",
                "description": "Create a new KOS client instance",
                "x-readme": {
                    "code-samples": [
                        {
                            "language": "python",
                            "code": "# Connect to local KOS instance\nkos = KOS()\n\n# Connect to remote KOS instance\nkos = KOS(ip='192.168.1.100', port=50051)"
                        }
                    ]
                }
            }
        },
        "/imu/values": {
            "get": {
                "operationId": "get_imu_values",
                "tags": ["IMU"],
                "summary": "Get IMU Values",
                "description": "Get the latest IMU sensor values including acceleration and angular velocity",
                "x-readme": {
                    "code-samples": [
                        {
                            "language": "python",
                            "code": "values = kos.imu.get_imu_values()"
                        }
                    ]
                }
            }
        },
        "/imu/quaternion": {
            "get": {
                "operationId": "get_quaternion",
                "tags": ["IMU"],
                "summary": "Get Quaternion",
                "description": "Get the latest quaternion orientation",
                "x-readme": {
                    "code-samples": [
                        {
                            "language": "python",
                            "code": "quat = kos.imu.get_quaternion()"
                        }
                    ]
                }
            }
        },
        "/imu/zero": {
            "post": {
                "operationId": "zero_imu",
                "tags": ["IMU"],
                "summary": "Zero IMU",
                "description": "Zero the IMU with optional parameters",
                "x-readme": {
                    "code-samples": [
                        {
                            "language": "python",
                            "code": "# Basic zeroing\nkos.imu.zero()\n\n# Advanced zeroing\nkos.imu.zero(\n    duration=2.0,\n    max_retries=3,\n    max_angular_error=0.1\n)"
                        }
                    ]
                }
            }
        },
        "/actuator/calibrate": {
            "post": {
                "operationId": "calibrate_actuator",
                "tags": ["Actuator"],
                "summary": "Calibrate Actuator",
                "description": "Calibrate a specific actuator",
                "x-readme": {
                    "code-samples": [
                        {
                            "language": "python",
                            "code": "metadata = kos.actuator.calibrate(actuator_id=1)"
                        }
                    ]
                }
            }
        },
        "/actuator/command": {
            "post": {
                "operationId": "command_actuators",
                "tags": ["Actuator"],
                "summary": "Command Actuators",
                "description": "Send commands to multiple actuators",
                "x-readme": {
                    "code-samples": [
                        {
                            "language": "python",
                            "code": "commands = [\n    {\"actuator_id\": 1, \"position\": 1.57},\n    {\"actuator_id\": 2, \"torque\": 0.5}\n]\nkos.actuator.command_actuators(commands)"
                        }
                    ]
                }
            }
        }
    }
    
    # Add schemas
    openapi_spec["components"]["schemas"].update({
        "IMUResponse": IMUResponse.model_json_schema(),
        "ActuatorResponse": ActuatorResponse.model_json_schema(),
        "CalibrationMetadata": CalibrationMetadata.model_json_schema()
    })
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(openapi_spec, f, indent=2)
    
    print(f"OpenAPI documentation generated at: {output_path}") 