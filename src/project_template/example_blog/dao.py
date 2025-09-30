# -*- coding: utf-8 -*-
"""Data Access Objects for blog models.
   博客模型的数据访问对象。

This module provides generic and concrete DAO implementations for interacting
with SQLAlchemy models. It follows Google Python Style with bilingual
docstrings (English and Chinese) and includes type annotations.
本模块提供用于与 SQLAlchemy 模型交互的通用与具体 DAO 实现。
遵循 Google Python 风格，包含中英文文档字符串与类型注解。

Example:
    Basic usage::

        # Create an article
        article = ArticleDAO().create(session, CreateArticleSchema(...))

Attributes:
    None: This module does not expose module-level variables.
          本模块不暴露模块级变量。

Todo:
    * Add more DAOs when new models are introduced.
      当新增模型时补充更多 DAO。
"""

from typing import Generic, List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from project_template.example_blog.models import Article
from project_template.example_blog.schemas import (
    CreateArticleSchema,
    CreateSchema,
    ModelType,
    UpdateArticleSchema,
    UpdateSchema,
)


class BaseDAO(Generic[ModelType, CreateSchema, UpdateSchema]):
    """Base Data Access Object.
       基础数据访问对象。

    This generic DAO encapsulates common CRUD operations for SQLAlchemy
    models. Subclasses must set the ``model`` attribute to a concrete model
    class.
    该通用 DAO 封装了 SQLAlchemy 模型的常见 CRUD 操作。
    子类必须设置 ``model`` 属性为具体模型类。

    Attributes:
        model (ModelType): SQLAlchemy model class managed by the DAO.
                           DAO 管理的 SQLAlchemy 模型类。
    """

    model: ModelType

    def get(self, session: Session, offset: int = 0, limit: int = 10) -> List[ModelType]:
        """Return a list of model instances with pagination.
           使用分页返回模型实例列表。

        Args:
            session: Active SQLAlchemy session.
                     活动的 SQLAlchemy 会话。
            offset: Number of items to skip. 默认跳过的数量。
            limit: Maximum number of items to return. 返回的最大数量。

        Returns:
            List[ModelType]: Retrieved model instances.
                              获取到的模型实例列表。
        """
        result = session.query(self.model).offset(offset).limit(limit).all()
        return result

    def get_by_id(self, session: Session, pk: int) -> Optional[ModelType]:
        """Return a single model instance by primary key.
           通过主键返回单个模型实例。

        Args:
            session: Active SQLAlchemy session.
                     活动的 SQLAlchemy 会话。
            pk: Primary key value. 主键值。

        Returns:
            Optional[ModelType]: The model instance if found, else ``None``。
                                  若找到模型实例则返回，否则为 ``None``。
        """
        # Prefer Session.get for primary-key lookups in SQLAlchemy 1.4+
        return session.get(self.model, pk)

    def create(self, session: Session, obj_in: CreateSchema) -> ModelType:
        """Create and persist a new model instance.
           创建并持久化一个新的模型实例。

        Args:
            session: Active SQLAlchemy session.
                     活动的 SQLAlchemy 会话。
            obj_in: Pydantic schema with creation data.
                    携带创建数据的 Pydantic 模式对象。

        Returns:
            ModelType: The newly created and refreshed model instance.
                       新创建并刷新的模型实例。
        """
        obj = self.model(**jsonable_encoder(obj_in))
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def patch(self, session: Session, pk: int, obj_in: UpdateSchema) -> ModelType:
        """Partially update fields of a model instance.
           部分更新模型实例的字段。

        Args:
            session: Active SQLAlchemy session.
                     活动的 SQLAlchemy 会话。
            pk: Primary key of the target instance. 目标实例的主键。
            obj_in: Pydantic schema with fields to update.
                    携带待更新字段的 Pydantic 模式对象。

        Returns:
            ModelType: The updated and refreshed model instance.
                       已更新并刷新的模型实例。

        Raises:
            ValueError: If the target instance does not exist.
                        当目标实例不存在时。
        """
        obj = self.get_by_id(session, pk)
        if obj is None:
            raise ValueError(f"{getattr(self.model, '__name__', 'Model')} not found: {pk}")
        update_data = obj_in.dict(exclude_unset=True)
        for key, val in update_data.items():
            setattr(obj, key, val)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def delete(self, session: Session, pk: int) -> None:
        """Delete a model instance by primary key.
           通过主键删除模型实例。

        Args:
            session: Active SQLAlchemy session.
                     活动的 SQLAlchemy 会话。
            pk: Primary key of the target instance. 目标实例的主键。

        Raises:
            ValueError: If the target instance does not exist.
                        当目标实例不存在时。
        """
        obj = self.get_by_id(session, pk)
        if obj is None:
            raise ValueError(f"{getattr(self.model, '__name__', 'Model')} not found: {pk}")
        session.delete(obj)
        session.commit()

    def count(self, session: Session) -> int:
        """Return the total number of rows for the model.
           返回该模型的总记录数。

        Args:
            session: Active SQLAlchemy session.
                     活动的 SQLAlchemy 会话。

        Returns:
            int: Total count of model instances.
                 模型实例总数。
        """
        return session.query(self.model).count()


class ArticleDAO(BaseDAO[Article, CreateArticleSchema, UpdateArticleSchema]):
    """DAO implementation for the ``Article`` model.
       ``Article`` 模型的数据访问对象实现。

    Inherits CRUD operations from ``BaseDAO``.
    继承自 ``BaseDAO`` 的 CRUD 操作。
    """

    model = Article