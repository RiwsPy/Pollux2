from django.contrib import admin
from django import forms
from django.urls import path
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.gis.geos import Point

from .models import LampsMairin00, LampsCoccia00
from pollux.admin import LampsAdmin
import json


class CsvImportForm(forms.Form):
    file_upload = forms.FileField()


@admin.register(LampsMairin00)
class LampsUserAdmin(LampsAdmin):
    model_name = "LampsMairin00"
    model = LampsMairin00

    @property
    def readonly_fields(self):
        return super().readonly_fields + ["lat", "lng"]

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path("upload-file/", self.upload_file)]
        return new_urls + urls

    def upload_file(self, request):
        if request.method == "POST":
            db_file = request.FILES["file_upload"]

            if db_file.content_type == "application/json":
                self.upload_json(db_file)
            elif db_file.content_type == "text/csv":
                self.upload_csv(db_file)
            else:
                messages.warning(request, "Extension de fichier non reconnue.")
                return HttpResponseRedirect(request.path_info)

            url = reverse(f"admin:bank_{self.model_name.lower()}_changelist")
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/file_upload.html", data)

    def upload_csv(self, csv_file) -> None:
        file_data = csv_file.read().decode("utf-8")
        csv_data = file_data.split("\n")

        for lamp_data in csv_data:
            fields = lamp_data.split(',')
            try:
                self.model.objects.update_or_create(
                    code=fields[0] or self.model.code.field.default,
                    height=fields[1] or self.model.height.field.default,
                    irc=fields[2] or self.model.irc.field.default,
                    power=fields[3] or self.model.power.field.default,
                    colour=fields[4] or self.model.colour.field.default,
                    lng=float(fields[6]),
                    lat=float(fields[5]),
                    position=Point(float(fields[6]), float(fields[5])),  # (lng, lat)
                )
            except IndexError:
                continue

    def upload_json(self, json_file) -> None:
        json_data = json.load(json_file)
        for feat in json_data["features"]:
            self.model.objects.update_or_create(
                position=Point(feat["geometry"]["coordinates"]), **feat["properties"]
            )


@admin.register(LampsCoccia00)
class LampsUserAdmin02(LampsUserAdmin):
    model_name = "LampsCoccia00"
    model = LampsCoccia00
