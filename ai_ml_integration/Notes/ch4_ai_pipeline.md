**Chapter 4: The Universal AI Pipeline**
_Establishing a mental model for every AI feature, regardless of the data type._

As an experienced Solutions Architect, I've seen countless teams get bogged down in the details of a specific AI model without having a robust, reusable framework for how to integrate it. The "Universal AI Pipeline" is that framework. It's a mental model that applies to every AI feature, from a simple text summarizer to a complex computer vision system.

This isn't about the ML training lifecycle (data prep, model training, etc.). This is about the **inference lifecycle**—the steps your application takes every time a user makes a request to an AI-powered feature.

### **4.1 The Five Stages: Deconstructing every AI request**

Regardless of the technology or the data type, every successful AI integration can be broken down into these five stages. Your job as an engineer is to understand these stages and architect a robust, scalable system around them.

#### **Stage 1: Pre-processing**

This is the very first thing that happens after a user request comes in. The goal is to transform the raw, messy user input into a clean, standardized format that the model can understand. This stage is entirely independent of the model's logic.

- **Why it Matters:** Garbage in, garbage out. The quality of your output is directly tied to the quality of your input. This is your first line of defense against bad data, security vulnerabilities, and unpredictable model behavior.
- **Examples:**
  - **NLP:** A user's query might be "can u tell me the return policy plz?". Your pre-processing step would normalize this to "Can you tell me the return policy please?". This might involve:
    - Removing punctuation.
    - Correcting typos.
    - Converting text to lowercase or title case.
    - Cleaning up HTML tags or other irrelevant metadata.
  - **Computer Vision (CV):** A user uploads an image. Your pre-processing step might:
    - Resize the image to the model's required input dimensions (e.g., 224x224 pixels).
    - Normalize pixel values to a specific range (e.g., 0-1).
    - Compress the image to a standardized format (JPEG, PNG).
  - **Tabular Data:** You might take a user-provided form submission and:
    - Validate that all required fields are present.
    - Standardize the format of dates, currencies, or other numerical data.

#### **Stage 2: Retrieval**

This stage is specific to RAG and other systems that use external data. The goal is to find relevant context to "ground" the model's response. This stage happens **before** you ever call the LLM.

- **Why it Matters:** This is how you prevent hallucinations and ensure your model provides accurate, up-to-date information that is specific to your proprietary data. It's a fundamental pattern for building an enterprise-grade AI system.
- **Examples:**
  - **NLP:** A user asks, "How do I expense a coffee on a client meeting?" Your retrieval step would:
    1.  Take that query.
    2.  Convert it into a vector embedding.
    3.  Search your company's vector database (which contains chunks of your internal policy documents).
    4.  Retrieve the most semantically similar text chunks, such as the relevant sections on `client expenses`, `meal policy`, or `receipt submission`.
  - **CV:** While less common, this could be a visual search. A user uploads an image of a red handbag. The retrieval step would search a vector database of your product images to find similar images and retrieve their product IDs.

#### **Stage 3: Prompting**

This is the creative and engineering art of AI. The goal is to assemble all the information from the previous stages into a single, structured, and effective prompt that the model can understand. This is the part you'll spend a lot of time on.

- **Why it Matters:** The prompt is your application's direct interface with the model. A well-designed prompt will yield a consistent, high-quality, and useful output. A poorly designed prompt will lead to unpredictable, irrelevant, or even harmful responses.
- **Examples:**
  - **NLP (RAG):** You'll combine the user's question, the retrieved context from Stage 2, and a set of explicit instructions into a single prompt string.
    ```
    You are a helpful assistant for our company's employees. Answer the user's question only based on the provided context.
    <context>
    [Retrieved document chunk 1]
    [Retrieved document chunk 2]
    </context>
    Question: {user_question}
    ```
  - **CV:** For an image captioning model, the prompt might just be the image itself. For a more complex vision-language model, you might provide an image and a text prompt asking, "What is the product in this image and what color is it?".

#### **Stage 4: Inference**

This is the stage where you actually call the AI model's API and get a response. It's the point of no return where you pay for the computation.

