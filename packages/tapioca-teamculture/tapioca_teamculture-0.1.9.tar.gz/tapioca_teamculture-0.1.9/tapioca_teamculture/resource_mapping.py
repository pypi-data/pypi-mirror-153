# coding: utf-8

RESOURCE_MAPPING = {
    'attributes': {
        'resource': 'attributes',
        'methods': ['GET', 'POST']
    },
    'attribute': {
        'resource': 'attributes/{id}',
        'methods': ['GET', 'PUT']
    },
    'groups': {
        'resource': 'groups',
        'methods': ['GET']
    },
    'group_create': {
        'resource': 'v2/groups',
        'methods': ['POST']
    },
    'group_inactivate': {
        'resource': 'groups/{id}/inactivation',
        'methods': ['POST']
    },
    'group_activate': {
        'resource': 'groups/{id}/activation',
        'methods': ['POST']
    },
    'tree': {
        'resource': 'groups/tree',
        'methods': ['GET']
    },
    'user': {
        'resource': 'users/{email}',
        'methods': ['GET', 'DELETE']
    },
    'users': {
        'resource': 'users',
        'methods': ['GET', 'POST']
    },
    'user_create': {
        'resource': 'v2/users',
        'methods': ['POST']
    },
    'user_reactivate': {
        'resource': 'users/{email}/reactivate',
        'methods': ['PUT']
    },
    'user_undo_inactivation': {
        'resource': 'users/{email}/undo-inactivate',
        'methods': ['PUT']
    },
    'action_plans': {
        'resource': 'action-plans',
        'methods': ['GET']
    },
    'engagement_participation': {
        'resource': 'engagement/{group_id}/participations',
        'methods': ['GET']
    },
    'engagement': {
        'resource': 'engagement/{group_id}',
        'methods': ['GET']
    }
}
