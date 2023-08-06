import re
from typing import Callable
import jupytext
from nbformat.notebooknode import NotebookNode
from .config import Config


def notebook_to_script(
    notebook: NotebookNode,
) -> str:
    """Converts a notebook into a python script serialized as a string.
    Args:
        notebook (NotebookNode): Notebook to convert into script.
    Returns:
        str: Python script representation as string.
    """
    return jupytext.writes(notebook, fmt="py:percent")


def cut_notebook(
    regex_pattern: str = "(grade)(.|[ \t]*)(up)(.|[ \t]*)(to)(.|[ \t]*)(here)",
) -> NotebookNode:
    """Cuts a notebook, this allows for partial grading. Written as a closure so it can be consumed as a functional option for notebooks.
    Args:
        regex_pattern (str): Regexp pattern to look for. Cells after match will be omitted.
    Returns:
        Callable[[NotebookNode], NotebookNode]: A function that cuts the notebook.
    """

    def inner(
        notebook: NotebookNode,
    ):
        """Cuts a notebook by excluding all cells after a pattern is matched.
        Args:
            notebook (NotebookNode): Notebook to filter.
        Returns:
            NotebookNode: The filtered notebook.
        """
        filtered_cells = []

        for cell in notebook["cells"]:
            filtered_cells.append(cell)

            if cell["cell_type"] == "code" and re.search(regex_pattern, cell["source"]):
                break

        notebook["cells"] = filtered_cells
        return notebook

    return inner


def keep_tagged_cells(
    tag: str = "graded",
) -> Callable[[NotebookNode], NotebookNode]:
    """Keeps tagged cells from a notebook. Written as a closure so it can be consumed as a functional option for notebooks.
    Args:
        tag (str): Tag to look for within cell's metadata. Defaults to "graded".
    Returns:
        Callable[[NotebookNode], NotebookNode]: A function that filters the notebook.
    """

    def inner(
        notebook: NotebookNode,
    ) -> NotebookNode:
        """Filters a notebook by including tagged cells.
        Args:
            notebook (NotebookNode): Notebook to filter.
        Returns:
            NotebookNode: The notebook with tagged cells.
        """
        filtered_cells = []

        for cell in notebook["cells"]:
            if not tag in cell["metadata"].get("tags"):
                continue
            filtered_cells.append(cell)

        notebook["cells"] = filtered_cells
        return notebook

    return inner


def omit_tagged_cells(
    tag: str = "omit",
) -> Callable[[NotebookNode], NotebookNode]:
    """Omits tagged cells from a notebook. Written as a closure so it can be consumed as a functional option for notebooks.
    Args:
        tag (str): Tag to look for within cell's metadata. Defaults to "omit".
    Returns:
        Callable[[NotebookNode], NotebookNode]: A function that filters the notebook.
    """

    def inner(
        notebook: NotebookNode,
    ) -> NotebookNode:
        """Filters a notebook by excluding tagged cells.
        Args:
            notebook (NotebookNode): Notebook to filter.
        Returns:
            NotebookNode: The notebook without omitted cells.
        """
        filtered_cells = []

        for cell in notebook["cells"]:
            if tag in cell["metadata"].get("tags"):
                continue
            filtered_cells.append(cell)

        notebook["cells"] = filtered_cells
        return notebook

    return inner


def get_named_cells(
    notebook: NotebookNode,
) -> dict:
    """Returns the named cells for cases when grading is done using cell's output.
    Args:
        notebook (NotebookNode): The notebook from the learner.
    Returns:
        dict: All named cells encoded as a dictionary.
    """
    named_cells = {}
    for cell in notebook["cells"]:
        metadata = cell["metadata"]
        if not "name" in metadata:
            continue
        named_cells.update({metadata.get("name"): cell})
    return named_cells


def tag_code_cells(
    notebook: NotebookNode,
    tag: str = "graded",
) -> NotebookNode:
    """Filters a notebook to exclude additional cells created by learners.
       Also used for partial grading if the tag has been provided.
    Args:
        notebook (NotebookNode): Notebook to filter.
        tag (str): The tag to include in the code cell's metadata. Defaults to "graded".
    Returns:
        NotebookNode: The filtered notebook.
    """
    filtered_cells = []

    for cell in notebook["cells"]:

        if cell["cell_type"] == "code":

            if not "tags" in cell["metadata"]:
                cell["metadata"]["tags"] = []

            tags = cell["metadata"]["tags"]

            if not tag in tags:
                tags.append(tag)
                cell["metadata"]["tags"] = tags

        filtered_cells.append(cell)

    notebook["cells"] = filtered_cells

    return notebook


def notebook_version(
    notebook: NotebookNode,
) -> str:
    """Returns dlai version of a notebook.

    Args:
        notebook (NotebookNode): A notebook.

    Returns:
        str: Version encoded as string.
    """
    return notebook.get("metadata").get("dlai_version")


def notebook_is_up_to_date(
    notebook: NotebookNode,
) -> bool:
    """Determines if a notebook is up-to-date with latest grader version.

    Args:
        notebook (NotebookNode): A notebook.

    Returns:
        bool: True if both versions match, False otherwise.
    """
    version = notebook_version(notebook)
    c = Config()
    if version != c.latest_version:
        return False
    return True