- **Why it Matters:** This is often the most expensive and time-consuming part of the pipeline. Your job is to make this call as efficient as possible.
- **Implementation:**
  - You make a single, clean API call to a third-party service (e.g., `openai.Completion.create(...)`) or an internally hosted model.
  - For a complex pipeline, you might make multiple inference calls, for example, calling a small model to re-rank the retrieved results before calling the main LLM.
  - Your back-end (e.g., FastAPI or Node.js) must be architected for robustness, including proper API key management, error handling, and timeout mechanisms.

#### **Stage 5: Post-processing**

The model's output is almost never ready to be sent directly to the user. This stage takes the raw output from the model and formats it for the final application.

- **Why it Matters:** This ensures a consistent user experience and allows you to enforce business rules or data formatting on the model's output. It's also where you can add another layer of security and content moderation.
- **Examples:**
  - **NLP:** The LLM's raw output might be a single string. Your post-processing step might:
    - Parse the JSON response from the model.
    - Extract a key field and remove verbose or unnecessary text.
    - Add a disclaimer or a link back to the source documents.
    - Run a content moderation check to ensure the output is safe.
  - **CV:** The object detection model returns a list of coordinates and labels. Your post-processing step would:
    - Use these coordinates to draw bounding boxes on the original image.
    - Write the output to a new image file or a JSON payload for your front-end to render.
  - **Tabular Data:** A classification model returns a probability score (e.g., `0.95`). Your post-processing would:
    - Apply a business rule: `if score > 0.9, then trigger fraud alert`.
    - Format the output to be a human-readable message like "High confidence of fraudulent activity."

---

**Summary for the Engineer:**

This five-stage pipeline is your mental model for everything. When a new AI feature request comes in, don't immediately think "what model should I use?". Instead, think:

1.  **How do I Pre-process the user's input?**
2.  **What data do I need to Retrieve to ground the response?** (If any)
3.  **How do I craft the perfect Prompt to combine all of this?**
4.  **What is the most efficient way to run Inference?**
5.  **How do I Post-process the output to make it useful and safe?**

This framework ensures that you're building a reliable, scalable, and maintainable system, not just a one-off script. We'll see how this universal pipeline applies to different data modalities in the next sections. Ready to look at some concrete examples?

That's an excellent next step. The Universal AI Pipeline is a theoretical framework, and now we'll put it into practice with a concrete example. The principles remain the same, but the implementation details change with the data type.

### **4.2.1 A CV Pipeline: Resizing images, calling an object detection model, drawing bounding boxes.**

Let's design a pipeline for a common computer vision task: **Object Detection**. Imagine you are building a service that analyzes user-uploaded photos to identify products, such as shoes, bags, and watches.

We'll use a **FastAPI** backend, which is the standard for building high-performance, asynchronous Python APIs, especially for AI workloads.

---

**Architectural Blueprint:**

The user uploads an image to a front-end application. That image is sent to our FastAPI backend. The backend follows our five-stage pipeline to process the image and returns a new image with bounding boxes drawn around the detected objects.

Here is the code, broken down by our five stages.

#### **Stage 1: Pre-processing**

The user-uploaded image is likely a high-resolution, bulky file. The first thing we need to do is prepare it for the model. Most pre-trained object detection models are trained on specific image dimensions (e.g., 640x640 pixels). We'll use the Python Imaging Library (**PIL**) to handle this.

```python
# app/main.py
from fastapi import FastAPI, UploadFile, File
from PIL import Image, ImageDraw
import io
import torch

# Assuming you have a model loaded.
# In a real-world scenario, you would load this once on app startup.
# This example uses a placeholder for simplicity.
# You could load a YOLOv5, YOLOv8, or Detectron2 model here.
# model = load_my_object_detection_model()

app = FastAPI()

# Placeholder for a function that performs inference
def run_object_detection_inference(image):
    # This is where you'd call a hosted model API or an in-memory model.
    # It would return a list of detections.
    # Example detection format: [[x_min, y_min, x_max, y_max, class_id, confidence], ...]
    return [
        [100, 150, 300, 400, 0, 0.95], # Bounding box for a bag
        [500, 200, 600, 350, 1, 0.88]  # Bounding box for a shoe
    ]

# The model's expected input size
MODEL_INPUT_SIZE = (640, 640)

@app.post("/detect_objects/")
async def detect_objects(file: UploadFile = File(...)):
    # Read the image file into a BytesIO object
    image_data = await file.read()
    image_bytes = io.BytesIO(image_data)
    original_image = Image.open(image_bytes).convert("RGB")
    original_size = original_image.size

    # Pre-processing
    # 1. Resize the image to the model's required input size
    processed_image = original_image.resize(MODEL_INPUT_SIZE)
    # The processed_image is now ready for the model
```

