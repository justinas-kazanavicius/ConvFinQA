from langchain.prompts import PromptTemplate

# Prompt
reason_and_answer_prompt_template = PromptTemplate(
    template="""You are an investment analyst. You will be given: 
    <INSTRUCTIONS>
        You will be provided:
        1. a QUESTION asked by the user
        2. DOCUMENTS provided by an automated context retrieval system
        
        Your task is to use the context to provide a relevant ANSWER to the QUESTION

        Only answer what the user is asking and nothing else
        
        Explain your reasoning in a step-by-step manner. Ensure your reasoning and conclusion are correct. 

        Avoid simply stating the correct answer at the outset.

        If there is no relevant context provided, state that at the outset.

        At the end of your calculations provide a section for the final answer submission (must be in-between <ANSWER> and </ANSWER> tags).
    </INSTRUCTIONS>
    <EXAMPLE>
        <INPUT>
            <QUESTION>What is the percentage change in the net cash from operating activities from 2008 to 2009?</QUESTION>
            <DOCUMENTS>
            ...
            </DOCUMENTS>
        </INPUT>
        <OUTPUT>
            <ANSWER>29.31%</ANSWER>
        </OUTPUT>
    </EXAMPLE>
    <INPUT>
        <QUESTION>{question}</QUESTION>\n
        <DOCUMENTS>
        \n\n {documents}
        </DOCUMENTS>\n\n
        <QUESTION>{question}</QUESTION>\n
    </INPUT>
    """,
    input_variables=["question", "documents"],
)

# Prompt
eval_prompt_template = PromptTemplate(
    template="""
    <INSTRUCTIONS>
        You are an evaluator for an algorithm that answers investment analyst questions.

        You will be provided:
        1. QUESTION: question asked by the user
        2. ACTUAL_ANSWER: answer generated by the algorithm
        3. EXPECTED_ANSWER: expected answer

        Your task is to evaluate the algorithm's provided answer based on how well it matches the expected answer.
        If needed, use the question to to inform your evaluation.
        
        Only provide a number between 0 and 1 for your evaluation and nothing else. DO NOT provide explanations.

        If the actual answer matches the expected answer exactly, provide 1.
        If the actual answer is close to the expected answer, provide a number between 0 and 1 based on how close it is.
        For numerical answers, you should use relative difference: 1 - ((abs(a - b) / max(abs(a), abs(b))) ** 2)
        If the actual answer is not close to the expected answer, provide 0.

        
    </INSTRUCTIONS>
    <EXAMPLE>
        <INPUT>
            <QUESTION>What is the percentage change in the net cash from operating activities from 2008 to 2009?</QUESTION>
            <ACTUAL_ANSWER>29.31</ACTUAL_ANSWER>
            <EXPECTED_ANSWER>25.42%</EXPECTED_ANSWER>
        </INPUT>
        <OUTPUT>
            0.87
        </OUTPUT>
    </EXAMPLE>
    <INPUT>
        <QUESTION>{question}</QUESTION>\n
        <ACTUAL_ANSWER>{actual_answer}</ACTUAL_ANSWER>\n
        <EXPECTED_ANSWER>{expected_answer}</EXPECTED_ANSWER>\n
    </INPUT>
    """,
    input_variables=["question", "actual_answer", "expected_answer"],
)

extract_anwer_prompt_template = PromptTemplate(
    template="""
    <INSTRUCTIONS>
        You will be provided:
        1. QUESTION: question asked by the user
        2. LONG ANSWER: reasoning steps, followed by a final answer

        Your task is to extract the SHORT ANSWER from the LONG ANSWER

        The short answer should be as concise as possible, while still answering the question.

        Only return the SHORT ANSWER and nothing else.
    </INSTRUCTIONS>
    <EXAMPLE>
        <INPUT>    
            <QUESTION>What is the percentage change in the net cash from operating activities from 2008 to 2009?</QUESTION>
            <LONG ANSWER>
            ...Some calculations...

            29.31% is the percentage change in the net cash from operating activities from 2008 to 2009.
            </LONG ANSWER>
        </INPUT>
        <OUTPUT>
            29.31%
        </OUTPUT>
    </EXAMPLE>
    <INPUT>
        <QUESTION>{question}</QUESTION>\n
        <LONG ANSWER>{generation}</LONG ANSWER>\n
    </INPUT>
    """,
    input_variables=["question", "generation"],
)
