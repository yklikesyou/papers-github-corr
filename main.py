
import argparse

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
    parser.add_argument('--title', type=str, required=True,
                        help="검색할 논문의 제목을 입력해주세요.")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    paperswithcode_servicer = PapersWithCodeDataServicer(
        json_path=args.json_path)
    github_servicer = GithubAPIServicer(user_id=args.user_id, token=args.token)

    # Search papers with title
    query_title = args.title
    paper_items = paperswithcode_servicer.search_with_title(
        query_title, only_official=True)
    print(f"{query_title}에 해당하는 github repo들을 확인해볼까요?")
    for paper_item in paper_items:
        try:
            repo_url = paper_item['repo_url']
            github_stars = github_servicer.get_github_star(repo_url)
            print(f"{repo_url} 에 해당하는 github star는 {github_stars} 개입니다!")
        except RuntimeError as e:
            print(e)
