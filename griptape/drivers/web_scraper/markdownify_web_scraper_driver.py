from typing import Optional
from attr import define, field, Factory
from griptape.artifacts import TextArtifact
from griptape.drivers import BaseWebScraperDriver
from griptape.utils import import_optional_dependency


@define
class MarkdownifyWebScraperDriver(BaseWebScraperDriver):
    """Driver to scrape a webpage and return the content in markdown format.

    As a prerequisite to using MarkdownifyWebScraperDriver, you need to install the browsers used by
    playwright. You can do this by running: `poetry run playwright install`.
    For more details about playwright, see https://playwright.dev/python/docs/library.

    Attributes:
        include_links: If `True`, the driver will include link urls in the markdown output.
        exclude_tags: Optionally provide custom tags to exclude from the scraped content.
        exclude_classes: Optionally provide custom classes to exclude from the scraped content.
        exclude_ids: Optionally provide custom ids to exclude from the scraped content.
        timeout: Optionally provide a timeout in milliseconds for the page to continue loading after
            the browser has emitted the "load" event.
    """

    include_links: bool = field(default=True, kw_only=True)
    exclude_tags: list[str] = field(
        default=Factory(lambda: ["script", "style", "head", "header", "footer", "svg"]), kw_only=True
    )
    exclude_classes: list[str] = field(default=Factory(list), kw_only=True)
    exclude_ids: list[str] = field(default=Factory(list), kw_only=True)
    timeout: Optional[int] = field(default=None, kw_only=True)

    def scrape_url(self, url: str) -> TextArtifact:
        sync_playwright = import_optional_dependency("playwright.sync_api").sync_playwright
        BeautifulSoup = import_optional_dependency("bs4").BeautifulSoup
        MarkdownConverter = import_optional_dependency("markdownify").MarkdownConverter

        include_links = self.include_links

        # Custom MarkdownConverter to optionally linked urls. If include_links is False only
        # the text of the link is returned.
        class OptionalLinksMarkdownConverter(MarkdownConverter):
            def convert_a(self, el, text, convert_as_inline):
                if include_links:
                    return super().convert_a(el, text, convert_as_inline)
                return text

        with sync_playwright() as p:
            with p.chromium.launch(headless=True) as browser:
                page = browser.new_page()

                def skip_loading_images(route):
                    if route.request.resource_type == "image":
                        return route.abort()
                    route.continue_()

                page.route("**/*", skip_loading_images)

                page.goto(url)

                # Some websites require a delay before the content is fully loaded
                # even after the browser has emitted "load" event.
                if self.timeout:
                    page.wait_for_timeout(self.timeout)

                content = page.content()

                if not content:
                    raise Exception("can't access URL")

                soup = BeautifulSoup(content, "html.parser")

                # Remove unwanted elements
                exclude_selector = ",".join(
                    self.exclude_tags + [f".{c}" for c in self.exclude_classes] + [f"#{i}" for i in self.exclude_ids]
                )
                if exclude_selector:
                    for s in soup.select(exclude_selector):
                        s.extract()

                text = OptionalLinksMarkdownConverter().convert_soup(soup)

                return TextArtifact(text)