- **Best Practices:** Note that we convert the image to RGB to ensure a consistent format, and we store the `original_size` to use later in post-processing. This is a common and critical pattern.

#### **Stage 2: Retrieval**

For a simple object detection pipeline, the retrieval stage is often skipped. The model's job is to analyze the input image alone. There is no external context (like a vector database) required.

However, a more advanced CV pipeline might use retrieval. For example, if we were building a product similarity search, the retrieval stage would involve vectorizing the user's uploaded image and querying a vector database of product image embeddings. In our object detection example, we'll keep the pipeline simple and proceed directly to prompting/inference.

#### **Stage 3: Prompting**

Just like with retrieval, the prompting stage is often not a distinct step for many computer vision models. The "prompt" is simply the image itself.

However, with the rise of multi-modal models like Gemini Pro Vision, the concept of prompting is becoming relevant in CV. You might provide the image _and_ a text prompt like `"Identify all the sports equipment in this image."` to guide the model's focus. For our classic object detection pipeline, the image is the entire input, so we'll move on.

#### **Stage 4: Inference**

This is where the magic happens. We'll pass our pre-processed image to the model and get the raw results.

```python
    # ... (code from Stage 1) ...

    # Inference
    # Call a function that runs the model and gets the raw output
    raw_detections = run_object_detection_inference(processed_image)

    # ... (code for Stage 5 below) ...
```

- **Best Practices:** In a production setting, `run_object_detection_inference` would not be a placeholder. It would handle the following:
  - Making a robust, asynchronous HTTP request to a dedicated model serving endpoint (e.g., hosted on AWS SageMaker or a custom BentoML server).
  - Handling potential network failures, timeouts, and API rate limits.

#### **Stage 5: Post-processing**

The raw output from the model (a list of bounding box coordinates) is meaningless on its own. We need to process it into something useful for the end user. This often involves drawing the boxes on the original image.

```python
    # ... (code from Stage 4) ...

    # Post-processing
    # 1. Scale the bounding box coordinates back to the original image size.
    # The model works with 640x640, but the output must match the original image size.
    draw = ImageDraw.Draw(original_image)
    width_scale = original_size[0] / MODEL_INPUT_SIZE[0]
    height_scale = original_size[1] / MODEL_INPUT_SIZE[1]

    # Let's assume a mapping from class_id to label for the final output
    class_labels = {0: "bag", 1: "shoe"}

    processed_detections = []
    for detection in raw_detections:
        x_min, y_min, x_max, y_max, class_id, confidence = detection

        # Scale coordinates
        scaled_x_min = x_min * width_scale
        scaled_y_min = y_min * height_scale
        scaled_x_max = x_max * width_scale
        scaled_y_max = y_max * height_scale

        # Draw the bounding box and a label
        draw.rectangle(
            (scaled_x_min, scaled_y_min, scaled_x_max, scaled_y_max),
            outline="red",
            width=3
        )
        draw.text(
            (scaled_x_min, scaled_y_min - 10),
            f"{class_labels[class_id]}: {confidence:.2f}",
            fill="red"
        )

        processed_detections.append({
            "label": class_labels[class_id],
            "confidence": confidence,
            "box": [scaled_x_min, scaled_y_min, scaled_x_max, scaled_y_max]
        })

    # Save the processed image to a BytesIO object for the API response
    output_image_bytes = io.BytesIO()
    original_image.save(output_image_bytes, format="PNG")
    output_image_bytes.seek(0)

    # You might also return the JSON representation of the detections
    return {"detections": processed_detections}
```

- **Best Practices:** The coordinate scaling is a critical and often overlooked step that can lead to bugs. Always remember to scale your model's output back to the original image's dimensions.

