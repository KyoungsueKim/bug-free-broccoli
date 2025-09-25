"""아주대학교 공지사항 게시판에서 새 게시물을 탐지하는 로직."""

from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple
from urllib.parse import urljoin

import bs4
from bs4 import BeautifulSoup
import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://www.ajou.ac.kr/kr/ajou/notice.do"

# 크롤링을 건너뛸 키워드 Set
SKIP_KEYWORDS = {
    "예비군",
    # 필요시 여기에 더 많은 키워드를 추가할 수 있습니다
    # "동원훈련",
    # "민방위",
}


@dataclass(frozen=True)
class PostSummary:
    """게시판에서 추출한 게시글의 최소 정보"""

    number: int
    title: str
    url: str

    def contains_skip_keyword(self) -> bool:
        """게시글 제목에 필터링 키워드가 포함되어 있는지 여부"""

        return any(keyword in self.title for keyword in SKIP_KEYWORDS)


def _fetch_board() -> BeautifulSoup:
    """
    아주대학교 공지사항 게시판 HTML을 안전하게 가져온 뒤 BeautifulSoup 객체로 반환합니다.
    네트워크 오류가 발생할 경우 성공할 때까지 재시도합니다.
    """

    while True:
        try:
            response = requests.get(BASE_URL, verify=False)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as error:
            print(error)


def _clean_text(text: str) -> str:
    """게시판에서 수집한 문자열의 공백과 개행 문자를 정리합니다."""

    return " ".join(text.replace("\n", " ").replace("\t", " ").replace("\r", " ").split())


def _extract_post_number(tag: bs4.Tag) -> Optional[int]:
    """게시판의 번호 영역에서 정수 게시글 번호만 추출합니다."""

    cleaned = _clean_text(tag.text)
    digits = "".join(character for character in cleaned if character.isdigit())
    return int(digits) if digits else None


def _extract_post_title(tag: bs4.Tag) -> Tuple[str, Optional[str]]:
    """게시판의 제목 영역에서 제목과 상세 페이지 URL을 추출합니다."""

    link_tag = tag.find("a")
    if link_tag is None:
        return "", None

    title = _clean_text(link_tag.text)
    href = link_tag.get("href")
    return title, href


def _parse_posts(soup: BeautifulSoup) -> List[PostSummary]:
    """공지사항 목록 페이지에서 실제 게시글 정보만 추려냅니다."""

    number_tags = soup.find_all("td", {"class": "b-num-box"})
    title_tags = soup.find_all("div", {"class": "b-title-box"})

    posts: List[PostSummary] = []
    for number_tag, title_tag in zip(number_tags, title_tags):
        number = _extract_post_number(number_tag)
        if number is None:
            continue

        title, relative_url = _extract_post_title(title_tag)
        if not title or relative_url is None:
            continue

        posts.append(PostSummary(number=number, title=title, url=urljoin(BASE_URL, relative_url)))

    return posts


def _find_new_post(posts: Iterable[PostSummary], current_number: int) -> Tuple[Optional[PostSummary], List[PostSummary]]:
    """
    현재 번호보다 큰 게시글 중 필터링 키워드가 없는 최신 게시글을 찾습니다.
    함께 조회된 필터링 대상 게시글 목록도 반환하여 후속 처리에 활용합니다.
    """

    skipped_posts: List[PostSummary] = []

    for post in sorted(posts, key=lambda candidate: candidate.number, reverse=True):
        if post.number <= current_number:
            break

        if post.contains_skip_keyword():
            skipped_posts.append(post)
            continue

        return post, skipped_posts

    return None, skipped_posts


def refresh(current_number: int) -> Optional["Refresh"]:
    """현재 저장된 게시글 번호 이후의 새 게시글을 조회합니다."""

    soup = _fetch_board()
    posts = _parse_posts(soup)

    target_post, skipped_posts = _find_new_post(posts, current_number)

    for skipped in skipped_posts:
        print(
            f"게시글 번호 {skipped.number} - '{skipped.title}' 게시물은 필터링 키워드로 인해 건너뜁니다."
        )

    if target_post is not None:
        return Refresh(target_post.url, target_post.number)

    if skipped_posts:
        latest_skipped = skipped_posts[0]
        return Refresh(latest_skipped.url, latest_skipped.number, is_filtered=True)

    return None


class Refresh:
    """새로운 게시글 정보를 담는 단순 DTO."""

    def __init__(self, url: str, number: int, is_filtered: bool = False) -> None:
        self.url = url
        self.page_number = number
        self.is_filtered = is_filtered
        Refresh.page_number = number
