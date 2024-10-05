from customClass import RequestBody, FileSystem, Reflection
from SessionHandler import SessionHandler
from GitRepoHandler import GitRepoHandler
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import helper
import os

load_dotenv()
app = FastAPI(
    title="TinyGen",
    summary="An AI service that can modify your GitHub code in seconds.",
    contact={
        "name": "Abhinav Gupta",
        "url": "https://www.abhinavgupta.info",
        "email": "a363gupt@uwaterloo.ca",
    }
)

OPENAI_KEY = os.getenv('OPENAI_KEY')

llm = ChatOpenAI(api_key=OPENAI_KEY, model="gpt-4o-mini")
llmResponder = llm.with_structured_output(FileSystem)
llmReflector = llm.with_structured_output(Reflection)

@app.post("/process")
def process_request(data: RequestBody):
    """
    This API processes your prompt, modifies the code, and returns a git diff.
    """
    dbSession = SessionHandler()
    repo = GitRepoHandler(data.repoUrl)
    repo.clone()
    fileContent = {} # dictionary that stores all files and its content from repo
    helper.getFiles(repo.dirName, fileContent)

    response: FileSystem = llmResponder.invoke(helper.promptGenerator["getResponse"](fileContent, data.prompt))
    while not helper.isValidFileNames(fileContent, response.files): # confirm that the llm outputs the right file names
        print("file names not valid")
        response = llmResponder.invoke(helper.promptGenerator["getResponse"](fileContent, data.prompt))
    reflection: Reflection = llmReflector.invoke(helper.promptGenerator["getReflection"](fileContent, response.files, data.prompt))
    helper.updateFileContent(fileContent, response.files)

    revisions = 1
    while reflection.isNeedModifications and revisions <= 3: # revise a maximum of 3 times to avoid infinite revision
        revisions += 1
        response = llmResponder.invoke(helper.promptGenerator["getRevision"](fileContent, reflection.modifications, data.prompt))
        while not helper.isValidFileNames(fileContent, response.files): # confirm that the llm outputs the right file names
            print("file names not valid reflection")
            response = llmResponder.invoke(helper.promptGenerator["getRevision"](fileContent, reflection.modifications, data.prompt))
        reflection = llmReflector.invoke(helper.promptGenerator["getReflection"](fileContent, response.files, data.prompt))
        helper.updateFileContent(fileContent, response.files)

    helper.modifyFiles(response.files)
    dbSession.addRequest(data.repoUrl, data.prompt, repo.getDiff())
    dbSession.disconnect()

    return {
        "diff": repo.getDiff()
    }

@app.get("/requests")
def process_request():
    """
    This API returns a list of all outputs generated for prompts in previous API requests.
    """
    dbSession = SessionHandler()
    requests = dbSession.getAllRequests()
    dbSession.disconnect()

    return {
        "requests": requests
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
