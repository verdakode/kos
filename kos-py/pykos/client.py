"""KOS client."""

import grpc
from pydantic import ValidationError
from .openapi import IMUResponse, ActuatorResponse

from pykos.services.actuator import ActuatorServiceClient
from pykos.services.imu import IMUServiceClient
from pykos.services.process_manager import ProcessManagerServiceClient


class KOS:
    """KOS client.

    Args:
        ip (str, optional): IP address of the robot running KOS. Defaults to localhost.
        port (int, optional): Port of the robot running KOS. Defaults to 50051.

    Attributes:
        imu (IMUServiceClient): Client for the IMU service.
        actuator (ActuatorServiceClient): Client for the actuator service.
        process_manager (ProcessManagerServiceClient): Client for the process manager service.
    """

    def __init__(self, ip: str = "localhost", port: int = 50051) -> None:
        self.ip = ip
        self.port = port
        self.channel = grpc.insecure_channel(f"{self.ip}:{self.port}")
        self.imu = IMUServiceClient(self.channel)
        self.actuator = ActuatorServiceClient(self.channel)
        self.process_manager = ProcessManagerServiceClient(self.channel)

    def get_imu_data(self) -> IMUResponse:
        """Get IMU sensor data.
        
        Returns:
            IMUResponse: Current IMU sensor readings
        """
        data = self.imu.get_data()
        return IMUResponse(**data)

    def get_actuator_state(self) -> ActuatorResponse:
        """Get actuator state.
        
        Returns:
            ActuatorResponse: Current actuator state
        """
        state = self.actuator.get_state()
        return ActuatorResponse(**state)

    def close(self) -> None:
        """Close the gRPC channel."""
        self.channel.close()
