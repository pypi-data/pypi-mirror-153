from google.cloud import secretmanager
from google.api_core.exceptions import AlreadyExists
import google_crc32c
import json
import logging


class SecretManager:
    def __init__(self, project_id: str, secret_id: str):
        self.project_id = project_id
        self.secret_id = secret_id
        self.client = secretmanager.SecretManagerServiceClient()
        self.initialize()

    def initialize(self) -> None:
        logging.info("Creating secret...")
        try:
            self.client.create_secret(
                request={
                    "parent": f"projects/{self.project_id}",
                    "secret_id": self.secret_id,
                    "secret": {"replication": {"automatic": {}}},
                }
            )
            logging.info(f"Created secret {self.secret_id}")

        except AlreadyExists:
            logging.info(f"Secret {self.secret_id} already exists")

    def pull(self) -> dict:
        logging.info("Pulling latest secret version...")
        name = self.client.secret_version_path(self.project_id, self.secret_id, "latest")
        response = self.client.access_secret_version(request={"name": name})
        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            print("Data corruption detected.")
            raise ValueError("Data corruption detected.")

        payload = response.payload.data.decode("UTF-8")

        return json.loads(payload)

    def push(self, payload: dict) -> None:
        logging.info("Pushing secret...")
        parent = self.client.secret_path(self.project_id, self.secret_id)
        payload_bytes = json.dumps(payload).encode("UTF-8")
        crc32c = google_crc32c.Checksum()
        crc32c.update(payload_bytes)
        self.client.add_secret_version(
            request={
                "parent": parent,
                "payload": {
                    "data": payload_bytes,
                    "data_crc32c": int(crc32c.hexdigest(), 16),
                },
            }
        )