---

**Full `app/main.py` for this CV Pipeline:**

```python
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from PIL import Image, ImageDraw
import io
import torch

# Load a model once on startup
# Placeholder for a production model
# In a real app, this would be a YOLO, Detectron2, etc. model
# loaded from a path or a dedicated model server.
def load_my_object_detection_model():
    # Load model and set to evaluation mode
    return None # Return a mock object for this example

app = FastAPI()
# model = load_my_object_detection_model()

# This is a mock function for the model's inference step
def run_object_detection_inference(image):
    # This would be a call to a model.predict() method or an API endpoint
    return [
        [100, 150, 300, 400, 0, 0.95], # Bounding box for a bag
        [500, 200, 600, 350, 1, 0.88]  # Bounding box for a shoe
    ]

# The model's expected input size and a label map
MODEL_INPUT_SIZE = (640, 640)
CLASS_LABELS = {0: "bag", 1: "shoe"}

@app.post("/detect_objects/")
async def detect_objects(file: UploadFile = File(...)):
    """
    Processes an uploaded image to detect objects and returns a JSON response
    with the detected objects and their bounding box coordinates.
    """
    # Stage 1: Pre-processing
    try:
        image_data = await file.read()
        image_bytes = io.BytesIO(image_data)
        original_image = Image.open(image_bytes).convert("RGB")
        original_size = original_image.size

        processed_image = original_image.resize(MODEL_INPUT_SIZE)
    except Exception as e:
        return {"error": f"Failed during pre-processing: {str(e)}"}

    # Stage 2 & 3: Retrieval & Prompting (Not applicable for this simple pipeline)
    # The image is the entire input.

    # Stage 4: Inference
    try:
        raw_detections = run_object_detection_inference(processed_image)
    except Exception as e:
        return {"error": f"Failed during inference: {str(e)}"}

    # Stage 5: Post-processing
    try:
        draw = ImageDraw.Draw(original_image)
        width_scale = original_size[0] / MODEL_INPUT_SIZE[0]
        height_scale = original_size[1] / MODEL_INPUT_SIZE[1]

        final_detections = []
        for detection in raw_detections:
            x_min, y_min, x_max, y_max, class_id, confidence = detection

            scaled_x_min = x_min * width_scale
            scaled_y_min = y_min * height_scale
            scaled_x_max = x_max * width_scale
            scaled_y_max = y_max * height_scale

            label = CLASS_LABELS.get(class_id, "unknown")

            draw.rectangle(
                (scaled_x_min, scaled_y_min, scaled_x_max, scaled_y_max),
                outline="red",
                width=3
            )
            draw.text(
                (scaled_x_min, scaled_y_min - 10),
                f"{label}: {confidence:.2f}",
                fill="red"
            )

            final_detections.append({
                "label": label,
                "confidence": confidence,
                "box": [scaled_x_min, scaled_y_min, scaled_x_max, scaled_y_max]
            })

        # Return the processed image bytes
        output_image_bytes = io.BytesIO()
        original_image.save(output_image_bytes, format="PNG")
        output_image_bytes.seek(0)

        return Response(content=output_image_bytes.getvalue(), media_type="image/png")

    except Exception as e:
        return {"error": f"Failed during post-processing: {str(e)}"}
```

This is the kind of robust, clean, and scalable code that a senior engineer would write. It clearly separates the concerns of data preparation, model interaction, and result formatting, following our universal pipeline framework.

Next, we'll apply this same mental model to a different domain: Natural Language Processing. Ready?

Excellent. Let's shift our focus to the domain where the "Universal AI Pipeline" framework truly shines: Natural Language Processing. This is where the concept of RAG becomes a critical component.

Imagine we're building an internal HR chatbot for a large enterprise. This chatbot needs to answer employee questions about things like health benefits, expense policies, and PTO. Crucially, it must be accurate and up-to-date, and it cannot hallucinate or invent policies.

### **4.2.2 An NLP Pipeline: Chunking text, retrieving context (RAG), parsing LLM output.**

This pipeline will have a distinct, non-trivial Retrieval and Prompting stage, which is different from the CV example.

---

