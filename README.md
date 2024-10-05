# TinyGen

AI powered API service that can modify your GitHub code in seconds

Built for CodeGen's New Grad role home assigment

**Developed by Abhinav Gupta**

## Setup Instructions

- Clone this repository
- Setup a virtual environment
- Run `pip install -r requirements.txt`
- Set `OPENAI_KEY` and `DATABASE_URI` in the `.env` file
- Run `python server.py`
- Open `http://localhost:8000/docs` on the browser to see the API docs

## Notes on Implementation

- Used Render platform for deployment of this service.
- Supabase DB was integrated to post responses along with the prompts from API requests. There is another to fetch these.
- Built a reflection strategy where an LLM agent reflects on the response and suggests modifications. Then, the revsiion LLM agent makes enhancements based on the modifications. This is a cyclical process.
- Built a `GitRepoHandler` service to abstract all operations associated with the repository for code readability and modularity.
- Built a `SessionHandler` service to abstract all operations associated with Supabase for code readability and modularity.
