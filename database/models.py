from datetime import datetime
from typing import Optional, Dict, Any

class TextDocument:
    def __init__(
        self,
        title: str,
        content: str,
        author_id: int,
        author_name: str,
        guild_id: Optional[int] = None,
        channel_id: Optional[int] = None,
        tags: Optional[list] = None,
        _id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self._id = _id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.author_name = author_name
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.tags = tags or []
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        doc = {
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'author_name': self.author_name,
            'guild_id': self.guild_id,
            'channel_id': self.channel_id,
            'tags': self.tags,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        if self._id:
            doc['_id'] = self._id
        return doc
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TextDocument':
        return cls(
            _id=str(data.get('_id')),
            title=data.get('title'),
            content=data.get('content'),
            author_id=data.get('author_id'),
            author_name=data.get('author_name'),
            guild_id=data.get('guild_id'),
            channel_id=data.get('channel_id'),
            tags=data.get('tags', []),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )