from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from typing import TypedDict, Annotated
from pydantic import BaseModel, Field
import logging
import tempfile
from pathlib import Path
from encoder import encode


logging.basicConfig(level=logging.DEBUG)



def main():
    llm = AzureChatOpenAI(
        azure_deployment="gpt-4o",
        api_version="2025-01-01-preview",
        temperature=0
    )

    messages = [
        (
            "system",
            "You are a helpful translator. Translate the user sentence to German.",
        ),
        ("human", "I love programming."),
    ]

    response = llm.invoke(messages)
    print(response.content)

    encode(Path("/Users/bonyadnouri/Downloads/samplepptx.pptx"),Path("/Users/bonyadnouri/Documents/ContentExtractor/test_output/ppt_to_img.jpg"))


if __name__ == "__main__":
    main()