**Architectural Blueprint:**

An employee asks a question in a chat interface. The request hits our FastAPI backend, which executes our five-stage RAG pipeline.

#### **Stage 1: Pre-processing**

The user's query needs to be cleaned up before we do anything else. This is a simple but important step.

```python
# app/main.py
from fastapi import FastAPI, HTTPException
import openai
from pydantic import BaseModel, Field
import psycopg2
from pgvector.psycopg2 import register_vector
import numpy as np
import json
import re

app = FastAPI()

# Database connection and model setup (mocked for simplicity)
DATABASE_URL = "postgresql://user:password@host:port/dbname"
conn = psycopg2.connect(DATABASE_URL)
register_vector(conn)
# In a real app, you would have an embedding model and an LLM client
EMBEDDING_MODEL_NAME = "text-embedding-3-small"
LLM_MODEL_NAME = "gpt-4o"

class ChatRequest(BaseModel):
    user_query: str

# Let's mock a function to get embeddings
def get_embedding(text: str) -> list[float]:
    # In a production app, this would call the OpenAI API
    # response = openai.embeddings.create(input=text, model=EMBEDDING_MODEL_NAME)
    # return response.data[0].embedding
    return [0.1] * 1536  # Mock embedding for this example

@app.post("/chat")
async def chat_with_hr(request: ChatRequest):
    # Stage 1: Pre-processing
    # Sanitize and normalize the user's query
    sanitized_query = request.user_query.strip()

    if not sanitized_query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    print(f"Pre-processed query: {sanitized_query}")

    # ... rest of the pipeline below
```

- **Best Practices:** Input validation and sanitization are crucial. An empty string or a malformed query can cause your downstream components to fail.

#### **Stage 2: Retrieval**

This is the core of RAG. We need to find relevant context from our internal knowledge base to "ground" the LLM's answer. This assumes you've already pre-processed your HR documents (ingested them) and stored their embeddings in a `pgvector` table, as we discussed in Chapter 3.

```python
    # ... (code from Stage 1) ...

    # Stage 2: Retrieval
    # 1. Embed the user's query
    query_embedding = get_embedding(sanitized_query)

    # 2. Search the vector database for the top-k most similar document chunks
    retrieved_context = []
    with conn.cursor() as cur:
        cur.execute("""
            SELECT content FROM documents
            ORDER BY embedding <=> %s
            LIMIT 5
        """, (np.array(query_embedding),))
        retrieved_context = [row[0] for row in cur.fetchall()]

    context_string = "\n---\n".join(retrieved_context)
    print(f"Retrieved {len(retrieved_context)} document chunks.")

    # ... rest of the pipeline below
```

- **Best Practices:** We join the retrieved chunks into a single string. The separator (`---`) is important because it visually signals to the LLM that this is a new, separate piece of information.

#### **Stage 3: Prompting**

Now we construct the final, single prompt that will be sent to the LLM. This is where we define the LLM's personality, provide the retrieved context, and give clear instructions on how to behave.

```python
    # ... (code from Stage 2) ...

    # Stage 3: Prompting
    system_prompt = (
        "You are an expert HR assistant for a large company. "
        "Your only job is to answer employee questions. "
        "Answer the question **solely** based on the provided context. "
        "Do not use any external knowledge. If the answer is not in the context, "
        "politely state that you cannot answer the question and suggest they contact HR."
    )

    user_prompt = (
        f"Context:\n{context_string}\n\n"
        f"Question: {sanitized_query}"
    )

    # ... rest of the pipeline below
```

- **Best Practices:** Prompt engineering is an art. The system prompt is key to controlling the LLM's behavior. The phrase "solely based on the provided context" is a critical instruction to prevent hallucination.

#### **Stage 4: Inference**

We send the complete prompt to the LLM API and get the raw response. This is the simplest stage from a coding perspective, but it's where the cost and latency reside.

