from ast import dump
from dbm import dumb
from Acquisition import aq_inner
from plone import api
from plone.app.dexterity.behaviors.metadata import IPublication
from plone.app.multilingual.interfaces import ITranslationManager
from plone.app.textfield.value import RichTextValue
from plone.i18n.normalizer import idnormalizer
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.namedfile.file import NamedBlobFile
from plone.protect.interfaces import IDisableCSRFProtection
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from pytz import timezone
from zope.component import getUtility
from zope.interface import alsoProvides

import dateutil.parser
import requests
import json

"""
OHARRA: Oraingo webgunearen kontra egin inportazioa.
Information atalean bestela html-a ez dator ongi.
"""


class ImportView(BrowserView):
    def __call__(self):
        context = aq_inner(self.context)
        request = self.request
        alsoProvides(request, IDisableCSRFProtection)
        if context.Language() == "eu":
            resource_url = "http://localhost:2080/mankomunitatea/eu/herritarrentzako-arreta-eta-tramiteak/tramiteak/lan-eskaintzak/export_laneskaintzak"
            # resource_url = "http://localhost:8098/oinati/eu/export_kontratazioak"
        else:
            resource_url = "http://localhost:2080/mankomunitatea/es/atencion-al-ciudadano-y-tramites/tramites/oferta-de-empleo/export_laneskaintzak"
            # resource_url = "http://localhost:8098/oinati/es/export_kontratazioak"
        r = requests.get(resource_url, auth=("admintest", "admintest"))
        response = r.json()

        for item in response:
            contract = context.get(item.get("id"), None)
            if not (contract):
                context.invokeFactory(type_name="Contract", id=item.get("id"))
            contract = context.get(item.get("id"), None)
            contract.title = item.get("title")
            # contract.file_number = item.get("file_number")
            contract.state = item.get("situation")
            if item.get("portal_type") == "laneskaintza":
                contract.text = RichTextValue(
                    item.get("information"), "text/html", "text/html"
                )
                date_fields = [
                    "start_data",
                    "end_data",
                    "start_data_bog",
                    "prensa_data",
                    "file_enrolled_data",
                    "final_file_enrolled_data",
                    "file_exercise_results_data",
                ]
                file_fields = [
                    "modelo_instancia",
                    "temario",
                    "file_information",
                    "file_prensa",
                    "file_enrolled",
                    "final_file_enrolled",
                    "file_exercise_results",
                ]
            elif item.get("portal_type") == "kontratazioa":
                info_fields = [
                    "lizitazio_aurrekontua",
                    "documentation",
                    "attach1_information",
                    "behin_behineko_adjudikazioduna",
                    "behin_behineko_adjudikazioaren_zenbatekoa",
                    "behin_betiko_adjudikazioduna",
                    "behin_betiko_adjudikazioaren_zenbatekoa",
                ]
                info_html = u""
                for info_field in info_fields:
                    info_dict = item[info_field]
                    info_title = info_dict["title"]
                    info_value = info_dict["value"]
                    if info_value:
                        info_html += u"<h3>{}</h3>".format(info_title)
                        info_html += info_value

                contract.info = RichTextValue(
                    info_html, "text/html", "text/html"
                )

                date_fields = [
                    "published_date",
                    "published_date_boletin",
                    "organo_contratacion_date",
                    "last_date",
                    "eskaintza_ekonomikoa_date",
                    "kontratuasinatu_date",
                    "behin_behineko_adjudikazio_date",
                    "behin_behineko_profile_date",
                    "behin_betiko_adjudikazio_date",
                    "behin_betiko_profile_date",
                ]
                file_fields = [
                    "attach1",
                    "attach2",
                    "attach3",
                    "attach4",
                    "behin_behineko_file",
                    "behin_betiko_file",
                ]

                normalizer = getUtility(IIDNormalizer)
                contract.file_state = normalizer.normalize(
                    item.get("situation")
                )
                contract.file_type = normalizer.normalize(
                    item.get("contract_type")
                )
                contract.file_processing = normalizer.normalize(
                    item.get("izapidea")
                )
                contract.file_procedure = normalizer.normalize(
                    item.get("process")
                )
                contract.file_organization = normalizer.normalize(
                    item.get("organization")
                )
                contract.file_body = normalizer.normalize(
                    item.get("kontratazio_organoa")
                )

            madrid = timezone("Europe/Madrid")
            date_list = []
            i = 1
            for date_element in date_fields:
                date = item.get(date_element)
                date_date = date["value"]
                if date_date:
                    # bbb = dateutil.parser.parse(date_date).astimezone(madrid)
                    date_list.append(
                        {
                            "@id": i,
                            "title": date["title"],
                            "date": date_date,
                        }
                    )
                    i += 1

            if item["effective"]:
                bbb = dateutil.parser.parse(item["effective"]).astimezone(
                    madrid
                )
                contract.setEffectiveDate(bbb)

            if "last_date" in item.keys():
                if item["last_date"]["value"]:
                    # bbb = dateutil.parser.parse(
                    #     item["last_date"]["value"]
                    # ).astimezone(madrid)
                    contract.last_date = item["last_date"]["value"]
            contract.dates = {"items": date_list}

            for file_field_id in file_fields:
                file_field = item.get(file_field_id)
                file_filename = file_field["filename"]
                file_url = file_field["url"]
                file_title = file_field["title"]
                if file_filename:
                    r_file = requests.get(
                        file_url, auth=("admintest", "admintest")
                    )
                    file_file = r_file.content
                    new_file = contract.get(
                        idnormalizer.normalize(file_filename), None
                    )
                    if not new_file:
                        try:
                            contract.invokeFactory(
                                type_name="File",
                                id=idnormalizer.normalize(file_filename),
                                title=file_title,
                            )
                        except:
                            a = 1
                            import pdb

                            pdb.set_trace()
                            b = 2
                    new_file = contract.get(
                        idnormalizer.normalize(file_filename), None
                    )
                    new_file.file = NamedBlobFile(
                        file_file, filename=file_filename
                    )

                    new_file.reindexObject()

            contract_state = item["state"]
            if contract_state in ["published", "visible"]:
                try:
                    context.portal_workflow.doActionFor(
                        contract,
                        action="publish",
                        wf_id="simple_publication_workflow",
                        comment="Automatically published",
                    )
                except:
                    pass

            try:
                contract_eu = item["translation_eu"]
                if context.Language() == "es":
                    if contract_eu:
                        contract_full_path = contract_eu.split("/")[-1]
                        context_translation = ITranslationManager(
                            context
                        ).get_translation("eu")
                        contract_eu_obj = context_translation.get(
                            contract_full_path
                        )
                        if contract_eu_obj:
                            ITranslationManager(contract).register_translation(
                                "eu", contract_eu_obj
                            )
            except:
                pass
            contract.reindexObject()
        return 1
