from types import ModuleType
from typing import Any, Callable, List, Optional, Union
from .grading import test_case, LearnerSubmission

grading_function = Callable[[Any], List[test_case]]
learner_submission = Union[ModuleType, LearnerSubmission]
grading_wrapper = Callable[[learner_submission, Optional[ModuleType]], grading_function]
