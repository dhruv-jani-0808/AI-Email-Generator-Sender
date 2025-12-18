# 📧 AI Email Generator & Sender

A professional-grade email automation tool that leverages **Google Gemini AI** to craft context-aware emails and **Python's SMTP library** to send them instantly. Built with a sleek, interactive **Streamlit** interface.

---

## ✨ Features

* **AI-Powered Drafting:** Uses Gemini 2.5 Flash to generate high-quality subject lines and email bodies.
* **Customizable Tones:** Choose between Professional, Formal, or Casual styles.
* **Smart Length Control:** Generate Short, Medium, or Long emails based on your needs.
* **Live Preview & Edit:** Review and manually tweak the AI-generated draft before hitting send.
* **Automated Delivery:** Integrated SMTP logic to send emails directly from the app.
* **Modern UI:** Clean, form-based interface with state management to prevent accidental refreshes.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Engine:** [Google GenAI (Gemini)](https://ai.google.dev/)
* **Backend:** Python 3.x
* **Protocol:** SMTP (Simple Mail Transfer Protocol)

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.8+
* A Google Gemini API Key
* A Gmail account with an **App Password** enabled.

### 2. Installation
Clone the repository:
```bash
git clone https://github.com/dhruv-jani-0808/AI-Email-Generator-Sender
cd AI-Email-Generator-Sender
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a .env file in the root directory and add your credentials:

```Code snippet
GEMINI_API_KEY=your_gemini_api_key_here
EMAIL_PASSWORD=your_gmail_app_password_here
```
4. Run the App
```bash
streamlit run app.py
```
