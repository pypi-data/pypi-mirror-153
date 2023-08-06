# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from plone.app.multilingual.api import get_translation_manager
from Products.EasyNewsletter.interfaces import IIssueDataFetcher
from Products.EasyNewsletter.issuedatafetcher import DefaultDXIssueDataFetcher
from zope.interface import implementer


@implementer(IIssueDataFetcher)
class CombindSendDXIssueDataFetcher(DefaultDXIssueDataFetcher):
    """ """

    def _render_output_html(self, preview=False):
        """Return rendered newsletter
        with header+body+footer with all translations combined (raw html)
        except when preview=True, than just render current issue.
        """
        output_html = ""
        if preview:
            output_tmpl_id = self.issue.output_template
            issue_tmpl = self.issue.restrictedTraverse(str(output_tmpl_id))
            return issue_tmpl.render()

        tlm = get_translation_manager(self.issue)
        translations = tlm.get_translations()
        for lang, issue in translations.items():
            output_tmpl_id = issue.output_template
            issue_tmpl = issue.restrictedTraverse(str(output_tmpl_id))
            output_html_part = issue_tmpl.render()
            if output_html:
                # only use the real content, for every additional translation
                # and insert it into body tag of first output_html_part
                # output_html_part = "test additional languages\n"
                output_html = self._merge_content(output_html, output_html_part, lang)
            else:
                output_html = output_html_part
        return output_html

    def _merge_content(self, output_html, output_html_part, lang):
        part_soup = BeautifulSoup(output_html_part, "html.parser")
        output_soup = BeautifulSoup(output_html, "html.parser")
        content_parts = part_soup.select("#emailBody")
        anker_link_ref = "#lang_{0}".format(lang)
        anker_tag_name = "lang_{0}".format(lang)
        anker_link_wrapper = output_soup.new_tag("p")
        anker_link_wrapper.string = "> "
        anker_link = output_soup.new_tag("a", href=anker_link_ref)
        anker_link.string = "english version below"
        anker_link["class"] = "english_version_below_link"
        anker_link_wrapper.append(anker_link)
        output_soup.select(".enlHeaderContent")[0].insert(0, anker_link_wrapper)
        anker_tag = output_soup.new_tag("a")
        anker_tag["name"] = anker_tag_name
        output_soup.select(".aggregatedContentSlot")[0].append(anker_tag)
        for part in content_parts:
            output_soup.select(".aggregatedContentSlot")[0].append(part)
        return str(output_soup)
