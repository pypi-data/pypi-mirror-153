# coding: utf-8

RESOURCE_MAPPING = {
    'groups': {
        'resource': 'groups',
        'methods': ['GET', 'POST']
    },
    'tree': {
        'resource': 'groups/tree',
        'methods': ['GET']
    },
    'users': {
        'resource': 'users',
        'methods': ['GET', 'POST']
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