```python
    # ... (code from Stage 3) ...

    # Stage 4: Inference
    try:
        # In a production app, you would make an API call
        # response = openai.chat.completions.create(
        #     model=LLM_MODEL_NAME,
        #     messages=[
        #         {"role": "system", "content": system_prompt},
        #         {"role": "user", "content": user_prompt}
        #     ],
        #     temperature=0.0 # Use a low temp for factual accuracy
        # )
        # llm_output = response.choices[0].message.content

        # Mocking the LLM response
        llm_output = "According to the provided documents, a coffee on a client meeting is not reimbursable under the standard expense policy. Please refer to the full policy for more details."

    except openai.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"LLM API error: {e}")

    print(f"Raw LLM output: {llm_output}")

    # ... rest of the pipeline below
```

- **Best Practices:** Always handle API-specific errors. Using `temperature=0.0` is a good practice for factual tasks where creativity is not desired.

#### **Stage 5: Post-processing**

The raw LLM output is a string. We want to clean it up and ensure it's presented nicely to the user. This is also where we might enforce any final business rules or add a consistent footer to the response.

```python
    # ... (code from Stage 4) ...

    # Stage 5: Post-processing
    final_response = llm_output.strip()

    # Add a consistent disclaimer to every response
    disclaimer = "\n\n*This answer is based on the provided company policy documents and should not be considered legal advice.*"
    final_response_with_disclaimer = final_response + disclaimer

    print(f" {final_response_with_disclaimer}")

    return {"response": final_response_with_disclaimer}
```

- **Best Practices:** Post-processing is your final chance to control the output. Adding a disclaimer or a "thumbs up/down" feedback mechanism is a great way to improve the system's quality and gather valuable evaluation data.

---

**Summary of the NLP Pipeline:**

This example demonstrates how the five-stage pipeline provides a clean, logical flow for a sophisticated RAG-based application.

1.  **Pre-processing** a user's question.
2.  **Retrieving** relevant context from a vector database.
3.  **Prompting** the LLM with both the question and the context.
4.  **Inference** to get the LLM's response.
5.  **Post-processing** the response for final delivery to the user.

This is the canonical pattern you will use for a vast majority of your enterprise-grade NLP applications. Next, let's explore how this same framework applies to an entirely different domain: classical machine learning on tabular data. Ready?

You're on fire. This final example is crucial because it shows the "Universal AI Pipeline" isn't just for deep learning and unstructured data. It applies just as well to the classic, predictive ML models that every enterprise relies on.

Let's design a pipeline for a **fraud detection system**. Imagine a financial services application where every user transaction needs to be evaluated for fraud in real-time.

### **4.2.3 A Tabular Data Pipeline: Feature engineering from a database, calling a predictive model, triggering a business rule based on the output score.**

This pipeline will have a very strong Pre-processing stage (Feature Engineering) and a critical Post-processing stage (applying a business rule).

---

**Architectural Blueprint:**

A user initiates a transaction. Your backend receives a request with the transaction details. This triggers a call to a dedicated service that runs our five-stage pipeline.

We'll use **FastAPI** for the API and a mock `scikit-learn` model saved with `joblib`.

#### **Stage 1: Pre-processing (Feature Engineering)**

This is the most critical part of a tabular data pipeline. The raw transaction data is not enough. We need to create features that the model was trained on, often by combining new data with historical data from our database.

