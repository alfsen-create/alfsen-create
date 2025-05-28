import uuid
import random
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from etg.graph import ETGGraph, Node
from sandbox.environment import GridEnvironment


def make_node_id():
    return str(uuid.uuid4())


# Two routines the Output node can use

def routine_move_right(agent, env):
    if env.agent_pos < env.size - 1:
        return 'right'
    else:
        return 'left'


def routine_random(agent, env):
    return random.choice(['left', 'right'])


# The Output node's CognitiveCatalyst logic

def catalyst_observe_and_adapt(output_node, recent_rewards):
    catalyst = output_node.type_specific.get('cognitive_catalyst')
    if not catalyst:
        return  # No catalyst present
    avg_reward = sum(recent_rewards) / len(recent_rewards) if recent_rewards else 0
    if avg_reward < 0.2 and catalyst['status'] != 'mutated':
        # Adaptation: swap routine!
        old_routine = output_node.internal_code_chunk_ref
        output_node.internal_code_chunk_ref = 'routine_random'
        catalyst['status'] = 'mutated'
        catalyst.setdefault('adaptation_log', []).append({
            'step': len(recent_rewards),
            'change_description': f'Swapped routine from {old_routine} to routine_random (avg_reward={avg_reward:.2f})'
        })
        print(f"\n\U0001F525 CognitiveCatalyst activated: Output node mutated from {old_routine} to routine_random!\n")


def agent_step(graph: ETGGraph, env: GridEnvironment, step_count: int, recent_rewards):
    # Percept node
    percept = env.get_percept()
    graph.add_node({
        'node_id': make_node_id(),
        'node_type': 'Percept',
        'creation_timestamp': f'step-{step_count}',
        'last_modified_timestamp': f'step-{step_count}',
        'salience_score': 0.7,
        'cognitive_thread_id_ref': 'default-thread',
        'internal_code_chunk_ref': None,
        'embedded_context': [float(percept)],
        'type_specific': {'sensor_data_type': 'object_presence', 'raw_data_payload': percept}
    })

    # Output node with CognitiveCatalyst
    if step_count == 0:
        output_node = Node(
            node_id=make_node_id(),
            node_type='Output',
            creation_timestamp=f'step-{step_count}',
            last_modified_timestamp=f'step-{step_count}',
            salience_score=0.8,
            cognitive_thread_id_ref='default-thread',
            internal_code_chunk_ref='routine_move_right',
            embedded_context=[],
            type_specific={
                'action_type': 'move',
                'cognitive_catalyst': {
                    'catalyst_id': 'cc-output-001',
                    'status': 'monitoring',
                    'observables': ['recent_rewards'],
                    'trigger_conditions': ['avg_reward < 0.2 for last 5 steps'],
                    'adaptation_protocol': 'swap_to_routine_random'
                }
            }
        )
        graph.add_node(output_node.dict())
        graph.agent_output_node = output_node
    else:
        output_node = graph.agent_output_node

    # Catalyst observation and potential adaptation
    catalyst_observe_and_adapt(output_node, recent_rewards)

    # Decide action using current routine
    routine_name = output_node.internal_code_chunk_ref
    routine = globals()[routine_name]
    action = routine(graph, env)

    # Action node (for ETG trace)
    graph.add_node({
        'node_id': make_node_id(),
        'node_type': 'Action',
        'creation_timestamp': f'step-{step_count}',
        'last_modified_timestamp': f'step-{step_count}',
        'salience_score': 0.8,
        'cognitive_thread_id_ref': 'default-thread',
        'internal_code_chunk_ref': routine_name,
        'embedded_context': [],
        'type_specific': {
            'action_type': action,
            'action_parameters': {'step': step_count, 'agent_pos': env.agent_pos},
            'target_interface': 'GridEnvironment'
        }
    })

    # Execute action
    percept, reward, done = env.take_action(action)
    recent_rewards.append(reward)
    if len(recent_rewards) > 5:
        recent_rewards.pop(0)

    # Memory node
    graph.add_node({
        'node_id': make_node_id(),
        'node_type': 'MemoryFragment',
        'creation_timestamp': f'step-{step_count}',
        'last_modified_timestamp': f'step-{step_count}',
        'salience_score': reward,
        'cognitive_thread_id_ref': 'default-thread',
        'internal_code_chunk_ref': None,
        'embedded_context': [float(percept), reward],
        'type_specific': {
            'content_payload': f"Step {step_count}: Action={action}, Reward={reward}",
            'temporal_tags': [f'step-{step_count}'],
            'episodic_context_links': []
        }
    })

    return done, action, reward


if __name__ == "__main__":
    graph = ETGGraph(meta={}, nodes=[], edges=[])
    env = GridEnvironment(size=10, object_pos=7)
    done = False
    step = 0
    recent_rewards = []
    print("Agent starts searching for the object. Output node will adapt if failing for 5 steps.")
    while not done and step < 20:
        done, action, reward = agent_step(graph, env, step, recent_rewards)
        print(f"Step {step}: Agent at {env.agent_pos}, action={action}, reward={reward}, done={done}")
        step += 1

    output_node = graph.agent_output_node
    print("\n--- CognitiveCatalyst Adaptation Log ---")
    print(output_node.type_specific['cognitive_catalyst'].get('adaptation_log', []))
    print("\nAgent stopped at position", env.agent_pos)
