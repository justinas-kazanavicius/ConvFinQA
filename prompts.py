from langchain.prompts import PromptTemplate

# Prompt
reason_and_answer_prompt_template = PromptTemplate(
    template="""You are an investment analyst. You will be given: 
    <INSTRUCTIONS>
        You will be provided:
        1. a QUESTION asked by the user
        2. CONTEXT provided by an automated context retrieval system
        
        Your task is to use the CONTEXT to provide a relevant ANSWER to the QUESTION.

        Only answer what the user is asking and nothing else.
        
        Explain your reasoning in a step-by-step manner. Ensure your reasoning and conclusion are correct.

        Avoid simply stating the correct answer at the outset.

        If there is no relevant context provided, state that at the outset.

        At the end of your calculations, provide a section for the final answer submission (must be in-between <ANSWER> and </ANSWER> tags).
    </INSTRUCTIONS>
    <EXAMPLE>
        <INPUT>
            <QUESTION>What is the percentage change in the net cash from operating activities from 2008 to 2009?</QUESTION>
            <CONTEXT>
            In 2008, the net cash from operating activities was $200,000.
            In 2009, the net cash from operating activities was $258,620.
            </CONTEXT>
        </INPUT>
        <OUTPUT>
            <REASONING>
                To calculate the percentage change, we can use the formula:

                percentage_change = ((new_value - old_value) / old_value) * 100

                Substituting the given values:

                old_value = 200000
                new_value = 258620

                percentage_change = ((258620 - 200000) / 200000) * 100

                percentage_change = (58620 / 200000) * 100

                percentage_change = 0.2931 * 100

                percentage_change = 29.31%

                Therefore, the percentage change in the net cash from operating activities from 2008 to 2009 is 29.31%.
            </REASONING>
            <ANSWER>29.31%</ANSWER>
        </OUTPUT>
    </EXAMPLE>
    <INPUT>
        <QUESTION>{question}</QUESTION>
        <CONTEXT>
        {context}
        </CONTEXT>
    </INPUT>
    """,
    input_variables=["question", "context"],
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

        If answer is not provided, say "NO ANSWER"
    </INSTRUCTIONS>
    <INPUT>
        <QUESTION>{question}</QUESTION>\n
        <LONG ANSWER>{generation}</LONG ANSWER>\n
    </INPUT>
    """,
    input_variables=["question", "generation"],
)

filter_context_prompt_template = PromptTemplate(
    template="""
    <INSTRUCTIONS>
        You will be provided:
        1. QUESTION: question asked by the user
        2. DOCUMENTS: list of retrieved documents

        Your task is to:
         - pick the relevant DOCUMENTS that can be used to answer the question
         - discard irrelevant DOCUMENTS that provide no useful information to answer the question
         - trim the relevant DOCUMENTS to only include the relevant information needed to answer the question

        Only return the relevant information from the documents and the source douments, nothing else.
        Return in a YAML like format (see example).
        Do not try to produce the answer, only provide the relevant information that should be used to answer the question.
        
    </INSTRUCTIONS>
    <EXAMPLE>
        <INPUT>
            <QUESTION>What is the percentage change in the net cash from operating activities from 2008 to 2009?</QUESTION>
            <DOCS>
                <DOC ID="some-relevant-doc-1">
                The net cash from operating activities in 2008 was $10 million.
                </DOC>
                <DOC ID="some-relevant-doc-2">
                The net cash from operating activities increased by $2 million in 2009.
                </DOC>
                <DOC ID="some-irrelevant-doc-1">
                The company's net revenue from sales in 2009 was $50 million, compared to $45 million in 2008.
                </DOC>
            </DOCS>        
        </INPUT>
        <OUTPUT>
            The net cash from operating activities in 2008 was $10 million.
            The net cash from operating activities increased by $2 million in 2009.
            
            sources:
                - some-relevant-doc-1
                - some-relevant-doc-2
        </OUTPUT>
    </EXAMPLE>
    <INPUT>
        <QUESTION>{question}</QUESTION>\n
        <DOCS>
        {documents}
        </DOCS>
    </INPUT>
    """,
    input_variables=["question", "documents"],
)


generate_queries_prompt_template = PromptTemplate(
    template="""
    <INSTRUCTIONS>
        You will be provided with a QUESTION asked by the user.

        Your task is to generate a set of precise and relevant search queries that can be used to retrieve documents from a database to answer the QUESTION.

        Please ensure that the queries are comprehensive enough to cover all aspects of the QUESTION but also specific enough to filter out irrelevant information.

        Only return the search queries, and nothing else. Separate each query with a newline.
    </INSTRUCTIONS>
    <EXAMPLE>
         <INPUT>
            <QUESTION>What was the total revenue for the company in the last three quarters?</QUESTION>
        </INPUT>
        <OUTPUT>
            Total revenue last three quarters
            Revenue Q1 2024
            Revenue Q2 2024
            Revenue Q3 2024
            Revenue Q4 2023
            Sum of quarterly revenue figures
        </OUTPUT>
    </EXAMPLE>
    <INPUT>
        <QUESTION>{question}</QUESTION>\n
    </INPUT>
    """,
    input_variables=["question"],
)
