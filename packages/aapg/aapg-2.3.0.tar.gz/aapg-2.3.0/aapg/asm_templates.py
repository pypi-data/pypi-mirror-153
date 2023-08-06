"""
    Module to store pre-defined templates
"""

def prelude_template(args):
    stack_size = args['stack_size']
    return [
    ]

def recurse_sections(depth,reg1,reg2):
    return {
        'recurse_init': [
            ('li', 'a{}'.format(reg1), '{}'.format(depth))
        ],
        'recurse': [
            ('addi', 'sp', 'sp', '-32'),
            ('sw', 'ra', '28(sp)'),
            ('sw', 's0', '24(sp)'),
            ('addi', 's0', 'sp', '32'),
            ('sw', 'a{}'.format(reg1), '-20(s0)'),
            ('lw', 'a{}'.format(reg2), '-20(s0)'),
            ('bnez', 'a{}'.format(reg2), '.recurse.L4'),
            ('li', 'a{}'.format(reg2), '0'),
            ('j', '.recurse.L3')
        ],
        'recurse.L4': [
            ('lw', 'a{}'.format(reg2), '-20(s0)'),
            ('addi', 'a{}'.format(reg2), 'a{}'.format(reg2), '-1'),
            ('mv', 'a{}'.format(reg1), 'a{}'.format(reg2)),
            ('call', '.recurse')
        ],
        'recurse.L3': [
            ('mv', 'a{}'.format(reg1), 'a{}'.format(reg2)),
            ('LREGU', 'ra', '28(sp)'),
            ('LREGU', 's0', '24(sp)'),
            ('addi', 'sp', 'sp', '32'),
            ('jr',  'ra')
        ]
    }
