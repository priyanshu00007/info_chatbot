# 🧠 GenZway AI: Product & Review Intelligence Chatbot (CLI Version)

An AI-powered terminal application built using **LangChain**, **Ollama (LLaMA3)**, and **Chroma** that allows you to:

* 🔍 Ask intelligent questions based on product reviews
* 📝 Auto-generate SEO-optimized product descriptions
* 💬 Summarize customer sentiment, pros & cons
  Perfect for brands, marketers, and analysts who want instant insights from raw product feedback.
![Uploading image.png…]()

---

## 🚀 Features

* 💡 **Smart Q\&A** about brands/products using GenZway content
* 🧠 **LLaMA 3 integration** with Ollama (local LLM for privacy and speed)
* 🧾 **CSV-based review parsing**
* 🧮 **Chroma Vector Store** using `mxbai-embed-large` for semantic search
* 🔁 **Fully CLI-based interaction** with continuous input loop

---

## 📁 Project Structure

```
genzway-ai/
│
├── app.py                  # Main chatbot loop (CLI)
├── setup_vector.py         # Builds vector DB from reviews
├── content_detail.txt      # GenZway intro paragraph (fallback content)
├── content_detail.csv      # Reviews file with columns: Title, Review, Rating, Date
├── chroma_langchain_db/    # Chroma persistent storage
├── README.md               # You’re here!
```

---

## 🧱 Tech Stack

| Component       | Technology Used             |
| --------------- | --------------------------- |
| LLM             | LLaMA3 via Ollama           |
| Embeddings      | `mxbai-embed-large`         |
| Vector DB       | Chroma + LangChain          |
| CLI Interaction | Python + LangChain CLI loop |
| Data            | CSV or TXT-based reviews    |

---

## 📥 Installation & Setup

### 1. Clone this repository

```bash
git clone https://github.com/yourusername/genzway-ai.git
cd genzway-ai
```

### 2. Install dependencies

```bash
pip install langchain langchain-community langchain-core langchain-chroma pandas ollama
```

### 3. Setup Ollama (LLaMA3)

Install Ollama from [https://ollama.com](https://ollama.com), then run:

```bash
ollama pull llama3
```

> ⚠️ Make sure Ollama is running in the background.

### 4. Prepare Content

* Put **GenZway paragraph** in `content_detail.txt`
* Or put **review data** in `content_detail.csv` with the following columns:

```csv
Title,Review,Rating,Date
Amazing Pizza,"Loved the taste and quick delivery",5,2024-02-11
Not Great,"Too oily and the crust was soggy",2,2024-02-09
```

### 5. Initialize Vector Store

Run the following once:

```bash
python setup_vector.py
```

### 6. Start the Chatbot

```bash
python app.py
```

---

## 🧪 Example Questions to Try

* "What are the common complaints about this product?"
* "Summarize what customers love the most."
* "Can you give me a product description for GenZway based on the reviews?"

---

## 📌 Error Handling

### Error: `model 'llama3' not found (status code: 404)`

✅ Solution:

```bash
ollama pull llama3
```

### Error: `Please create 'content_detail.txt'...`

✅ Solution: Ensure your `content_detail.txt` file exists and is not empty.

---

## 📘 Sample Workflow

```bash
$ python setup_vector.py  # Setup database from CSV or text
$ python app.py           # Start asking questions!

Ask your question (q to quit): What do customers think about the product?

Answer:
Customers frequently mention the fast delivery, but also raise concerns about oiliness in the crust...
```

---

## 🧑‍💻 Author

**Priyanshu Rathod**
AI & Full Stack Developer | Building tools that think 🤖
[LinkedIn](https://linkedin.com/in/your-profile) · [GitHub](https://github.com/yourusername)

---

## 📄 License

This project is licensed under the MIT License.
