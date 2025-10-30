from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import Config
import logging

logger = logging.getLogger(__name__)

class MongoDB:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        if self._client is None:
            try:
                self._client = MongoClient(Config.MONGODB_URI, serverSelectionTimeoutMS=5000)
                # Test connection
                self._client.admin.command('ping')
                self._db = self._client[Config.MONGODB_DATABASE]
                logger.info(f"✓ Connected to MongoDB: {Config.MONGODB_DATABASE}")
            except ConnectionFailure as e:
                logger.error(f"✗ Failed to connect to MongoDB: {e}")
                raise
        return self._db
    
    def get_database(self):
        if self._db is None:
            return self.connect()
        return self._db
    
    def close(self):
        if self._client:
            self._client.close()
            logger.info("✓ MongoDB connection closed")
            self._client = None
            self._db = None

# Global database instance
db = MongoDB()