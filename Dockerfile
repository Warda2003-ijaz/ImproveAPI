# 1. Base image: Python 3.13 ka chhota (slim) version
FROM python:3.13-slim

# 2. Container ke andar kaam karne ka folder
WORKDIR /app

# 3. Pehle sirf requirements copy aur install karo (cache ka faida)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Ab baqi saara code copy karo
COPY . .

# 5. App port 8000 par chalegi
EXPOSE 8000

# 6. Container start hote hi yeh command chalegi
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
