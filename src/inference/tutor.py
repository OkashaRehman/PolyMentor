from src.inference.pipeline import PolyMentorPipeline
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TutorSession:
    """
    Interactive tutoring session.
    The tutor works through errors one at a time,
    giving progressive hints if the user asks.
    """

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
        print("🧠 PolyMentor — Interactive Tutor Mode")
        print("Type your code, then press Enter twice to submit.")
        print("Type 'hint' for the next hint, 'quit' to exit.")
        print("=" * 60 + "\n")

        hints_used = []
        current_hints = []
        hint_index = 0

        while True:
            print("📝 Paste your code (press Enter twice when done):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)

            code = "\n".join(lines)

            if code.lower() == "quit":
                print("👋 Session ended. Keep coding!")
                break

            result = self.pipeline.analyze(code, self.language, self.level)
            current_hints = result.hints
            hint_index = 0

            if not result.error_types:
                print("\n✅ No errors found! Code quality score:", result.quality_score)
                continue

            print(f"\n🔍 Detected: {', '.join(result.error_types)}")
            print(f"📚 Concept: {result.concept_taught}")
            print(f"💬 Explanation: {result.explanation}")
            print(
                f"\n💡 First hint: {current_hints[0] if current_hints else 'No hints available.'}"
            )
            print(f"📊 Code quality: {result.quality_score}/100\n")

            while True:
                action = (
                    input(
                        "Type 'hint' for next hint, 'new' for new code, 'quit' to exit: "
                    )
                    .strip()
                    .lower()
                )
                if action == "hint":
                    hint_index += 1
                    if hint_index < len(current_hints):
                        print(f"\n💡 {current_hints[hint_index]}\n")
                    else:
                        print(
                            "\n✅ No more hints. Try fixing the error and resubmit!\n"
                        )
                elif action == "new":
                    break
                elif action == "quit":
                    return


def run_tutor():
    pipeline = PolyMentorPipeline.from_pretrained("models_saved/best_mentor_model.pt")
    language = input("Language (python/javascript/java/cpp): ").strip() or "python"
    level = input("Level (beginner/intermediate/advanced): ").strip() or "beginner"
    session = TutorSession(pipeline, language, level)
    session.start()


if __name__ == "__main__":
    run_tutor()
