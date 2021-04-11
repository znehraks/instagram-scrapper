from konlpy.tag import Okt
from collections import Counter


def get_tags(text, ntags=50):
    # konlpy의 Twitter객체
    spliter = Okt()

    # nouns 함수를 통해서 text에서 명사만 분리/추출
    nouns = spliter.nouns(text)

    # Counter 객체를 생성하고 참조변수 nouns 할당
    count = Counter(nouns)

    # most_common 메소드는 정수를 입력받아 객체 안의 명사 중 빈도수가
    # 큰 명사부터 순서대로 입력받은 정수 개수만큼 저장되어 있는 객체를
    # 반환하여 명사와 사용된 개수를 return_list에 저장함
    return_list = []
    for n, c in count.most_common(ntags):
        temp = {'tag': n, 'count': c}
        return_list.append(temp)
    return return_list


def main():
    # 분석할 파일
    text_file_name = "out.txt"

    # 최대 많은 빈도수 부터 20개 명사 추출
    noun_count = 20

    # count.txt 에 저장
    output_file_name = "count.txt"

    # 분석할 파일을 open
    open_text_file = open(text_file_name, 'r', -1, "utf-8")

    text = open_text_file.read()  # 파일을 읽습니다.

    tags = get_tags(text, noun_count)  # get_tags 함수 실행

    open_text_file.close()  # 파일 close

    # 결과로 쓰일 count.txt 열기
    open_output_file = open(output_file_name, 'w', -1, "utf-8")

    # 결과 저장
    for tag in tags:
        noun = tag['tag']
        count = tag['count']
        open_output_file.write('{} {}\n'.format(noun, count))
    open_output_file.close()


if __name__ == '__main__':
    main()
