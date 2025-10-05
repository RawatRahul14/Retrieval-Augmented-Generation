# === Python Modules ===
import setuptools

# === Reading the README.md for Long Description ===
with open(
    "README.md",
    "r",
    encoding = "utf-8"
) as f:
    long_description = f.read()

# === Package Metadata Variables ===
__version__ = "0.0.0"
REPO_NAME = "Retrieval-Augmented-Generation"
AUTHOR_USER_NAME = "RawatRahul14"
SRC_REPO = "rag_pipeline"
AUTHOR_EMAIL = "rahulrawat272chd@gmail.com"

# === Setup Function for Packaging ===
setuptools.setup(
    ## === Basic Details ===
    name = SRC_REPO,
    version = __version__,
    author = AUTHOR_USER_NAME,
    author_email = AUTHOR_EMAIL,

    ## === Description Fields ===
    description = "A modular RAG pipeline for intelligent document querying using LLMs, embeddings, and vector databases.",
    long_description = long_description,
    long_description_content = "text/markdown",

    ## === Project URLs ===
    url = f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls = {
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },

    ## === Package Directory and Discovery ===
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where = "src")
)