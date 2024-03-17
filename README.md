# Home Assist | [at-home-in-germany.com](http://at-home-in-germany.com/)

![Brandenburger Tor | Photo: Daniel Le](frontend/img/sidebar_img.jpg)
*Brandenburger Tor | Photo: Daniel Le*
<br>

`Home Assist` is a personal project designed to assist refugees, migrants, and expats who are moving to Germany. The main goal of this project is to simplify the settlement process in Germany, with a particular focus on housing-related topics.

This is an `on-going` project, and the current version is a prototype that provides general information and assistance on various topics, such as finding accommodation, understanding the rental market, and dealing with landlords. The project uses the OpenAI GPT-3.5 model with the employment of RAG (Retrieval-Augmented Generation) to retrieve relevant information from a provided knowledge base and generate responses to user queries.

## Project Structure
The application is divided into two main parts (architecture-wise): the backend and the frontend.

## Backend
It is built with Python and uses the OpenAI GPT-3.5 model to generate responses to user queries. The backend is responsible for processing user inputs and generating appropriate responses. The main file is backend_app.py, and it uses the HomeAssist class from model.py to interact with the AI model.
The LLM model is backed RAG to retrieve relevant information from a provided knowledge base, and by Pinecone, a vector database that allows for fast and efficient similarity search for our knowledge base.

*TODO*: To integrate Langchain agent for accessing a broader knowledge base, e.g. with Google search capability.

The backend app is deployed with FastAPI and runs on port 8112.
The endpoint is /ask, and it accepts POST requests with a JSON payload containing the user's query, including chat history.

## Frontend
The frontend app is built with Streamlit and provides a user-friendly interface for interacting with the AI model. The main file is frontend_app.py, which sets up the Streamlit interface and handles user inputs and outputs.
The frontend app runs on port 8111, and it communicates with the backend app by making POST requests to the backend API.

## Deployment
The project is containerized using Docker and can be run using Docker Compose. The docker-compose.yaml file contains the configuration for running the backend and frontend services.

To start the project, run the following command in the terminal after you already exported the require secrets to environment variables:

```
docker-compose up
```
This will start the backend service on port 8112 and the frontend service on port 8111.

Secrets to be exported to environment variables:
`.envrc`:
```
export OPENAI_API_KEY=""
export PINECONE_API_KEY=""
export PINECONE_API_ENV=""
```



## Contributing
Feedback and suggestions are always welcome.

## License
This project is licensed under the terms of the LICENSE file.

## Disclaimer
This project is intended to provide general information and assistance to individuals moving to Germany. It is not a substitute for professional advice or help and should not be relied on for making decisions. Always seek the advice of a qualified professional for any questions you may have.

## Acknowledgements
This project uses the OpenAI GPT-3.5 model for generating responses. The use of this model is subject to the terms and conditions of OpenAI.

## Contact
For any questions or feedback, please reach out to me at khoadaniel@example.com.