def make_prompt_for_summary_and_questions(transcribtion: str) -> str:
    prompt = f"""
    ```
    {transcribtion}
    ```
    This is a transcript of a cartoon that a child is watching. 
    Make a summary of this cartoon and come up with 3 questions about the plot to ask your child. 
    These questions should be in the same language as the transcript. The questions should encourage reflection.
    Your response format is json-schema.
    """
    return prompt