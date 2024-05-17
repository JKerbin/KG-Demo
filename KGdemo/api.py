from flask import Flask, request, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# Neo4j数据库连接信息
uri = "bolt://localhost:7687"
username = ""
password = ""


# 定义Neo4j会话类
class KnowledgeGraph:
    # TODO: 带有安全验证的数据库初始化
    # def __init__(self, neo4j_uri, neo4j_user, neo4jpw):
    #     self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4jpw))

    def __init__(self, neo4j_uri):
        self.driver = GraphDatabase.driver(neo4j_uri)

    # 查询知识图谱
    def search(self, query):
        with self.driver.session() as session:
            return session.read_transaction(self._search, query)

    @staticmethod
    def _search(tx, query):
        result = tx.run("MATCH (n) WHERE n.name CONTAINS $query RETURN n.name", query=query)
        return [record["n.name"] for record in result]


# 实例化知识图谱
graph = KnowledgeGraph(uri)


# 定义搜索API路由
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    results = graph.search(query)
    return jsonify({'results': results})


if __name__ == '__main__':
    app.run(debug=True)
