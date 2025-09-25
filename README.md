# 🌊 RippleWorks – AquaPredict Pro  

An interactive **Water Quality Intelligence System** built with machine learning and Streamlit.  
This project predicts **Water Quality Index (WQI)** (numeric score) and **Water Quality Classification (WQC)** (Excellent / Good / Medium / Poor / Very Poor) based on water parameters.  

<img width="1365" height="733" alt="image" src="https://github.com/user-attachments/assets/96cbccad-3a5e-4c4c-a0e0-7c2636439459" />

---

##  Features  
- End-to-end pipeline: cleaning → feature engineering → modeling → deployment  
- Handles **missing values** (KNN/median strategies) and **outliers** (IQR capping + domain thresholds)  
- Computes **WQI** dynamically and categorizes into classes (WQC)  
- Supports both **regression (WQI prediction)** and **classification (WQC prediction)**  
- Deployed as a sleek **Streamlit web app**  

---

##  Tech Stack  
- **Python** (Pandas, NumPy, Scikit-learn, XGBoost)  
- **Streamlit** for web UI  
- **Joblib** for model persistence  
- **GitHub + Streamlit Cloud** for deployment  

---

##  Dataset  
Source: Kaggle – Indian River Water Quality dataset  
- 1991 rows, 8 key water quality parameters  
- Target variables engineered: **WQI** and **WQC**  

---


