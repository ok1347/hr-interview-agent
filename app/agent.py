#this is the agent for the HR recruiter
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from dotenv import load_dotenv

load_dotenv()


def agent_rh_respond(cv_text: str, offer_text: str, chat_history: list[str], user_input: str) -> str:
    #this is the prompt template for the HR agent, we can adapt it to the specific needs of the HR interview process and add more specific questions or instructions as needed.
    system_template = """
You are a professional and empathetic HR recruiter conducting a smart job interview.

Here is the candidate's resume:
{cv_text}

Here is the job offer:
{offer_text}

Here is the recent conversation history:
{chat_history}

Here is the candidate's latest message:
{user_input}

Your task:
- If it is a question, answer clearly, politely, and professionally.
- If it is a response, ask the next relevant HR interview question.
Always sound natural and human. Don't prefix your answer with "HR:" or "Assistant:".
    """

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template)
    ])

    llm = ChatOpenAI(model="gpt-4o", temperature=0.4)

    chain = prompt | llm

    result = chain.invoke({
        "cv_text": cv_text,
        "offer_text": offer_text,
        "chat_history": "\n".join(chat_history),
        "user_input": user_input
    })

    return result.content.strip()
