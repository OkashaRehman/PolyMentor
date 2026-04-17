from tree_sitter import Language, Parser
from pathlib import Path
from src.utils.logger import get_logger

logger = get_logger(__name__)

GRAMMAR_DIR = Path("vendor")
LIB_PATH = Path("build/languages.so")


def build_language_library():
    """Compile Tree-sitter grammars into a shared library."""
    LIB_PATH.parent.mkdir(parents=True, exist_ok=True)
    Language.build_library(
        str(LIB_PATH),
        [
            str(GRAMMAR_DIR / "tree-sitter-python"),
            str(GRAMMAR_DIR / "tree-sitter-javascript"),
            str(GRAMMAR_DIR / "tree-sitter-java"),
            str(GRAMMAR_DIR / "tree-sitter-cpp"),
        ],
    )
    logger.info(f"Built language library at {LIB_PATH}")


LANGUAGE_MAP = {
    "python": "python",
    "javascript": "javascript",
    "java": "java",
    "cpp": "cpp",
}


class ASTParser:
    """Parses source code into an Abstract Syntax Tree using Tree-sitter."""

    def __init__(self):
        if not LIB_PATH.exists():
            build_language_library()
        self.parsers = {}
        for lang_name, ts_name in LANGUAGE_MAP.items():
            lang = Language(str(LIB_PATH), ts_name)
            parser = Parser()
            parser.set_language(lang)
            self.parsers[lang_name] = parser

    def parse(self, code: str, language: str) -> dict:
        """Parse code and return a dict representation of the AST."""
        if language not in self.parsers:
            raise ValueError(f"Unsupported language: {language}")

        parser = self.parsers[language]
        tree = parser.parse(bytes(code, "utf8"))
        return self._node_to_dict(tree.root_node)

    def _node_to_dict(self, node, depth: int = 0) -> dict:
        return {
            "type": node.type,
            "start_point": node.start_point,
            "end_point": node.end_point,
            "depth": depth,
            "children": [self._node_to_dict(c, depth + 1) for c in node.children],
        }

    def get_node_types(self, code: str, language: str) -> list:
        """Return a flat list of all AST node types for feature extraction."""
        ast = self.parse(code, language)
        return self._flatten_types(ast)

    def _flatten_types(self, node: dict) -> list:
        types = [node["type"]]
        for child in node.get("children", []):
            types.extend(self._flatten_types(child))
        return types
