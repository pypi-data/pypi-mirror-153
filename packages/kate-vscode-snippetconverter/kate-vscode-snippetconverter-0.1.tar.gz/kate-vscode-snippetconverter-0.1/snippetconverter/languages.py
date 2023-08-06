"""helper methods to define languages of snippets"""
from enum import Enum
from itertools import count

# Based on visual studio code identifiers https://code.visualstudio.com/docs/languages/identifiers
LANGUAGES = Enum(
    "LANGUAGES",
    zip(
        [
            "ABAP",
            "BAT",
            "BIBTEX",
            "CLOJURE",
            "COFFEESCRIPT",
            "C",
            "CMAKE",
            "CPP",
            "CSHARP",
            "CSS",
            "DIFF",
            "DOCKERFILE",
            "FSHARP",
            "GITCOMMIT",
            "GITREBASE",
            "GO",
            "GROOVY",
            "HANDLEBARS",
            "HTML",
            "INI",
            "JAVA",
            "JAVASCRIPT",
            "JAVASCRIPTREACT",
            "JSON",
            "JSONC",
            "LATEX",
            "LESS",
            "LUA",
            "MAKEFILE",
            "MARKDOWN",
            "OBJECTIVEC",
            "OBJECTIVECPP",
            "PERL",
            "PHP",
            "POWERSHELL",
            "JADE",
            "PYTHON",
            "R",
            "RAZOR",
            "RUBY",
            "RUST",
            "SCSS",
            "SHADERLAB",
            "SHELLSCRIPT",
            "SQL",
            "SWIFT",
            "TYPESCRIPT",
            "TYPESCRIPTREACT",
            "TEX",
            "VB",
            "XML",
            "XSL",
            "YAML",
        ],
        count(),
    ),
)


def induce_language_from_file_name(filename):
    """identify languaged of snippet file based on filename"""
    # pylint: disable=R0911
    # pylint: disable=R0912
    if "C++" in filename or "c++" in filename or "cpp" in filename or "Cpp" in filename:
        return LANGUAGES.CPP
    if "Python" in filename or "python" in filename:
        return LANGUAGES.PYTHON
    if "Bibtex" in filename:
        return LANGUAGES.BIBTEX
    if "CMake" in filename:
        return LANGUAGES.CMAKE
    if "Makefile" in filename:
        return LANGUAGES.MAKEFILE
    if "Markdown" in filename:
        return LANGUAGES.MARKDOWN
    if "Latex" in filename or "LaTeX" in filename:
        return LANGUAGES.TEX
    if "Javascript" in filename or "javascript" in filename:
        return LANGUAGES.JAVASCRIPT
    if "JSON.xml" in filename:
        return LANGUAGES.JSON
    if "html" in filename:
        return LANGUAGES.HTML
    if "Powershell" in filename:
        return LANGUAGES.POWERSHELL
    if "Windows-batch" in filename:
        return LANGUAGES.BAT
    if "C snippets" in filename:
        return LANGUAGES.C
    if "Bash" in filename:
        return LANGUAGES.SHELLSCRIPT
    if "SQL" in filename:
        return LANGUAGES.SQL
    raise Exception("Could not induce language from filename {}".format(filename))


def get_language_identifier_for_vscode(language):
    """get language identiger for vscode based on language"""
    languageidentifier = dict(
        {
            "ABAP": "abap",
            "BAT": "bat",
            "BIBTEX": "bibtex",
            "CLOJURE": "clojure",
            "COFFEESCRIPT": "coffeescript",
            "C": "c",
            "CPP": "cpp",
            "CSHARP": "csharp",
            "CSS": "css",
            "CMAKE": "cmake",
            "DIFF": "diff",
            "DOCKERFILE": "dockerfile",
            "FSHARP": "fsharp",
            "GITCOMMIT": "git-commit",
            "GITREBASE": "git-rebase",
            "GO": "go",
            "GROOVY": "groovy",
            "HANDLEBARS": "handlebars",
            "HTML": "html",
            "INI": "ini",
            "JAVA": "java",
            "JAVASCRIPT": "javascript",
            "JAVASCRIPTREACT": "javascriptreact",
            "JSON": "json",
            "JSONC": "jsonc",
            "LATEX": "latex",
            "LESS": "less",
            "LUA": "lua",
            "MAKEFILE": "makefile",
            "MARKDOWN": "markdown",
            "OBJECTIVEC": "objective-c",
            "OBJECTIVECPP": "objective-cpp",
            "PERL": "perl",
            "PHP": "php",
            "POWERSHELL": "powershell",
            "PYTHON": "python",
            "JADE": "jade",
            "R": "r",
            "RAZOR": "razor",
            "RUBY": "ruby",
            "RUST": "rust",
            "SCSS": "scss",
            "SHADERLAB": "shaderlab",
            "SHELLSCRIPT": "shellscript",
            "SQL": "sql",
            "SWIFT": "swift",
            "TYPESCRIPT": "typescript",
            "TYPESCRIPTREACT": "typescriptreact",
            "TEX": "tex",
            "VB": "vb",
            "XML": "xml",
            "XSL": "xsl",
            "YAML": "yaml",
        }
    )
    try:
        return languageidentifier[language.name]
    except ValueError:
        print("No known VSCode language identifier for language {}".format(language))
        raise ValueError
