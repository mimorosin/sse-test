"""정적 분석 샘플: NoSQL Injection 및 안전하지 않은 $where."""

from typing import Any


def find_user_mongo(collection, username: Any):
    # username이 dict이면 연산자 주입 가능 ({"$ne": null} 등)
    return collection.find_one({"username": username})


def search_with_where(collection, expr: str):
    # $where에 사용자 입력을 문자열로 전달 -> JS 실행
    return list(collection.find({"$where": "this.name == '" + expr + "'"}))


def aggregate_by_role(collection, role_filter: Any):
    pipeline = [{"$match": {"role": role_filter}}, {"$group": {"_id": "$team", "n": {"$sum": 1}}}]
    return list(collection.aggregate(pipeline))
