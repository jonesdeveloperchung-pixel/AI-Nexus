import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import List

# Define the base for declarative models
Base = declarative_base()

class GeneratedContent(Base):
    __tablename__ = 'generated_content'

    id = Column(Integer, primary_key=True)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    language = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<GeneratedContent(id={self.id}, language='{self.language}', timestamp='{self.timestamp}')>"

# Database file path
DATABASE_FILE = "ai_writing.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Engine and Session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initializes the database and creates tables if they don't exist.
    """
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at {DATABASE_FILE}")

def save_content(prompt: str, response: str, language: str) -> GeneratedContent:
    """
    Saves generated content to the database.
    """
    db = SessionLocal()
    try:
        new_content = GeneratedContent(prompt=prompt, response=response, language=language)
        db.add(new_content)
        db.commit()
        db.refresh(new_content)
        print(f"Content saved: ID {new_content.id}")
        return new_content
    finally:
        db.close()

def get_all_content() -> List[GeneratedContent]:
    """
    Retrieves all generated content from the database.
    """
    db = SessionLocal()
    try:
        return db.query(GeneratedContent).all()
    finally:
        db.close()

if __name__ == "__main__":
    # Clean up previous db for fresh start
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)

    init_db()

    # Save some sample content
    content1 = save_content(
        prompt="Write a short story about a cat.",
        response="Once upon a time, there was a fluffy cat named Whiskers...",
        language="English"
    )
    content2 = save_content(
        prompt="寫一首關於山的詩。",
        response="高山巍峨，雲霧繚繞，宛如仙境。",
        language="Chinese"
    )

    # Retrieve and print all content
    print("\nAll generated content:")
    all_content = get_all_content()
    for content in all_content:
        print(f"ID: {content.id}, Lang: {content.language}, Prompt: {content.prompt[:50]}..., Response: {content.response[:50]}...")
