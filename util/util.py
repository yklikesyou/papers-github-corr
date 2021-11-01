def _clean_str(title: str):
    return title.strip().lower()

def match_title(key: str, query: str, exact: bool):
    if exact:  # 제목이 정확히 똑같은 논문이 있을 경우 return (단, 대소문자 구분 없음)
        return _clean_str(query) == _clean_str(key) 
    else:  # keyword 검색 등 query가 key 안에 있기만 해도 return
        return _clean_str(query) in _clean_str(key) 