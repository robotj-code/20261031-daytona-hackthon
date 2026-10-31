import configparser
from neo4j import GraphDatabase

# Load configuration from .secret.ini
config = configparser.ConfigParser()
config.read('.secret.ini')

NEO4J_URI = config.get('neo4j', 'uri')
NEO4J_USER = config.get('neo4j', 'username')
NEO4J_PASSWORD = config.get('neo4j', 'password')
NEO4J_DB = config.get('neo4j', 'database')

# Comprehensive multi-tier supply chain portfolio dataset for Case 1 & Case 2 demo
portfolio_data = {
  "nodes": [
    {"id": "entity_001", "name": "Apex Auto Group", "type": "PortfolioCompany"},
    {"id": "entity_002", "name": "Titan Battery Systems", "type": "Tier1Supplier"},
    {"id": "entity_003", "name": "Lithium Dynamic Core", "type": "Tier2Supplier"},
    {"id": "entity_004", "name": "Valence Microchips", "type": "Tier1Supplier"},
    {"id": "entity_005", "name": "Global Freight Logistics", "type": "LogisticsPartner"},
    {"id": "entity_006", "name": "Red Sea Shipping Route", "type": "GeopoliticalZone"},
    {"id": "entity_007", "name": "Sovereign Risk Index", "type": "MacroMetric"},
    {"id": "entity_008", "name": "Quantum Robotics Corp", "type": "PortfolioCompany"}
  ],
  "relationships": [
    {"source": "entity_001", "target": "entity_002", "type": "DEPENDS_ON"},
    {"source": "entity_001", "target": "entity_004", "type": "DEPENDS_ON"},
    {"source": "entity_002", "target": "entity_003", "type": "SUPPLIED_BY"},
    {"source": "entity_002", "target": "entity_005", "type": "SHIPS_VIA"},
    {"source": "entity_004", "target": "entity_005", "type": "SHIPS_VIA"},
    {"source": "entity_005", "target": "entity_006", "type": "OPERATES_IN"},
    {"source": "entity_006", "target": "entity_007", "type": "IMPACTED_BY"},
    {"source": "entity_008", "target": "entity_004", "type": "DEPENDS_ON"},
    {"source": "entity_008", "target": "entity_005", "type": "SHIPS_VIA"}
  ]
}

def seed_database():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    print("🌱 Seeding Neo4j database with multi-tier portfolio risk graph...")
    
    with driver.session(database=NEO4J_DB) as session:
        # Clear existing graph data to start fresh
        session.run("MATCH (n) DETACH DELETE n")
        
        # Create Nodes
        for node in portfolio_data["nodes"]:
            session.run(
                "CREATE (n:Entity {id: $id, name: $name, type: $type})",
                id=node["id"], name=node["name"], type=node["type"]
            )
        
        # Create Relationships
        for rel in portfolio_data["relationships"]:
            query = f"""
            MATCH (a:Entity {{id: $source}}), (b:Entity {{id: $target}})
            CREATE (a)-[:{rel["type"]}]->(b)
            """
            session.run(query, source=rel["source"], target=rel["target"])
            
    print("✅ Seeding complete! Added 8 nodes and 9 multi-tier relationships.")
    driver.close()

if __name__ == "__main__":
    seed_database()