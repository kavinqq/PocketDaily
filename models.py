from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    JSON,
    Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import relationship


db = SQLAlchemy()
migrate = Migrate()


class TimeStampedModel(db.Model):
    __abstract__ = True

    created_at = Column(
        DateTime,
        default=datetime.now,
        nullable=False
    )
    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
    )

    def save(self, commit=True):
        if commit:
            db.session.add(self)
            db.session.commit()

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()


class UserStateEnum(Enum):
    RANDOM_INT = "RANDOM_INT"
    ADVENTURE_GAME = "ADVENTURE_GAME"


class UserState(TimeStampedModel):
    line_id = Column(
        String,
        primary_key=True,
        unique=True,
        index=True,
        info={"verbose_name": "LineID"}
    )
    action = Column(
        SQLAlchemyEnum(UserStateEnum),
        nullable=True,
        info={"verbose_name": "當前的動作"}
    )
    data = Column(
        JSON,
        nullable=True,
        info={"verbose_name": "當前的資料"}
    )
    history_messages = Column(
        JSON,
        nullable=True,
        info={"verbose_name": "對話歷史"}
    )
    
    input_histories = relationship("UserInputHistory", back_populates="user_state")
    
    def __repr__(self):
        return f"<UserState:{self.line_id}>"
    
    def update(
        self,
        action: Optional[UserStateEnum]=None,
        data: Optional[Dict[str, Any]]=None,
        history_messages: Optional[List[Dict[str, Any]]]=None
    ) -> None:
        
        self.action = action        
        self.data = data        
        self.history_messages = history_messages
            
        self.save()


class UserInputHistory(TimeStampedModel):
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    user_state_line_id = Column(
        String,
        ForeignKey('user_state.line_id'),
        nullable=False,
        info={"verbose_name": "UserState LineID"}
    )
    user_state = relationship(
        "UserState",
        back_populates="input_histories"
    )
    input_text = Column(
        Text,
        nullable=True,
        info={"verbose_name": "用戶輸入的文字"}
    )

    def __repr__(self):
        return f"<UserInputHistory:{self.id}>"
