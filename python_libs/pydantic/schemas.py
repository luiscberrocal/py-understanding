import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from python_libs.pydantic.model_config import Payload


class PaymentsFile(BaseModel):
    """File that contain a list of dictionaries containing payments."""
    local_path: Path = Field(description='Local path to the file.')
    creation_date: datetime = Field(description='Datetime when the local file was created.')
    raw_hash_digest: str = Field(description='Hash digest for the file content as it was read from Kafka.'
                                             ' Use hash_file function.',
                                 max_length=96, min_length=96)
    record_count: int = Field(description='Records found in the file', ge=0)
    kafka_group: str = Field(description='Kafka group used to consume the messages.', max_length=64)
    processed_hash_digest: Optional[str] = Field(description='Hash digest for the file content after'
                                                             ' being ordered and cleaned. Use hash_file function.',
                                                 max_length=96, min_length=96)
    datadog_start_date: Optional[datetime] = Field(description='Date the file started to be sent to Datadog.')
    datadog_end_date: Optional[datetime] = Field(description='Date the file finished being sent to Datadog.')
    data_dog_count: Optional[int] = Field(description='Amount of records sent to Datadog.', ge=0)
    url: Optional[HttpUrl] = Field(description='S3 http url.')

    def exist_locally(self) -> bool:
        return self.local_path.exists()


def extract_properties(model: BaseModel):
    schema = model.schema()
    properties = []
    for key, item in schema['properties'].items():
        item['name'] = key
        properties.append(item)
    return properties


def save_schema_to_file(file: Path, model: BaseModel) -> None:
    properties = extract_properties(model)
    columns = list(properties[0].keys())
    columns.extend(['minLength', 'maxLength', 'minimum'])
    with open(file, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(properties)

def save_schema(model: BaseModel, file: Path):
    with open(file, 'w') as f:
        json.dump(model.schema(), f, indent=4)

if __name__ == '__main__':
    output_folder = Path(__file__).parent.parent.parent / 'output'
    # csv_file = output_folder / 'payments_file_schema.csv'
    # save_schema_to_file(csv_file, PaymentsFile)

    j_file = output_folder / 'payments_file_schema.json'
    save_schema(PaymentsFile, j_file)

    j_file = output_folder / 'payload_schema.json'
    save_schema(Payload, j_file)
