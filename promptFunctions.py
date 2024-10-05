from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

def getResponse(files, userPrompt):
    strFiles = "\n".join([f"File Name: {filename}\nContent: \n{content}" for filename, content in files.items()])

    promptTemplate = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"""
                Objective: 
                Determine which files provided need changing to satisfy the user's request for modifications.
                The user has provided the file names, each associated with its content, followed by the actual user request.

                Output: 
                Return the response by extracting every file name and generating the new code associated with that file below it.
                Return this only for every file you change. Ignore files and their content for ones that do not need any change.

                Notes: 
                Do not add comments to mention what has changed.
                If a comment is being added, phrase it in a way that remains consistent with other comments in the file's content."""
            ),
            (
                "user",
                """
                {files}
                
                User Request: {userPrompt}
                """
            )
        ]
    )

    return promptTemplate.format_messages(files=strFiles, userPrompt=userPrompt)

def getReflection(originalFiles, modifiedFiles, userPrompt):
    strOriginalFiles = "\n".join([f"File Name: {filename}\nContent: \n{content}" for filename, content in originalFiles.items()])
    strModifiedFiles = ""
    for file in modifiedFiles:
        strModifiedFiles += f"File Name: {file.name}\nContent: \n{file.content}\n"

    promptTemplate = PromptTemplate.from_template(
        """
        Based on the following prompt: "{userPrompt}", does the modified content of the files improve upon the original?
        Is the modified content functional, readable, comprehensive, and logically as well as syntactically correct based on the prompt?
        Are there any superfluous changes made in the modified content based on the prompt?
        The content has been provided by the file name followed by its file content.


        Original Content: 
        {originalFiles}
        
        Modified Content: 
        {modifiedFiles}
        
        Respond "true" if changes are needed. Else, respond "false". Provide a list of all the improvements needed if and only if you respond "true". Keep the modifications concise.
        """
    )

    return promptTemplate.format(originalFiles=strOriginalFiles, modifiedFiles=strModifiedFiles, userPrompt=userPrompt)

def getRevision(files, modifications, userPrompt):
    strFiles = "\n".join([f"File Name: {filename}\nContent: \n{content}" for filename, content in files.items()])

    promptTemplate = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"""
                Objective: 
                Modify the files provided that need changing to satisfy the user's request for modifications.
                Make sure to address any concerns with the content being superfluous, if mentioned in the modifications.
                The user has provided the file names, each associated with its content, followed by the list of modifications.

                Output: 
                Return the response similar to the user input - by extracting every file name and generating the new code associated with that file below it.
                Return this only for every file you change. Ignore files and their content for ones that do not need any change.

                Notes: 
                Do not add comments to mention what has changed.
                If a comment is being added, phrase it in a way that remains consistent with other comments in the file's content."""
            ),
            (
                "user",
                """
                {files}
                
                Modifications: 
                {modifications}
                """
            )
        ]
    )

    return promptTemplate.format_messages(files=strFiles, modifications=modifications, userPrompt=userPrompt)