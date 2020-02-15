# _*_ coding:utf-8 _*_
__author__ = 'geda'
__date__ = '2020/2/12 16:48'

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader
from  xadmin.plugins.utils import get_context_dict


# excel 导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        nodes.append(
            loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', get_context_dict(context)))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)
