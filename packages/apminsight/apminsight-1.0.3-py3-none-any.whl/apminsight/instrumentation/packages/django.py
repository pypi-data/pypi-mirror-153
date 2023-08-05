
from apminsight import constants
from apminsight.instrumentation.wrapper import wsgi_wrapper

module_info = {
    'django.core.handlers.wsgi' : [
        {
            constants.class_str : 'WSGIHandler',
            constants.method_str : '__call__',
            constants.wrapper_str : wsgi_wrapper,
            constants.component_str : constants.django_comp
        }
    ],
    'django.conf.urls' : [
        {
            constants.method_str : 'url',
            constants.wrap_args : 1,
            constants.component_str : constants.django_comp
        }
    ],
    'django.urls' : [
        {
            constants.method_str : 'path',
            constants.wrap_args : 1,
            constants.component_str : constants.django_comp
        }
    ],
    'django.template' : [
        {
            constants.class_str : 'Template',
            constants.method_str : 'render',
            constants.component_str : constants.template
        }
    ]
}