import ijson
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")


# Define SQLAlchemy Base and model
Base = declarative_base()


class TitleBoundary(Base):
    __tablename__ = "title_boundary"

    id = Column(String(255), primary_key=True)
    dataset = Column(String(255), nullable=False)
    end_date = Column(String(255), nullable=True)
    entity = Column(String(255), nullable=False)
    entry_date = Column(String(255), nullable=False)
    geometry = Column(
        Geometry("MULTIPOLYGON", srid=4326), nullable=False
    )  # PostGIS geometry column
    name = Column(String(255), nullable=True)
    organisation_entity = Column(String(255), nullable=False)
    point = Column(String, nullable=False)
    prefix = Column(String(255), nullable=False)
    reference = Column(String(255), nullable=False)
    start_date = Column(String(255), nullable=False)
    typology = Column(String(255), nullable=False)


# Function to read the large JSON file
def iterate_large_json(file_path):
    with open(file_path, "r") as f:
        objects = ijson.items(
            f, "entities.item"
        )  # Adjust the path based on your JSON structure
        for obj in objects:
            yield obj


# Set up SQLAlchemy engine and session
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create the table if it doesn't exist (run this only once)
Base.metadata.create_all(engine)

# Define the file path for your JSON data
file_path = "./input/title-boundary.json"

print("running...")

# Loop through the items and insert them into the database
for idx, item in enumerate(iterate_large_json(file_path)):
    print(f"Processing item {idx}: {item["reference"]}")

    try:
        # Prepare data for insertion
        dataset = TitleBoundary(
            id=item["reference"],  # Use the reference as the primary key
            dataset=item["dataset"],
            end_date=item.get("end-date", None),
            entity=item["entity"],
            entry_date=item["entry-date"],
            geometry=item["geometry"],  # Handle geometry correctly if needed
            name=item.get("name", None),
            organisation_entity=item["organisation-entity"],
            point=item[
                "point"
            ],  # You might need to convert this to a PostGIS point type
            prefix=item["prefix"],
            reference=item["reference"],
            start_date=item["start-date"],
            typology=item["typology"],
        )

        # Add to session and commit the transaction
        session.add(dataset)
        session.commit()
    except Exception as e:
        print(f"Error processing item {idx}: {e}")
        session.rollback()
        continue  # Skip to the next item
    # if idx == 9:  # Stop after the first 10 items (optional)
    #     break

# Close the session
session.close()
