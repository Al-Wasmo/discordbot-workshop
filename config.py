import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    # Discord Configuration
    TOKEN = os.getenv('TOKEN')
    COMMAND_PREFIX = "!" 
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    MONGODB_DATABASE = os.getenv('Cluster0', 'discord_bot_db')
    
    @classmethod
    def validate(cls):
        if not cls.TOKEN:
            raise ValueError("TOKEN is not set in environment variables")
        if not cls.MONGODB_URI:
            raise ValueError("MONGODB_URI is not set in environment variables")