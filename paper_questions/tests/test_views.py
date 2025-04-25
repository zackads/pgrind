from typing import Optional
from django.test import TestCase

from bs4 import BeautifulSoup, Tag
from bs4.element import PageElement, AttributeValueList
from django.urls import reverse


class HomePageTests(TestCase):
    def test_random_question(self):
        """
        I can select a random question from the homepage
        """
        # Given I am on the homepage
        homepage = self.client.get(reverse("paper_questions:home"))
        self.assertEqual(homepage.status_code, 200)
        soup = BeautifulSoup(homepage.content, "html.parser")

        # When I click the "random question" link
        random_question_anchor: Optional[PageElement] = soup.find(
            "a", string="random question"
        )
        assert isinstance(
            random_question_anchor, Tag
        ), "'random question' link not found"
        random_question_href: Optional[str] | AttributeValueList = (
            random_question_anchor.get("href")
        )
        assert isinstance(
            random_question_href, str
        ), "'random question' href not present"
        random_question_page = self.client.get(random_question_href, follow=True)
        soup = BeautifulSoup(random_question_page.content, "html.parser")

        # I am presented with a question image
        question_img: Optional[PageElement] = soup.find("img")
        assert isinstance(question_img, Tag)
        question_img_src: Optional[str] | AttributeValueList = question_img.get("src")
        assert isinstance(question_img_src, str)
        self.assertEqual(self.client.get(question_img_src).status_code, 200)

        # When I click the "skip" link
        skip_anchor: Optional[PageElement] = soup.find(
            "a", attrs={"aria-label": "skip"}
        )
        assert isinstance(skip_anchor, Tag), "'skip' link not found"
        skip_href: Optional[str] | AttributeValueList = skip_anchor.get("href")
        assert isinstance(skip_href, str), "'skip' href not present"
        next_page = self.client.get(skip_href, follow=True)
        soup = BeautifulSoup(next_page.content, "html.parser")

        # I get a new question...
        self.assertTrue(random_question_href in next_page.request["PATH_INFO"])
        new_question_img: Optional[PageElement] = soup.find("img")
        assert isinstance(new_question_img, Tag)
        new_question_img_src: Optional[str] | AttributeValueList = new_question_img.get(
            "src"
        )
        assert isinstance(new_question_img_src, str)
        self.assertNotEqual(new_question_img_src, question_img_src)
        self.assertEqual(self.client.get(new_question_img_src).status_code, 200)
        question_url = next_page.request["PATH_INFO"]

        # ... and solution
        solution_anchor: Optional[PageElement] = soup.find(
            "a", attrs={"aria-label": "solution"}
        )
        assert isinstance(solution_anchor, Tag), "'solution' link not found"
        solution_href: Optional[str] | AttributeValueList = solution_anchor.get("href")
        assert isinstance(solution_href, str), "'solution' href not present"
        solution_page = self.client.get(solution_href, follow=True)
        soup = BeautifulSoup(solution_page.content, "html.parser")
        solution_img: Optional[PageElement] = soup.find("img")
        assert isinstance(solution_img, Tag)
        solution_img_src: Optional[str] | AttributeValueList = solution_img.get("src")
        assert isinstance(solution_img_src, str)
        self.assertEqual(self.client.get(solution_img_src).status_code, 200)

        # When I record how difficult I found the problem
        self.assertIsNotNone(
            soup.find("button", attrs={"aria-label": "confidence-easy"})
        )
        self.assertIsNotNone(
            soup.find("button", attrs={"aria-label": "confidence-medium"})
        )
        self.assertIsNotNone(
            soup.find("button", attrs={"aria-label": "confidence-hard"})
        )
        form = soup.find("form", attrs={"aria-label": "confidence"})
        assert isinstance(form, Tag)
        action = form.get("action")
        method = form.get("method", "get")
        assert isinstance(method, str)
        method = method.lower()
        hidden_inputs = form.find_all("input", type="hidden")
        form_data = {input["name"]: input["value"] for input in hidden_inputs}
        form_data["confidence"] = "2"  # Medium
        if method == "post":
            post_response = self.client.post(action, data=form_data, follow=True)
        else:
            post_response = self.client.get(action, data=form_data, follow=True)

        # I am presented with another question
        self.assertEqual(post_response.status_code, 200)
        self.assertTrue(random_question_href in next_page.request["PATH_INFO"])
        third_question_img: Optional[PageElement] = soup.find("img")
        assert isinstance(third_question_img, Tag)
        third_question_img_src: Optional[str] | AttributeValueList = (
            third_question_img.get("src")
        )
        assert isinstance(third_question_img_src, str)
        self.assertNotEqual(third_question_img, solution_img_src)
        self.assertEqual(self.client.get(third_question_img_src).status_code, 200)

        # When I go back to the homepage
        home_anchor: Optional[PageElement] = soup.find(
            "a", attrs={"aria-label": "home"}
        )
        assert isinstance(home_anchor, Tag), "'home' link not found"
        home_href: Optional[str] | AttributeValueList = home_anchor.get("href")
        assert isinstance(home_href, str), "'home' href not present"
        next_page = self.client.get(home_href, follow=True)
        soup = BeautifulSoup(next_page.content, "html.parser")

        # I can see my attempt has been recorded
        heatmap_cell_anchor = soup.find("a", attrs={"href": question_url})
        assert isinstance(heatmap_cell_anchor, Tag)
        cell = next(
            (
                child
                for child in heatmap_cell_anchor.contents
                if isinstance(child, Tag) and child.name == "li"
            ),
            None,
        )
        assert isinstance(cell, Tag)
        self.assertTrue("amber" in str(cell.get("class", "")))
