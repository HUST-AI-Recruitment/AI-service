import re
def extract_numbers(content: str) -> list[int]:
    numbers = re.findall(r'\d+', content)
    return [int(num) for num in numbers]

def AI_response_handler(content: str) -> int:
    numbers = extract_numbers(content)
    possible_scores = [num for num in numbers if num >= 0 and num <= 100]
    if len(possible_scores) == 0:
        raise ValueError("No score found")
    return sum(possible_scores) // len(possible_scores)

if __name__ == '__main__':
    s = input()
    print(extract_numbers(s))