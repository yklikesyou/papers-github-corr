
import argparse
import pandas as pd

from paperswithcode_handler import PapersWithCodeDataServicer
from github_handler import GithubAPIServicer


def parse_args():
    parser = argparse.ArgumentParser(
        description='Paperswithcode와 Github의 환상적인 콜라보레이션')

    parser.add_argument('--paperswithcode_json_path', dest='json_path', type=str,
                        default="./links-between-papers-and-code.json",
                        help="paperswithcode에서 다운로드 받은 데이터의 경로를 입력해주세요.")
    parser.add_argument('--user_id', type=str, required=True,
                        help="Github에서 사용하는 User ID를 입력해주세요.")
    parser.add_argument('--github_token', dest='token', type=str, required=True,
                        help="Github에서 발급받은 OAuth token을 입력해주세요.")
    # parser.add_argument('--title', type=str, required=True,
    #                     help="검색할 논문의 제목을 입력해주세요.")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    paperswithcode_servicer = PapersWithCodeDataServicer(
        json_path=args.json_path)
    github_servicer = GithubAPIServicer(user_id=args.user_id, token=args.token)

    df = pd.DataFrame(columns=['Paper Titles', 'Stars',
                      'Watchers', 'Forks', 'Issues'])
    NUM_TOTAL = NUM_INFO = NUM_NO_INFO = 0

    # Get CVPR2020 titles
    csv_file = pd.read_csv(
        "cvpr2020.csv", encoding='utf-8-sig', index_col=None)
    titles_info = csv_file['paper_title']
    titles_info_list = titles_info.values.tolist()

    # Search papers with title
    for title in titles_info_list:
        NUM_TOTAL += 1
        print(NUM_TOTAL)
        query_title = title
        paper_items = paperswithcode_servicer.search_with_title(
            query_title, only_official=True)
        if len(paper_items) != 0:
            for paper_item in paper_items:
                try:
                    repo_url = paper_item['repo_url']
                    github_stars, github_watchers, github_forks, github_issues = github_servicer.get_github_star(
                        repo_url)
                    # Dataframe에 저장
                    df.loc[NUM_INFO] = [title, github_stars,
                                        github_watchers, github_forks, github_issues]
                    NUM_INFO += 1
                except RuntimeError as e:
                    print(e)
        else:
            NUM_NO_INFO += 1

    df.to_csv("CVPRpapers_github_metrics.csv", encoding='utf-8-sig')
    print(f'총 {NUM_TOTAL}개의 논문 = 지표 정보 있는 논문 수 {NUM_INFO}개 + 없는 논문 수{NUM_NO_INFO}개')
