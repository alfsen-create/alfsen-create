class Node:
    def __init__(self, node_id, node_type, creation_timestamp, last_modified_timestamp,
                 salience_score=0.0, cognitive_thread_id_ref=None,
                 internal_code_chunk_ref=None, embedded_context=None,
                 type_specific=None):
        self.node_id = node_id
        self.node_type = node_type
        self.creation_timestamp = creation_timestamp
        self.last_modified_timestamp = last_modified_timestamp
        self.salience_score = salience_score
        self.cognitive_thread_id_ref = cognitive_thread_id_ref
        self.internal_code_chunk_ref = internal_code_chunk_ref
        self.embedded_context = embedded_context or []
        self.type_specific = type_specific or {}

    def dict(self):
        return {
            'node_id': self.node_id,
            'node_type': self.node_type,
            'creation_timestamp': self.creation_timestamp,
            'last_modified_timestamp': self.last_modified_timestamp,
            'salience_score': self.salience_score,
            'cognitive_thread_id_ref': self.cognitive_thread_id_ref,
            'internal_code_chunk_ref': self.internal_code_chunk_ref,
            'embedded_context': self.embedded_context,
            'type_specific': self.type_specific,
        }

class ETGGraph:
    def __init__(self, meta=None, nodes=None, edges=None):
        self.meta = meta or {}
        self.nodes = nodes or []
        self.edges = edges or []

    def add_node(self, node_dict):
        self.nodes.append(node_dict)
        return node_dict
