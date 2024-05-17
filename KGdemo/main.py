from neo4j import GraphDatabase

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

    # 创建节点和关系
    def create_graph(self):
        with self.driver.session() as session:
            session.write_transaction(self._create_graph)

    @staticmethod
    def _create_graph(tx):
        # 创建人物节点
        tx.run("CREATE (:Person {name: 'Alice'})")
        tx.run("CREATE (:Person {name: 'Bob'})")
        tx.run("CREATE (:Person {name: 'Charlie'})")

        # 创建关系
        tx.run("MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'}) "
               "CREATE (a)-[:KNOWS]->(b)")
        tx.run("MATCH (b:Person {name: 'Bob'}), (c:Person {name: 'Charlie'}) "
               "CREATE (b)-[:KNOWS]->(c)")

    # 查询知识图谱
    def query_graph(self):
        with self.driver.session() as session:
            return session.read_transaction(self._query_graph)

    @staticmethod
    def _query_graph(tx):
        result = tx.run("MATCH p=()-[:DIRECTED]->() RETURN p LIMIT 1")
        return [record["p"] for record in result]


# 运行示例
if __name__ == "__main__":
    graph = KnowledgeGraph(uri)

    # 创建知识图谱
    graph.create_graph()

    # 查询知识图谱
    res = graph.query_graph()
    print("Knowledge Graph:")
    for rec in res:
        print(rec)
