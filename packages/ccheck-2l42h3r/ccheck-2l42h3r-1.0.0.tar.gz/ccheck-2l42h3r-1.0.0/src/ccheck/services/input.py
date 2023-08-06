from typing import List


class InputService:
    def get_multiline_input(self) -> str:
        content: List[str] = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            content.append(line)

        return "\n".join(map(str, content))
