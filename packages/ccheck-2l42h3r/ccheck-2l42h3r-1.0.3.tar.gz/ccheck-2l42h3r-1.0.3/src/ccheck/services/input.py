"""InputService class module"""

from typing import List


class InputService:
    """InputService class"""

    @staticmethod
    def get_multiline_input() -> str:
        """Returns read multi-line stdin input"""
        content: List[str] = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            content.append(line)

        return "\n".join(map(str, content))
