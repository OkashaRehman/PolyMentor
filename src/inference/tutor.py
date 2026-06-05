from src.inference.pipeline import PolyMentorPipeline
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TutorSession:
    """Interactive Groq-powered coding tutor session."""

    def __init__(
        self,
        pipeline: PolyMentorPipeline,
        language: str = "python",
        level: str = "beginner",
    ):
        self.pipeline = pipeline
        self.language = language
        self.level = level

    def start(self):
        print("\n" + "=" * 60)
        print("PolyMentor - Groq Coding Tutor")
        print("Ask a coding question, paste code, or type 'quit' to exit.")
        print("For code review, paste code after your question and press Enter twice.")
        print("=" * 60 + "\n")

        while True:
            question = input("Question: ").strip()
            if question.lower() in {"quit", "exit"}:
                print("Session ended. Keep building.")
                break

            print("Optional code, press Enter on an empty line to submit:")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)

            result = self.pipeline.chat(
                message=question or "Review this code and teach me what to improve.",
                code="\n".join(lines),
                language=self.language,
                level=self.level,
            )

            print("\n" + "-" * 60)
            print(result.answer)
            print("-" * 60)
            print(f"Model: {result.model} | Time: {result.elapsed_ms:.0f} ms\n")


def run_tutor():
    pipeline = PolyMentorPipeline.from_groq()
    language = input("Language (python/javascript/typescript/java/cpp/go/rust): ").strip() or "python"
    level = input("Level (beginner/intermediate/advanced): ").strip() or "beginner"
    session = TutorSession(pipeline, language, level)
    session.start()


if __name__ == "__main__":
    run_tutor()
