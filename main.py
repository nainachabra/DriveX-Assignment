from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = FastAPI()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Adding CORS middleware to allow requests from the frontend
origins = [
    "http://localhost:3000",  # React App origin
    "http://127.0.0.1:3000",  # React App local development address
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows access from these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Load the tokenizer and model
chosen_model = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(chosen_model)
model = AutoModelForSeq2SeqLM.from_pretrained(chosen_model)

@app.post("/ask_question")
async def handle_question(file: UploadFile = File(...), question: str = Form(...)):
    try:
        print(f"Received question: {question}")
        
        # 1. Ensure the file is an Excel file
        if file.content_type not in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
            print(f"Error: Unsupported file type - {file.content_type}")
            raise HTTPException(status_code=400, detail="Only Excel files are allowed.")
        
        # 2. Read the uploaded file
        contents = await file.read()
        print(f"File contents received, reading Excel file...")

        try:
            df = pd.read_excel(BytesIO(contents))
            print(f"Excel file loaded successfully. Number of rows: {len(df)}")
        except Exception as e:
            print(f"Error reading the Excel file: {e}")
            raise HTTPException(status_code=400, detail=f"Error reading Excel file: {str(e)}")

        # 3. Convert the DataFrame to a string for the model
        if df.empty:
            print("Error: The Excel file is empty or not properly formatted.")
            raise HTTPException(status_code=400, detail="The Excel file is empty or not properly formatted.")
        
        text_data = df.to_string(index=False)
        print(f"Data extracted from Excel: {text_data[:200]}...")  # Show only first 200 chars

        columns = list(df.columns)
        data = []
        for row in df.itertuples(index=False):
            data.append("; ".join([f"{key}: {val}" for key, val in zip(columns, row)]))
        data = "\n".join(data)
        print(f"Processed data: {data[:200]}...")  # Show only first 200 chars for debugging

        # 4. Ask the question to the model
        input_text = f"Context: {data}\n\nQuestion: {question}\n\nAnswer:"
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=4096)
        
        # Ensure the model is generating correctly
        try:
            outputs = model.generate(**inputs, max_length=150, num_beams=3)
            answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
            print(f"Model answer: {answer}")
        except Exception as e:
            print(f"Error generating model response: {e}")
            raise HTTPException(status_code=500, detail="Error generating model response")

        return JSONResponse(content={"answer": answer})
    
    except HTTPException as e:
        print(f"HTTP error occurred: {e.detail}")
        raise e  # Re-raise HTTP exceptions
    except Exception as e:
        print(f"General error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
@app.options("/ask_question")
async def options():
    return {"message": "OK"}
   
@app.get("/")
def read_root():
    return {"message": "Welcome to the Drivex Assignment submitted by Naina Chabra"}