import re
import sys
import subprocess
from datetime import datetime
from collections import deque

def parse_log_file(file_path, num_lines):
    pattern = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}) (\w+) (.+)"
    parsed_logs = deque(maxlen=num_lines)
    try:
        with open(file_path, "r") as file:
            for line in file:
                match = re.match(pattern, line)
                if match:
                    timestamp_str, log_level, message = match.groups()
                    timestamp = datetime.strptime(
                        timestamp_str[:-5], "%Y-%m-%dT%H:%M:%S"
                    )
                    # 새로운 형식으로 timestamp 변환
                    formatted_date = timestamp.strftime("%y년 %m월 %d일")
                    am_pm = "오전" if timestamp.hour < 12 else "오후"
                    hour = timestamp.hour if timestamp.hour <= 12 else timestamp.hour - 12
                    formatted_time = f"{am_pm} {hour}시 {timestamp.minute}분 {timestamp.second}초"
                    formatted_timestamp = f"{formatted_date} {formatted_time}"
                    #parse_log_file 함수 내에서:
                    #timestamp를 파싱한 후, 새로운 형식으로 변환하는 코드를 추가했습니다.
                    #strftime을 사용하여 날짜 부분을 "yy년 mm월 dd일" 형식으로 변환합니다.
                    #시간을 12시간 형식으로 변환하고, "오전/오후"를 추가했습니다.
                    #최종적으로 formatted_timestamp를 생성하여 딕셔너리에 저장합니다.
                    #create_html_content 함수는 변경할 필요가 없습니다. 이미 변환된 timestamp를 그대로 사용합니다.
                    #이렇게 수정하면 로그의 timestamp가 요청하신 "24년 9월 6일 오전 9시 6분 32초" 형식으로 표시될 것입니다.
                    parsed_logs.append(
                        {
                            "timestamp": formatted_timestamp,
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

# ... (나머지 코드는 변경 없음)