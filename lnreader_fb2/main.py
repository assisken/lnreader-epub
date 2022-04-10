import json
from collections import defaultdict
from typing import Dict, List

from FB2 import FictionBook2, TitleInfo
from selenium import webdriver

from lnreader_fb2.xml_processor import XmlProcessor

from .types import Backup, Download


def main():
    # path = input("Enter /fullpath/to/lnreader_backup_1234-56-78.json: ")
    path = "/home/aken/Downloads/lnreader_backup_2022-04-10.json"

    with open(path, "r") as file:
        data = json.load(file)

    print("Parsing your backup...")
    backup = Backup.parse_obj(data)

    chapter_by_id = {chapter.chapterId: chapter for chapter in backup.chapters}
    novel_by_id = {novel.novelId: novel for novel in backup.novels}

    downloaded_by_chapter_by_novel_id: Dict[
        int, Dict[int, List[Download]]
    ] = defaultdict(lambda: defaultdict(list))
    for download in backup.downloads:
        chapter = chapter_by_id[download.downloadChapterId]

        downloaded_by_chapter_by_novel_id[chapter.novelId][chapter.chapterId].append(
            download
        )

    browser = webdriver.Chrome()

    for novel_id, chapter in downloaded_by_chapter_by_novel_id.items():
        novel = novel_by_id[novel_id]

        print(f"Processing: {novel.novelName}...")

        book = FictionBook2()
        browser.get(novel.novelCover)
        cover = browser.find_element_by_tag_name("img").screenshot_as_png

        book.titleInfo = TitleInfo(
            title=novel.novelName,
            annotation=novel.novelSummary,
            coverPageImages=[cover],
        )
        book.chapters = []

        for chapter_id, downloads in chapter.items():
            chapter = chapter_by_id[chapter_id]

            for download in downloads:
                processor = XmlProcessor(download.chapterText)
                book.chapters.append((chapter.chapterName, list(processor)))

        file.close()
        browser.close()

        book.write(f"out/{novel.novelName}.fb2")
        print('Done! Take your books at "out" folder')
