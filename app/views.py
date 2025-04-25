from os.path import isfile, join, isdir

from django.db import connection
from django.shortcuts import render
from os import listdir

from django.views.generic import TemplateView

class index(TemplateView):
    template_name = "query_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rtrn_files = []
        list_of_files = listdir("sql/")
        for f in list_of_files:
            if isfile(join("sql/", f)):
                rtrn_files.append(f)
            elif isdir(join("sql/", f)):
                new_file = [f]
                for j in listdir(join("sql/", f)):
                    new_file.append(j)
                rtrn_files.append(new_file)
        context["files"] = rtrn_files
        return context


class query(TemplateView):
    template_name = "query.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file = open("sql/"+context["type"]+"/"+context["filename"], "r")
        content = file.read()
        file.close()

        with connection.cursor() as cursor:
            cursor.execute(content)
            context["query"] = cursor.fetchall()
        return context