"""
You may download paperswithcode metadata from
https://github.com/paperswithcode/paperswithcode-data
"""
import json
import gzip
from util import match_title


MAX_ITEM_NUMBER = 100


class PapersWithCodeDataServicer:
    def __init__(self, json_path="./links-between-papers-and-code.json"):
        self.json_data = self._load_json(json_path)

    @staticmethod
    def _load_json(json_path):

        with open(json_path, 'r', encoding='utf-8-sig') as json_file:
            json_data = json.load(json_file)

        return json_data

    @staticmethod
    def _only_official_github(items):

        # temp_list = []
        # for item in items:
        #     if item['is_official']:
        #         temp_list.append(item)

        # return temp_list

        return [item for item in items if item['is_official']]

    def print_paper_list(self, max_item_number=MAX_ITEM_NUMBER):
        paper_list = [paper_item['paper_title']
                      for paper_item in self.json_data[:max_item_number]]

        return paper_list

    def search_with_title(self, title: str, exact=True, only_official=False):
        """title이 실제 Paperswithcode json 파일 내에 있는 지 확인합니다.

        Args:
            title (str): 논문 제목
            exact (bool, optional): string이 정확히 똑같아야 검색 결과로 인정할 지 여부(대소문자 구분 없음). Defaults to True.
            only_official (bool, optional): github official repo에 해당하는 것만 추출. Defaults to False.

        Returns:
            list[dict]: 결과 item(dict)을 담은 list
        """
        items = [paper_item for paper_item in self.json_data
                 if match_title(paper_item['paper_title'], title, exact=exact)]

        if len(items) != 0:
            if only_official:
                official_item = self._only_official_github(items)
                if len(official_item) == 1:
                    return official_item
                else:  # len(official_item) == 0 or len(official_item) > 1
                    return []
            else:
                return items
        else:  # len(items) == 0, which means NotFound!
            return []
