import os
import re

def extract_syscalls_and_timestamps(file_path, output_file, batch_size=10000):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    pattern = re.compile(r'(\d+)\s+\S+\s+\d+\s+[<>]\s+\w+\s+(\w+)')
    extracted_data = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                match = pattern.search(line)
                if match:
                    timestamp = match.group(1)
                    syscall = match.group(2)
                    extracted_data.append(f'{timestamp}\t{syscall}')

                # 배치 크기만큼 데이터가 모이면 파일에 기록
                if len(extracted_data) >= batch_size:
                    with open(output_file, 'a') as outfile:
                        outfile.write('\n'.join(extracted_data) + '\n')
                    extracted_data.clear()  # 리스트 초기화

        # 남아 있는 데이터 기록
        if extracted_data:
            with open(output_file, 'a') as outfile:
                outfile.write('\n'.join(extracted_data) + '\n')

    except Exception as e:
        print(f"Error reading or writing file: {e}")

# 사용 예시
input_file = '/home/joon/SEMI/Research/Dataset/SocialNetwork-training-data/collection-1/node1/sysdig-socialnetwork-events_000.txt'
output_file = '/home/joon/SEMI/Research/Dataset/SocialNetwork-training-data/collection-1/node1/sysdig-socialnetwork-events_000_extracted_syscalls.txt'
extract_syscalls_and_timestamps(input_file, output_file)
