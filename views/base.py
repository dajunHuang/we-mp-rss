from math import e
from fastapi import Request, Query
from core.db import DB
from core.models.feed import Feed
from core.models.article import Article
from driver.wxarticle import Web
from datetime import datetime
from core.models.tags import Tags
import json
#获取公众号视图数据
def get_mps_view(
    page: int ,
    limit: int 
): 
    session = DB.get_session()
    data={}
    try:
        # 查询标签总数
        total = session.query(Feed).filter(Feed.status == 1).count()
        
        # 计算偏移量
        offset = (page - 1) * limit

        # 查询公众号列表
        feeds = session.query(Feed).filter(Feed.status == 1).order_by(Feed.created_at.desc()).offset(offset).limit(limit).all()
        
        # 处理公众号数据
        feed_list = []
        for feed in feeds:
            # 对于 Feed 表，id 就是公众号的 ID
            mp_id = feed.id
            
            # 统计该公众号的文章数量
            article_count = session.query(Article).filter(
                Article.mp_id == mp_id,
                Article.status == 1
            ).count()
            
            feed_data = {
                "id": feed.id,
                "name": feed.mp_name,
                "cover": Web.get_image_url(feed.mp_cover) if feed.mp_cover else "",
                "intro": feed.mp_intro,
                "mp_count": 1,  # Feed 本身就是一个公众号
                "article_count": article_count,
                "sync_time": datetime.fromtimestamp(feed.sync_time).strftime('%Y-%m-%d %H:%M') if feed.sync_time else "未同步",
                "created_at": feed.created_at.strftime('%Y-%m-%d') if feed.created_at else ""
            }
            feed_list.append(feed_data)
        
        # 计算分页信息
        total_pages = (total + limit - 1) // limit
        has_prev = page > 1
        has_next = page < total_pages
        
        # 构建面包屑
        breadcrumb = [
            {"name": "公众号", "url": "/views/mps"}
        ]
        # 使用模板引擎渲染
        data={
            "feeds": feed_list,
            "current_page": page,
            "total_pages": total_pages,
            "total_items": total,
            "limit": limit,
            "has_prev": has_prev,
            "has_next": has_next,
            "breadcrumb": breadcrumb
        }
    except Exception as e:
        print(e)
    finally:
        session.close()
    return data



#显示所有标签，支持分页
def get_tags_view(
    page: int ,
    limit: int 
):
    """
    显示所有标签，支持分页
    """
    session = DB.get_session()
    data={}
    try:
        # 查询标签总数
        total = session.query(Tags).filter(Tags.status == 1).count()
        
        # 计算偏移量
        offset = (page - 1) * limit
        
        # 查询标签列表
        tags = session.query(Tags).filter(Tags.status == 1).order_by(Tags.created_at.desc()).offset(offset).limit(limit).all()
        
        # 处理标签数据
        tag_list = []
        for tag in tags:
            # 解析mps_id JSON
            mps_ids = []
            if tag.mps_id:
                try:
                    mps_data = json.loads(tag.mps_id)
                    mps_ids = [str(mp['id']) for mp in mps_data] if isinstance(mps_data, list) else []
                except (json.JSONDecodeError, TypeError):
                    mps_ids = []
            
            # 统计文章数量
            article_count = 0
            if mps_ids:
                article_count = session.query(Article).filter(
                    Article.mp_id.in_(mps_ids),
                    Article.status == 1
                ).count()
            
            # 获取关联的公众号数量
            mp_count = len(mps_ids) if mps_ids else 0
            
            tag_data = {
                "id": tag.id,
                "name": tag.name,
                "cover": Web.get_image_url(tag.cover) if tag.cover else "",
                "intro": tag.intro,
                "mp_count": mp_count,
                "article_count": article_count,
                "sync_time": datetime.fromtimestamp(tag.sync_time).strftime('%Y-%m-%d %H:%M') if tag.sync_time else "未同步",
                "created_at": tag.created_at.strftime('%Y-%m-%d') if tag.created_at else ""
            }
            tag_list.append(tag_data)
        
        # 计算分页信息
        total_pages = (total + limit - 1) // limit
        has_prev = page > 1
        has_next = page < total_pages
        
        # 构建面包屑
        breadcrumb = [
            {"name": "首页", "url": "/views/home"}
        ]
        
        data={
            "tags": tag_list,
            "current_page": page,
            "total_pages": total_pages,
            "total_items": total,
            "limit": limit,
            "has_prev": has_prev,
            "has_next": has_next,
        }
        
        
    except Exception as e:
        print(f"获取首页数据错误: {str(e)}")
    finally:
        session.close()
    return data