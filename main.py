from database import Base, engine
from media_model import MediaModel
from scheduled_content_model import ScheduledContentModel


def main():
    Base.metadata.create_all(engine)

    print("Database tables created successfully.")


if __name__ == "__main__":
    main()