from causality.model.Schema import Schema
from causality.learning.RCD import RCD
from causality.citest.CITest import LinearCITest
from causality.datastore.PostgreSqlDataStore import PostgreSqlDataStore
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

schema = Schema()

# Core Entities
schema.addEntity('Game')
schema.addAttribute('Game', 'outcome')
schema.addAttribute('Game', 'awaystrength')

schema.addEntity('PGS')  # Player Game Stats
schema.addAttribute('PGS', 'points')
schema.addAttribute('PGS', 'assists')
schema.addAttribute('PGS', 'pct')
schema.addAttribute('PGS', 'tov')

schema.addEntity('TGS')  # Team Game Stats
schema.addAttribute('TGS', 'tpts')
schema.addAttribute('TGS', 'opts')

# Mapping Relationships
schema.addRelationship('PGSM', 
                       ('PGS', Schema.ONE), 
                       ('Game', Schema.MANY))

schema.addRelationship('TGSM', 
                       ('TGS', Schema.ONE), 
                       ('Game', Schema.MANY))
logger.info(schema)

# NB: Following step requires prior loading of rcd-test-data.sql into the test database.
dataStore = PostgreSqlDataStore(dbname='nba_syntactic', user='postgres', password='test', host='localhost', port='5432')
linearCITest = LinearCITest(schema, dataStore)

hopThreshold = 4
rcd = RCD(schema, linearCITest, hopThreshold)
rcd.identifyUndirectedDependencies()
rcd.orientDependencies()