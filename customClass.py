from pydantic import BaseModel, Field

class RequestBody(BaseModel):
    repoUrl: str
    prompt: str

class File(BaseModel):
    name: str = Field(description="Name of the file")
    content: str = Field(description="Content of the file")

class FileSystem(BaseModel):
    files: list[File] = Field(description="List of files that need modification")

class Reflection(BaseModel):
    isNeedModifications: bool = Field(description="Boolean that is true when files need further changes. Else, it is false")
    modifications: str = Field(description="List of changes that need to be applied on the file content")