from signalnoise.database.connection import (
    engine
)

from signalnoise.database.models import (
    Base
)
from signalnoise.database.entities.document_entity import DocumentEntity

Base.metadata.create_all(
    bind=engine
)

print(
    "Tables Created Successfully"
)