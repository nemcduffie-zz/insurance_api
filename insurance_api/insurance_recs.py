from typing import Dict


INSURANCE_TYPES = {
    'needed': [
        {
            'type': 'Personal Liability',
            'conpany': 'Coya',
            'price_monthly': '€4.99'
        }, {
            'type': 'Job',
            'conpany': 'Community Life',
            'price_monthly': '€30.00'
        }
    ],
    'health': {
        'public': {
            'type': 'Health (Public)',
            'conpany': 'Techniker Krankenkasse',
            'price_monthly': '€281.25'
        },
        'private': {
            'type': 'Health (Private)',
            'conpany': 'Ottonova',
            'price_monthly': '€237.80'
        }
    },
    'children': {
        'type': 'Life',
        'conpany': 'Community Life',
        'price_monthly': '€20.00'
    },
    'optional': [
        {
            'type': 'Car',
            'conpany': 'Fri:day',
            'price_monthly': '€75.00'
        }, {
            'type': 'Household Content',
            'conpany': 'One Insurance',
            'price_monthly': '€7.50'
        }, 
    ]

}


def insurance_recs(User) -> Dict:
    recs = {
        'needed': INSURANCE_TYPES['needed'],
        'optional': INSURANCE_TYPES['optional'],
        'not_needed': []
    }
    if User.children:
        recs['needed'].append(INSURANCE_TYPES['children'])
    else:
        recs['not_needed'].append(INSURANCE_TYPES['children'])
    if User.occupation_type == 'Self-employed':
        recs['needed'].append(INSURANCE_TYPES['health']['private'])
        recs['not_needed'].append(INSURANCE_TYPES['health']['public'])
    else:
        recs['needed'].append(INSURANCE_TYPES['health']['public'])
        recs['not_needed'].append(INSURANCE_TYPES['health']['private'])
    return recs
