# 🛡️ Blockchain-Based Product Verification & Analytics Dashboard  
*A blockchain-inspired system for product authenticity, tamper detection, and supply chain analytics.*

---

## 📌 Overview

This project demonstrates how **hashing + data analytics** can be used to simulate blockchain-style product verification.  
Although **no real blockchain** is used, each row in the Excel dataset is assigned a **SHA-256 hash** that acts as a digital fingerprint.  
Any modification to product details results in a **hash mismatch**, helping detect tampering instantly.

The dashboard is built using **Streamlit**, with features for data visualization, product lifecycle tracking, and verification.

---

## 🎯 Objectives

- ✔️ Verify product authenticity using **batch numbers + hash validation**  
- ✔️ Visualize analytics such as category distribution, stock levels & pricing trends  
- ✔️ Track product lifecycle (manufacturing date, expiry, certifications, etc.)  
- ✔️ Build trust through **tamper detection** using hashing logic  

---

## 🧠 Key Concept: Hashing (SHA-256)

This project demonstrates the **Avalanche Effect** of hashing:

```
Input: "Hello"
Hash: aaf4c61ddcc5e8a2dabede0f3b482cd9...

Input: "hello"
Hash: 5d41402abc4b2a76b9719d911017c592...
```

Even a tiny change → completely different hash.

### Hash Used For:
- Tamper detection  
- Product authenticity  
- Immutability simulation  
- Fingerprint generation  

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Streamlit** | Frontend UI |
| **Pandas** | Data processing |
| **Plotly Express** | Interactive visualizations |
| **Datetime** | Timestamps |
| **Hashlib (SHA-256)** | Hash generation |
| **Openpyxl** | Excel reading/writing |

---

## 📊 Features

### 🔍 **1. Product Verification**
- Search by **Batch ID**
- Recalculate hash → match with stored hash
- Shows **authentic / tampered** status

### 📈 **2. Analytics Dashboard**
Includes:
- Category distribution pie chart  
- Stock-level bar chart  
- Price trends  
- Manufacturing & expiry timeline  
- Certification summary  

### 🔗 **3. Blockchain-Inspired Structure (Simulated)**
Not a real blockchain — but mimics the concepts:
- Block index  
- Timestamp  
- Product data  
- Hash + Previous hash  
- Immutability  
- Traceability  

---

## 📁 Folder Structure

```
📦 blockchain-product-verification-dashboard
│
├── app.py
├── data/
│   └── products.xlsx
├── images/
│   └── screenshots.png
├── README.md
└── requirements.txt
```

---

## 🏗️ Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/blockchain-product-verification-dashboard.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the dashboard:

```bash
streamlit run app.py
```

---

## ⚠️ Limitations

- ❌ No real blockchain backend → hashes stored locally  
- ❌ Excel is static → needs manual updates  
- ❌ Hash sensitive to formatting changes  
- ❌ Dashboard runs locally (not deployed)  
- ❌ No real-time supply chain data  

---

## 🚀 Future Enhancements

- 🔗 Integrate real blockchain (Ethereum / Hyperledger Fabric)  
- 📱 Add QR-code scanning for instant verification  
- ☁️ Deploy to Streamlit Cloud  
- 🛰️ Real-time data updates  
- 🔌 API integration with ERP systems  

---

## 🤝 Contributing

This project is created for educational and demonstration purposes.  
Feel free to fork, improve, and submit pull requests!

---

## ⭐ Support

If you find this useful, please ⭐ the repository!

---

## 👨‍💻 Author

**ALBIN SAJI**  
