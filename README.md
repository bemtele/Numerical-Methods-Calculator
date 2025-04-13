# **PDF Tools Web App - README**

## **📌 Overview**
A **Flask-based web application** deployed on **Heroku** that allows users to:
- **Merge two PDF files** into one.
- **Extract specific pages** from a PDF file.

🔗 **Live Demo:** [https://free-pdf-tools.herokuapp.com](https://free-pdf-tools.herokuapp.com)

---

## **✨ Features**
✅ **Merge PDFs** – Combine two PDFs into a single file.  
✅ **Extract Pages** – Select specific pages (e.g., `1,3,5-7`) from a PDF.  
✅ **User-Friendly UI** – Simple web interface with no installation required.  
✅ **Free & Hosted on Heroku** – No cost for basic usage.  

---

## **🛠️ How It Works**
1. **Homepage** – Choose between **Merge PDFs** or **Extract Pages**.
2. **Merge PDFs** – Upload two PDFs, and the app combines them.
3. **Extract Pages** – Upload a PDF and specify pages (e.g., `1,3,5-7`).
4. **Download** – Get the processed file instantly.

---

## **🚀 Deployment (Heroku - No CLI Needed)**
### **Method 1: One-Click Deploy (Fastest)**
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/yourusername/pdf-tools-heroku) *(Replace with your GitHub repo URL)*

### **Method 2: Manual Deployment via Heroku Web**
1. **Fork this repo** on [GitHub](https://github.com/bemtele/pdf-tools-heroku).
2. **Go to [Heroku](https://heroku.com)** → Create New App.
3. **Connect to GitHub** and select your forked repo.
4. **Deploy Branch** (`main` or `master`).
5. **Open App** → Done! 🎉

---

## **🔧 Local Setup (For Development)**
### **Prerequisites**
- Python 3.7+
- Git (optional)

### **Steps**
1. **Clone the repo**
   ```sh
   git clone https://github.com/yourusername/pdf-tools-heroku.git
   cd pdf-tools-heroku
   ```
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the app locally**
   ```sh
   python app.py
   ```
4. **Open in browser** → `http://localhost:5000`

---

## **📂 Project Structure**
```
pdf-tools-heroku/
├── app.py               # Flask application
├── requirements.txt     # Python dependencies
├── Procfile             # Heroku config
├── runtime.txt          # Python version (optional)
└── templates/           # HTML pages
    ├── index.html       # Homepage
    ├── merge.html       # PDF merger UI
    └── extract.html     # PDF extractor UI
```

---

## **⚠️ Limitations (Free Heroku Tier)**
- **Files are temporary** (Heroku has an ephemeral filesystem).
- **App sleeps after 30 mins** of inactivity (first load may be slow).
- **Max file upload size**: ~16MB.

**Fix?** Upgrade to a **paid Heroku plan** for permanent storage & always-on performance.

---

## **🛑 Troubleshooting**
| Issue | Solution |
|-------|----------|
| App crashes on Heroku | Check logs: **Heroku Dashboard → More → View logs** |
| File upload fails | Ensure PDFs are <16MB |
| Slow first load | Heroku free tier sleeps; wait 5-10 secs |
| Missing dependencies | Verify `requirements.txt` is correct |

---

## **📜 License**
MIT License - Free for personal & commercial use.

---

## **💡 Future Improvements**
- [ ] Add **password protection** for PDFs.
- [ ] Support **batch processing** (multiple files).
- [ ] Add **image-to-PDF** conversion.
- [ ] Improve UI with **drag-and-drop**.

---

## **📬 Contact**
- **GitHub**: [@bemtele](https://github.com/bemtele)
- **Email**: bemtele@gmail.com

---

### **🎉 Enjoy the tool? Give it a ⭐ on GitHub!**
[![GitHub Stars](https://img.shields.io/github/stars/bemtele/pdf-tools-heroku?style=social)](https://github.com/bemtele/pdf-tools-heroku)

---