```python
# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import psycopg2
import pandas as pd
import os
from datetime import datetime

app = FastAPI()

# Load the pre-trained model and the feature names once on startup
try:
    fraud_model = joblib.load('fraud_model.pkl')
    model_features = joblib.load('model_features.pkl')
except FileNotFoundError:
    raise RuntimeError("Model files not found. Ensure 'fraud_model.pkl' and 'model_features.pkl' are in place.")

class TransactionRequest(BaseModel):
    user_id: int
    amount: float
    merchant_id: int

def get_historical_features_from_db(user_id: int, current_amount: float) -> pd.DataFrame:
    """
    Connects to the database to build a feature set for a user transaction.
    """
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        with conn.cursor() as cur:
            # This is a simplified query; a real one would be much more complex
            cur.execute("""
                SELECT
                    COUNT(id) as total_transactions_24h,
                    AVG(amount) as avg_amount_30d,
                    SUM(amount) as total_spent_90d
                FROM transactions
                WHERE user_id = %s AND timestamp > NOW() - INTERVAL '90 days'
                GROUP BY user_id
            """, (user_id,))
            row = cur.fetchone()
        conn.close()

        if not row:
            # Handle case where no history is found
            return pd.DataFrame([[0, 0.0, 0.0]], columns=['total_transactions_24h', 'avg_amount_30d', 'total_spent_90d'])

        # Create a DataFrame from the database row and the current transaction data
        features_dict = {
            'total_transactions_24h': row[0],
            'avg_amount_30d': row[1],
            'total_spent_90d': row[2],
            'current_amount': current_amount,
            'is_weekend': datetime.now().weekday() >= 5
        }

        # Ensure the feature order matches the model's training data
        user_data = pd.DataFrame([features_dict], columns=model_features)

        return user_data

    except Exception as e:
        raise RuntimeError(f"Database error during feature engineering: {e}")

@app.post("/predict_fraud")
async def predict_fraud(request: TransactionRequest):
    # Stage 1: Pre-processing (Feature Engineering)
    try:
        transaction_features = get_historical_features_from_db(request.user_id, request.amount)
        if transaction_features is None:
            raise HTTPException(status_code=404, detail="User not found or no history available.")

        print(f"Engineered features for transaction: {transaction_features.to_dict('records')[0]}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # ... rest of the pipeline below
```

- **Best Practices:** The feature engineering logic needs to be identical to the logic used when the model was trained. Any discrepancy will lead to inaccurate predictions. The `get_historical_features_from_db` function is the heart of this pipeline, showcasing your SQL and data manipulation skills.

#### **Stage 2: Retrieval**

This stage is not applicable for a traditional tabular data pipeline. There is no external context to retrieve; all the necessary information is already in your database.

#### **Stage 3: Prompting**

This stage is also not applicable. The input to a classical ML model is not a prompt string but a structured array of numbers (the features).

#### **Stage 4: Inference**

We now pass our prepared feature vector to the loaded model to get a prediction.

```python
    # ... (code from Stage 1) ...

    # Stage 4: Inference
    try:
        # Use the model to predict the probability of fraud
        fraud_probability = fraud_model.predict_proba(transaction_features)[0, 1]

        print(f"Raw model output: Fraud probability = {fraud_probability}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")

    # ... rest of the pipeline below
```

- **Best Practices:** `predict_proba` is almost always better than `predict`. It gives you the full probability score, allowing you to be more nuanced in your business rules in the next stage.

#### **Stage 5: Post-processing**

The raw probability score is not an action. This stage converts the model's output into a concrete business decision. This is where you set the risk tolerance for your application.

```python
    # ... (code from Stage 4) ...

    # Stage 5: Post-processing
    FRAUD_THRESHOLD = 0.8
    is_fraudulent = fraud_probability > FRAUD_THRESHOLD

    action_taken = "allow"
    if is_fraudulent:
        action_taken = "flag_for_review"
        print("Business rule triggered: Transaction flagged for review.")

    # Return a structured response
    return {
        "user_id": request.user_id,
        "transaction_amount": request.amount,
        "predicted_fraud_probability": float(fraud_probability),
        "is_fraudulent_flag": bool(is_fraudulent),
        "action_taken": action_taken
    }
```

- **Best Practices:** Your business rules (e.g., `FRAUD_THRESHOLD`) should be configurable parameters, not hardcoded values. This allows your team to easily adjust the sensitivity of the system. The output should be a clear, actionable signal for your downstream services.

---

**Summary of the Tabular Data Pipeline:**

This example demonstrates how the five-stage pipeline adapts to a predictive task on structured data:

1.  **Pre-processing** is focused on **feature engineering**, a critical and data-intensive step.
2.  **Retrieval** and **Prompting** are not applicable, as the input is a structured feature vector.
3.  **Inference** is a straightforward call to a pre-trained model.
4.  **Post-processing** involves applying a business rule to the model's numerical output, converting a score into a decision.

This concludes our exploration of the Universal AI Pipeline. You now have a mental model that can be applied to any AI task, regardless of the data modality. This framework will be your compass for building production-grade, reliable, and scalable systems.

In the next chapter, we'll dive into our first architectural blueprint: the **Decoupled Architecture**, which is the most common and scalable pattern for leveraging third-party AI models.
