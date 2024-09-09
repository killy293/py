import re
import sys
import subprocess
#subprocess 모듈을 임포트합니다. 이 모듈은 외부 프로그램을 실행하는 데 사용됩니다.
from datetime import datetime
from collections import deque


def parse_log_file(file_path, num_lines):
#이 함수는 로그 파일을 파싱하는 역할을 합니다.
#정규표현식 패턴을 사용하여 로그 파일의 각 줄을 파싱합니다.
#deque를 사용하여 지정된 라인 수(num_lines)만큼만 로그를 저장합니다.
#파일을 열어 각 줄을 읽으며, 패턴과 일치하는 경우 타임스탬프, 로그 레벨, 메시지를 추출합니다.
#타임스탬프는 datetime 객체로 변환됩니다.
#파싱된 로그 정보를 딕셔너리 형태로 deque에 저장합니다.
#파일 관련 예외(파일 없음, 권한 오류 등)를 처리합니다.
    # 2024-08-05T23:27:41+0900
    # T 문자로 split 하기 ->
    #  2024-08-05 -> - 문자로 split하면 연월일로 분리
    #  23:27:41+0900
    # \d{4}
    pattern = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}) (\w+) (.+)"
    parsed_logs = deque(maxlen=num_lines)
    try:
        with open(file_path, "r") as file:
            for line in file:
                match = re.match(pattern, line)
                if match:
                    timestamp_str, log_level, message = match.groups()
                    # 타임존 정보를 제거하고 파싱 (Python 3.6 이하 버전 호환성을 위해)
                    # "2024-08-05T23:27:41+0900" 형식의 내용에서 뒤 5자리 +0900 제거
                    #문자열을 datetime 객체로 변환하는 Python의 datetime 모듈 함수입니다.
                    #이 함수는 두 개의 인자를 받습니다: 1=변환하려는 날짜/시간 문자열, 2=해당 문자열의 형식을 지정하는 포맷 문자열
                    timestamp = datetime.strptime(
                        timestamp_str[:-5], "%Y-%m-%dT%H:%M:%S"
                    )
                    parsed_logs.append(
                        {
                            "timestamp": timestamp,
                            "log_level": log_level,
                            "message": message.strip(),
                        }
                    )
    except FileNotFoundError:
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
        sys.exit(1)
    except PermissionError:
        print(f"오류: '{file_path}' 파일을 읽을 권한이 없습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        sys.exit(1)

    return list(parsed_logs)


def create_html_content(parsed_logs):
#이 함수는 파싱된 로그 데이터를 HTML 형식으로 변환합니다.
#HTML 문서의 기본 구조를 문자열로 정의합니다.
#CSS 스타일을 포함하여 테이블 형태로 로그를 표시합니다.
#파싱된 각 로그 항목을 HTML 테이블의 행으로 추가합니다.
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>로그 파서 결과</title>
        <style>
            body { font-family: Arial, sans-serif; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
        <h1>파싱된 로그</h1>
        <table>
            <tr>
                <th>시간</th>
                <th>로그 레벨</th>
                <th>메시지</th>
            </tr>
    """

    for log in parsed_logs:
        html_content += f"""
            <tr>
                <td>{log['timestamp']}</td>
                <td>{log['log_level']}</td>
                <td>{log['message']}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    return html_content


def open_html_file(output_html_path):
    try:
        subprocess.run(['xdg-open', output_html_path], check=True)
        print(f"HTML 파일을 성공적으로 열었습니다: {output_html_path}")
    except subprocess.CalledProcessError as e:
        print(f"{output_html_path} 파일을 여는 중 오류가 발생했습니다: {e}")
    except FileNotFoundError:
        print("xdg-open 명령을 찾을 수 없습니다. 시스템에 설치되어 있는지 확인하세요.")
#open_html_file 함수를 정의합니다. 이 함수는 HTML 파일의 경로를 인자로 받습니다.
#subprocess.run() 함수를 사용하여 xdg-open 명령을 실행합니다. 첫 번째 인자는 실행할 명령어와 그 인자들의 리스트입니다.
#check=True 옵션을 사용하여 명령 실행 중 오류가 발생하면 예외를 발생시킵니다.
#예외 처리를 통해 오류 상황(명령 실행 실패, xdg-open 명령이 없는 경우 등)을 관리합니다.
#사용 예시에서는 html_file_path 변수에 열고자 하는 HTML 파일의 경로를 지정하고, open_html_file 함수를 호출합니다.
#이 코드를 실행하면, 지정된 HTML 파일이 시스템의 기본 웹 브라우저에서 열립니다.
#주의사항: 이 코드는 xdg-open 명령이 시스템에 설치되어 있어야 작동합니다. 대부분의 현대 리눅스 배포판에는 기본적으로 설치되어 있습니다.
#파일 경로는 절대 경로를 사용하는 것이 좋습니다. 상대 경로를 사용할 경우, Python 스크립트가 실행되는 현재 작업 디렉토리를 기준으로 합니다.
#보안상의 이유로, 사용자 입력을 직접 subprocess.run()에 전달할 때는 주의해야 합니다. 필요한 경우 입력을 검증하거나 이스케이프 처리를 해야 합니다.


def main():
#프로그램의 주 실행 흐름을 관리합니다.
#명령줄 인자를 확인하고 처리합니다 (로그 파일 경로, 읽을 라인 수, 출력 HTML 파일 경로).
#parse_log_file() 함수를 호출하여 로그를 파싱합니다.
#create_html_content() 함수를 호출하여 HTML 내용을 생성합니다.
#생성된 HTML 내용을 파일로 저장합니다.
#파일 저장 관련 예외를 처리합니다.
    if len(sys.argv) != 4:
        print(
            "사용법: python log2html.py <로그_파일_경로> <읽을_라인_수> <출력_HTML_파일_경로>"
        )
        sys.exit(1)

    log_file_path = sys.argv[1]
    output_html_path = sys.argv[3]

    try:
        num_lines = int(sys.argv[2])
        if num_lines <= 0:
            raise ValueError
    except ValueError:
        print("오류: 라인 수는 양의 정수여야 합니다.")
        sys.exit(1)

    parsed_logs = parse_log_file(log_file_path, num_lines)

    html_content = create_html_content(parsed_logs)

    try:
        with open(output_html_path, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)
        print(f"HTML 파일이 성공적으로 생성되었습니다: {output_html_path}")
        open_html_file(output_html_path)
        # HTML 파일을 자동으로 엽니다.
    except PermissionError:
        print(f"오류: '{output_html_path}'에 쓸 권한이 없습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"HTML 파일 생성 중 오류 발생: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
#블록:
#스크립트가 직접 실행될 때 main() 함수를 호출합니다.

#위 코드는 로그 파일을 파싱하고, 파싱된 데이터를 HTML 형식으로 변환하여 저장하는 기능을 수행합니다.
#명령줄 인터페이스를 통해 사용자가 로그 파일 경로, 읽을 라인 수, 출력 HTML 파일 경로를 지정할 수 있게 합니다.