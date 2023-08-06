# -*- coding: utf-8 -*-
import unittest

from App.Common import package_home
from collective.easynewsletter_combined_send.testing import (
    COLLECTIVE_EASYNEWSLETTER_COMBINED_SEND_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.multilingual.api import translate
from plone.app.multilingual.interfaces import IPloneAppMultilingualInstalled
from plone.app.testing import TEST_USER_ID, setRoles
from plone.app.textfield import RichTextValue
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces.controlpanel import IMailSchema
from Products.CMFPlone.tests.utils import MockMailHost
from Products.EasyNewsletter.interfaces import IIssueDataFetcher
from Products.EasyNewsletter.utils.mail import get_portal_mail_settings
from Products.MailHost.interfaces import IMailHost
from zope.component import getSiteManager, getUtility
from zope.interface import alsoProvides

GLOBALS = globals()
TESTS_HOME = package_home(GLOBALS)


class IssuedatafetcherIntegrationTests(unittest.TestCase):
    layer = COLLECTIVE_EASYNEWSLETTER_COMBINED_SEND_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.portal_url()
        alsoProvides(self.layer["request"], IPloneAppMultilingualInstalled)

        # create EasyNewsletter instance and add some subscribers
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        # login(self.portal, TEST_USER_NAME)
        self.newsletter = api.content.create(
            container=self.portal["en"],
            type="Newsletter",
            id="enl1",
            title=u"ENL 1",
            sneder_email=u"newsletter@acme.com",
            sender_name=u"ACME newsletter",
            test_email=u"test@acme.com",
        )
        self.newsletter.output_template = "output_default"
        self.mail_settings = get_portal_mail_settings()
        # Set up a mock mailhost
        self.portal._original_MailHost = self.portal.MailHost
        self.portal.MailHost = mailhost = MockMailHost("MailHost")
        self.portal.MailHost.smtp_host = "localhost"
        registry = getUtility(IRegistry)
        self.mail_settings = registry.forInterface(IMailSchema, prefix="plone")
        self.mail_settings.email_from_address = "portal@plone.test"
        self.mail_settings.smtp_host = u"localhost"
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)
        # We need to fake a valid mail setup
        self.mailhost = self.portal.MailHost
        self.issue1 = api.content.create(
            container=self.newsletter,
            type="Newsletter Issue",
            id="issue1",
            title=u"This is a very long newsletter issue title with special "
            u"characters such as äüö. Will this really work?",
        )
        self.issue1.output_template = "output_default"
        body = "<h1>This is the newsletter content!</h1>"
        self.issue1.text = RichTextValue(
            raw=body,
            mimeType="text/html",
            outputMimeType="text/x-plone-outputfilters-html",
            encoding="utf-8",
        )

        self.newsletter_de = translate(self.newsletter, target_language="de")
        self.newsletter_de.output_template = "output_default"

        self.issue1_de = translate(self.issue1, target_language="de")
        self.issue1_de.title = u"Dies ist ein sehr langer Newsletter-Title, mit Umlauten wie äüö. Funktioniert das wirklich?"
        self.issue1_de.output_template = "output_default"
        body = "<h1>Dies ist der Newsletter Inhalt!</h1>"
        self.issue1_de.text = RichTextValue(
            raw=body,
            mimeType="text/html",
            outputMimeType="text/x-plone-outputfilters-html",
            encoding="utf-8",
        )

    def test_fetching_issue_data(self):
        issue_data_fetcher = IIssueDataFetcher(self.issue1)
        issue_data = issue_data_fetcher._render_output_html()
        self.assertIn("This is the newsletter content", issue_data)
        self.assertIn("Dies ist der Newsletter Inhalt", issue_data)
