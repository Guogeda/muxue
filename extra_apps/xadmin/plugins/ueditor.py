# _*_ coding:utf-8 _*_
__author__ = 'geda'
__date__ = '2020/2/12 13:07'

import xadmin
from xadmin.views import BaseAdminPlugin, CreateAdminView, ModelFormAdminView, UpdateAdminView, ListAdminView
from DjangoUeditor.models import UEditorField
from DjangoUeditor.widgets import UEditorWidget
from django.conf import settings


class XadminUEditorWidget(UEditorWidget):
    def __init__(self, **kwargs):
        self.ueditor_options = kwargs
        self.Media.js = None
        super(XadminUEditorWidget, self).__init__(kwargs)


class UeditorPlugin(BaseAdminPlugin):
    isExecute = False

    def init_request(self, *args, **kwargs):
        return bool(self.isExecute)

    def get_field_style(self, attrs, db_field, style, **kwargs):
        if style == 'ueditor':
            if isinstance(db_field, UEditorField):
                widget = db_field.formfield().widget
                param = {}
                param.update(widget.ueditor_settings)
                param.update(widget.attrs)
                return {'widget': XadminUEditorWidget(**param)}
        return attrs

    def block_extrahead(self, context, nodes):
        js = '<script type="text/javascript" src="%s"></script>' % (
                settings.STATIC_URL + "ueditor/ueditor.config.js")  # 自己的静态目录
        js += '<script type="text/javascript" src="%s"></script>' % (
                settings.STATIC_URL + "ueditor/ueditor.all.js")  # 自己的静态目录
        nodes.append(js)


xadmin.site.register_plugin(UeditorPlugin, ListAdminView)
xadmin.site.register_plugin(UeditorPlugin, UpdateAdminView)
xadmin.site.register_plugin(UeditorPlugin, CreateAdminView)
