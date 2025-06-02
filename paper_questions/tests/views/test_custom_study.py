from typing import Optional
from django.test import TestCase

from bs4 import BeautifulSoup, Tag
from bs4.element import PageElement, AttributeValueList
from django.urls import reverse
from django.core.management import call_command
from urllib.parse import urlparse


class HomePageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("collectstatic", interactive=False)

    def test_custom_study(self):
        """
        I can start a custom study session from the homepage
        """
        # Given I am on the homepage
        homepage = self.client.get(reverse("paper_questions:home"))
        self.assertEqual(homepage.status_code, 200)
        soup = BeautifulSoup(homepage.content, "html.parser")

        # When I click the "custom study" link
        custom_study_anchor: Optional[PageElement] = soup.find(
            "a", attrs={"aria-label": "custom study"}
        )
        assert isinstance(custom_study_anchor, Tag), "'custom study' link not found"

        custom_study_href: Optional[str] | AttributeValueList = custom_study_anchor.get(
            "href"
        )
        assert isinstance(custom_study_href, str), "'custom study' href not present"
        custom_study_page = self.client.get(custom_study_href, follow=True)
        soup = BeautifulSoup(custom_study_page.content, "html.parser")

        # I am presented with a list of subjects
        subjects_list: Optional[PageElement] = soup.find(
            "fieldset", attrs={"aria-label": "subjects"}
        )
        assert isinstance(subjects_list, Tag), "'subjects' list not found"

        # I am presented with a list of difficulties
        subjects_list: Optional[PageElement] = soup.find(
            "fieldset", attrs={"aria-label": "difficulties"}
        )
        assert isinstance(subjects_list, Tag), "'difficulties' list not found"

        # When I select a "computer architecture" and "not attempted" and "medium" questions, and submit the form
        form = soup.find("form", attrs={"aria-label": "custom_study"})
        assert isinstance(form, Tag)
        action = form.get("action")
        method = form.get("method", "get")
        assert isinstance(method, str)
        method = method.lower()
        form_data = {
            "difficulties": ["0", "2"],
            "subjects": ["comp_arch", "data"],
        }
        if method == "post":
            post_response = self.client.post(action, data=form_data, follow=True)
        else:
            post_response = self.client.get(action, data=form_data, follow=True)
        # I have started the correct custom study session
        self.assertEqual(post_response.status_code, 200)
        url = urlparse(
            post_response.redirect_chain[-1][0]
            if post_response.redirect_chain
            else post_response.request["PATH_INFO"]
        )
        segments = [segment for segment in url.path.split("/") if segment]
        print(url.path.split("/"))
        print(segments)
        subjects, difficulties = segments[1], segments[2]
        self.assertEqual(subjects, "comp_arch-data")
        self.assertEqual(difficulties, "0-2")
