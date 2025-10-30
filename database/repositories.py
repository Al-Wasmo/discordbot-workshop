from typing import List, Optional
from bson.objectid import ObjectId
from datetime import datetime
import logging

from database.connection import db
from database.models import TextDocument

logger = logging.getLogger(__name__)

class TextRepository:
    def __init__(self):
        self.collection = db.get_database()['texts']
    
    def create(self, document: TextDocument) -> str:
        try:
            doc_dict = document.to_dict()
            result = self.collection.insert_one(doc_dict)
            logger.info(f"✓ Created document: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"✗ Error creating document: {e}")
            raise
    
    def get_by_id(self, document_id: str) -> Optional[TextDocument]:
        try:
            result = self.collection.find_one({'_id': ObjectId(document_id)})
            if result:
                return TextDocument.from_dict(result)
            return None
        except Exception as e:
            logger.error(f"✗ Error retrieving document: {e}")
            return None
    
    def get_by_author(self, author_id: int, limit: int = 10) -> List[TextDocument]:
        try:
            results = self.collection.find({'author_id': author_id})
            return [TextDocument.from_dict(doc) for doc in results]
        except Exception as e:
            logger.error(f"✗ Error retrieving documents by author: {e}")
            return []
    
    def get_by_guild(self, guild_id: int, limit: int = 10) -> List[TextDocument]:
        try:
            results = self.collection.find(
                {'guild_id': guild_id}
            ).sort('created_at', -1).limit(limit)
            return [TextDocument.from_dict(doc) for doc in results]
        except Exception as e:
            logger.error(f"✗ Error retrieving documents by guild: {e}")
            return []
    
    def search_by_title(self, search_term: str, guild_id: Optional[int] = None) -> List[TextDocument]:
        try:
            query = {'title': {'$regex': search_term, '$options': 'i'}}
            if guild_id:
                query['guild_id'] = guild_id
            
            results = self.collection.find(query).sort('created_at', -1).limit(20)
            return [TextDocument.from_dict(doc) for doc in results]
        except Exception as e:
            logger.error(f"✗ Error searching documents: {e}")
            return []
    
    def update(self, document_id: str, content: str) -> bool:
        try:
            result = self.collection.update_one(
                {'_id': ObjectId(document_id)},
                {
                    '$set': {
                        'content': content,
                        'updated_at': datetime.now()
                    }
                }
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"✗ Error updating document: {e}")
            return False
    
    def delete(self, document_id: str, author_id: int) -> bool:
        try:
            result = self.collection.delete_one({
                '_id': ObjectId(document_id),
                'author_id': author_id
            })
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"✗ Error deleting document: {e}")
            return False
    
    def get_stats(self, guild_id: Optional[int] = None) -> dict:
        try:
            query = {'guild_id': guild_id} if guild_id else {}
            total = self.collection.count_documents(query)
            
            pipeline = [
                {'$match': query} if guild_id else {'$match': {}},
                {'$group': {'_id': '$author_id', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 5}
            ]
            
            top_authors = list(self.collection.aggregate(pipeline))
            
            return {
                'total_documents': total,
                'top_authors': top_authors
            }
        except Exception as e:
            logger.error(f"✗ Error getting stats: {e}")
            return {'total_documents': 0, 'top_authors': []}