## Setup Steps

1. **Clone the Repository**

   ```sh
   git clone https://github.com/ShanthoshPrabhu/autocomplete-backend.git
   cd autocomplete-backend
   ```

2. **Install uv (if not already installed)**

   ```sh
   pip install uv
   ```

3. **Sync Python Dependencies**

   ```sh
   uv sync --frozen
   ```

4. **(Optional) Run the Initial Script**

   ```sh
   uv run script.py
   ```

5. **Run Database Migrations**

   ```sh
   uv run alembic upgrade head
   ```

6. **Start the Backend Server**
   ```sh
   uv run main.py
   ```
   The API will be available at [http://localhost:8000](http://localhost:8000) by default.

---

## API Usage

- **Autocomplete Endpoint**
  - **URL:** `/autocomplete`
  - **Method:** `GET`
  - **Query Parameters:**
    - `query` (string): The text to autocomplete.
    - `limit` (int, optional): Maximum number of suggestions (default: 10).
  - **Headers:**
    - `Authorization: Bearer <FIREBASE_ID_TOKEN>`
  - **Response:**
    ```json
    {
      "suggestions": ["suggestion1", "suggestion2"]
    }
    ```

---

## Firebase Setup Notes

- The backend uses Firebase for authentication. You must provide valid Firebase credentials and ensure your Firebase project is set up.
- Make sure your Firebase Admin SDK credentials are available to the backend, typically via a service account JSON file.
- The backend will verify the `Authorization` header in incoming requests using Firebase.

---
