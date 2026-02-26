# Base image
FROM python:3.12

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install fastapi uvicorn llama-cpp-python streamlit requests pydantic

# Expose ports
EXPOSE 8000
EXPOSE 8501

# Run FastAPI server
CMD ["python", "deploy/app.py"]