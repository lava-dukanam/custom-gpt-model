def consolidate_feedback(feedback_list: list[str]) -> str:
  """
  Consolidates a list of feedback strings into a single string.

  Args:
    feedback_list: A list of strings, where each string is a piece of feedback.

  Returns:
    A single string with all feedback items joined by newline characters.
  """
  return "\n".join(feedback_list)
