"""CLI entry point: python -m assistant "your question here" """
import sys
from .bot import ask


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m assistant \"your question\"")
        sys.exit(1)
    question = " ".join(sys.argv[1:])
    result = ask(question)
    print(result["answer"])
    if result["citations"]:
        print(f"Citations: {', '.join(result['citations'])}")
    else:
        print("Citations: (none)")


if __name__ == "__main__":
    main()
