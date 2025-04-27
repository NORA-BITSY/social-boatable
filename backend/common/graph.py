from functools import lru_cache
from neo4j import GraphDatabase
from .config import get_settings

@lru_cache()
def get_driver():
    settings = get_settings()
    uri = settings.neo4j_uri
    # expects credentials in URI  bolt://user:pass@host:7687 or via env NEO4J_USER/PASS
    return GraphDatabase.driver(uri)


# Convenience query context manager
class Neo4jSession:
    def __enter__(self):
        self._session = get_driver().session()
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

def record_follow(follower_id: int, followed_id: int):
    with Neo4jSession() as s:
        s.run("""
            MERGE (a:User {id:$f1}) MERGE (b:User {id:$f2})
            MERGE (a)-[:FOLLOWS]->(b)
        """, f1=follower_id, f2=followed_id)

def followed_ids(user_id: int) -> set[int]:
    query = "MATCH (u:User {id: $uid})-[:FOLLOWS]->(f:User) RETURN f.id AS fid"
    # Use a new session for the query
    with get_driver().session() as session:
        result = session.run(query, uid=user_id)
        return {record["fid"] for record in result}
