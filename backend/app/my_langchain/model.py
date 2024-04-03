from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.runnables import RunnablePassthrough


class HomeAssist:
    def __init__(self):

        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

        summarize_questions_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """Given a chat history and the latest user question \
                                which might reference context in the chat history, formulate a standalone question \
                                which can be understood without the chat history. Do NOT answer the question, \
                                just reformulate it if needed and otherwise return it as is."""),
                # This MessagesPlaceholder() will take multiple messages in the chat history
                # Each message is a `langchain_core.messages` object
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )

        # The output of summarize_questions_chain is a string
        summarize_questions_chain = summarize_questions_prompt | llm | StrOutputParser()

        system_prompt_template = """You are an assistant for question-answering tasks. \
        Use the following pieces of retrieved context to answer the question. \
        If you're using the provided context as your source of information, please quote the source at the end of your answer. \
        If you don't know the answer, just say that you don't know and ask the user (human) to contact the authorities for more information.

        {context}"""

        main_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt_template),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )

        def summarize_questions(input: dict):
            if input.get("chat_history"):
                # if the chat_history in the input of the chain is not empty (codes below)
                return summarize_questions_chain
            else:
                return input["question"]

        embedder = OpenAIEmbeddings(model="text-embedding-ada-002")

        INDEX_NAME = "homeassist"
        retriever = PineconeVectorStore(index_name=INDEX_NAME,
                                        embedding=embedder).as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )

        self.rag_chain = (
            # This RunnablePassthrough will make sure that besides the output of it,
            # the k:v pairs in the original inputs are passed through too.
            RunnablePassthrough.assign(
                # This line means -> make a k:v = context : (summarize_questions | retriever)
                context=summarize_questions | retriever
            )
            | main_prompt
            | llm
        )

    def ask_ai(self, prompt):
        ai_msg = self.rag_chain.invoke(prompt)
        # ai_msg = AIMessage(content="this is a test message from the backend.")
        return ai_msg
