#!/usr/bin/env python
#coding=utf-8
u"""Модуль содержит описания схем json-данных, таких как настройки агента, его задач и пр."""


CORE = {
    u'$schema': u'http://json-schema.org/draft-03/schema#',
    u'id': u'http://json-schema.org/draft-03/schema#',
    u'type': u'object',
    u'properties': {
        u'type': {
            u'type': [u'string', u'array'],
            u'items': {
                u'type': [u'string', {u'$ref': u'#'}]
            },
            u'uniqueItems': True,
            u'default': u'any'
        },
        u'properties': {
            u'type': u'object',
            u'additionalProperties': {u'$ref': u'#'},
            u'default': {}
        },
        u'patternProperties': {
            u'type': u'object',
            u'additionalProperties': {u'$ref': u'#'},
            u'default': {}
        },
        u'additionalProperties': {
            u'type': [{u'$ref': u'#'}, u'boolean'],
            u'default': {}
        },
        u'items': {
            u'type': [{u'$ref': u'#'}, u'array'],
            u'items': {u'$ref': u'#'},
            u'default': {}
        },
        u'additionalItems': {
            u'type': [{u'$ref': u'#'}, u'boolean'],
            u'default': {}
        },
        u'required': {
            u'type': u'boolean',
            u'default': False
        },
        u'dependencies': {
            u'type': u'object',
            u'additionalProperties': {
                u'type': [u'string', u'array', {u'$ref': u'#'}],
                u'items': {u'type': u'string'}
            },
            u'default': {}
        },
        u'minimum': {
            u'type': u'number'
        },
        u'maximum': {
            u'type': u'number'
        },
        u'exclusiveMinimum': {
            u'type': u'boolean',
            u'default': False
        },
        u'exclusiveMaximum': {
            u'type': u'boolean',
            u'default': False
        },
        u'minItems': {
            u'type': u'integer',
            u'minimum': 0,
            u'default': 0
        },
        u'maxItems': {
                u'type': u'integer',
                u'minimum': 0
        },
        u'uniqueItems': {
            u'type': u'boolean',
            u'default': False
        },
        u'pattern': {
            u'type': u'string',
            u'format': u'regex'
        },
        u'minLength': {
            u'type': u'integer',
            u'minimum': 0,
            u'default': 0
        },
        u'maxLength': {
            u'type': u'integer'
        },
        u'enum': {
            u'type': u'array',
            u'minItems': 1,
            u'uniqueItems': True
        },
        u'default': {
            u'type': u'any'
        },
        u'title': {
            u'type': u'string'
        },
        u'description': {
            u'type': u'string'
        },
        u'format': {
            u'type': u'string'
        },
        u'divisibleBy': {
            u'type': u'number',
            u'minimum': 0,
            u'exclusiveMinimum': True,
            u'default': 1
        },
        u'disallow': {
            u'type': [u'string', u'array'],
            u'items': {
                    u'type': [u'string', {u'$ref': u'#'}]
            },
            u'uniqueItems': True
        },
        u'extends': {
            u'type': [{u'$ref': u'#'}, u'array'],
            u'items': {u'$ref': u'#'},
            u'default': {}
        },
        u'id': {
            u'type': u'string',
            u'format': u'uri'
        },
        u'$ref': {
            u'type': u'string',
            u'format': u'uri'
        },
        u'$schema': {
            u'type': u'string',
            u'format': u'uri'
        }
    },
    u'dependencies': {
        u'exclusiveMinimum': u'minimum',
        u'exclusiveMaximum': u'maximum'
    },
    u'default': {}
}

AGENT_TASK = {
    u'title': u'Задача агента',
    u'type': u'object',
    u'properties': {
        u'name': {u'type': u'string', u'required': True},
        u'display_name': {u'type': u'string'},
        u'active': {u'type': u'boolean', u'required': True},
        u'params': {u'type': u'object'},
        u'schedule': {
            u'type': u'object',
            u'required': True,
            u'properties': {
                u'cron': {u'type': u'string', u'required': True},
                u'start': {u'type': u'string', u'format': u'date-time'},
                u'stop': {u'type': u'string', u'format': u'date-time'}
            }
        },
        u'executable': {
            u'type': u'object',
            u'required': True,
            u'properties':{
                u'module': {u'type': u'string', u'required': True, u'pattern': ur'[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*'},
                u'func': {u'type': u'string', u'required': True, u'pattern': ur'[a-zA-Z0-9_]+'}
            },
        },
        u'log_file': {u'type': u'string', u'blank': True},
        u'sys_log': {u'type': u'boolean', u'default': False},
        u'log_level': {u'type': u'string', u'default': u'warning', u'enum': [u'debug', u'info', u'warning', u'error', u'critical']}
    }
}

AGENT_SETTINGS = {
    u'title': u'Настройки агента',
    u'type': u'object',
    u'properties': {
        u'service':{
            u'type': u'object',
            u'properties':{
                u'start_type': {u'type': u'integer', u'default': 3, u'enum': [2, 3, 4]},
                u'err_control': {u'type': u'integer', u'default': 1, u'enum': [0, 1, 2, 3]},
                u'interactive': {u'type': u'boolean', u'default': False},
                u'username': {u'type': u'string'},
                u'password': {u'type': u'string'}
            },
            u'dependencies':{
                u'password': u'username'
            }
        },
        u'path': {u'type': u'string', u'required': True},
        u'log_file': {u'type': u'string', u'blank': True},
        u'sys_log': {u'type': u'boolean', u'default': False},
        u'log_level': {u'type': u'string', u'default': u'warning', u'enum': [u'debug', u'info', u'warning', u'error', u'critical']}
    }
}

#TODO: implement schema for menu description
MENU = {
    u'title': u'Описание меню',
    u'type': u'object',
}