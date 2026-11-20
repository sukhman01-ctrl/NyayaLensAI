"""
NyayaLens AI - Model Training & Evaluation Pipeline
Trains and evaluates Scikit-learn NLP classifiers on labeled Indian legal clauses.
Outputs: Accuracy, Precision, Recall, F1-Score, Confusion Matrix, and serialized models.
"""

import os
import json
# pyrefly: ignore[missing-import]
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support, confusion_matrix
# pyrefly: ignore[missing-import]
import joblib

DATA_PATH = Path(__file__).resolve().parent / "app" / "data" / "synthetic_clause_dataset.json"
MODELS_DIR = Path(__file__).resolve().parent / "app" / "data" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

def train_and_evaluate():
    print("=" * 70)
    print("NyayaLens AI - Machine Learning Training & Evaluation Pipeline")
    print("=" * 70)

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [item["text"] for item in data]
    types = [item["clause_type"] for item in data]
    risks = [item["risk_level"] for item in data]

    print(f"\n[1] Ingested Dataset: {len(data)} Labeled Legal Clauses (Synthetic Benchmark)")
    print(f"    - Unique Clause Categories: {len(set(types))} ({', '.join(sorted(list(set(types))))})")
    print(f"    - Risk Levels: {', '.join(sorted(list(set(risks))))}")

    # =========================================================================
    # TASK 1: CLAUSE CATEGORY CLASSIFIER
    # =========================================================================
    print("\n" + "-" * 70)
    print("TASK 1: TRAINING CLAUSE CATEGORY CLASSIFIER (TF-IDF + Logistic Regression)")
    print("-" * 70)

    X_train_type, X_test_type, y_train_type, y_test_type = train_test_split(
        texts, types, test_size=0.25, random_state=42, stratify=types
    )

    type_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=800, stop_words='english')),
        ('clf', LogisticRegression(C=2.0, max_iter=500, random_state=42))
    ])

    type_pipeline.fit(X_train_type, y_train_type)
    y_pred_type = type_pipeline.predict(X_test_type)

    acc_type = accuracy_score(y_test_type, y_pred_type)
    prec_type, rec_type, f1_type, _ = precision_recall_fscore_support(y_test_type, y_pred_type, average='weighted', zero_division=0)
    report_type_dict = classification_report(y_test_type, y_pred_type, output_dict=True, zero_division=0)

    print(f"\n>> Clause Category Results on Held-out Test Set ({len(y_test_type)} clauses):")
    print(f"   Accuracy:  {acc_type * 100:.2f}%")
    print(f"   Precision: {prec_type * 100:.2f}%")
    print(f"   Recall:    {rec_type * 100:.2f}%")
    print(f"   F1-Score:  {f1_type * 100:.2f}%")
    print("\nClassification Report (per class):")
    print(classification_report(y_test_type, y_pred_type, zero_division=0))

    # Save Model
    type_model_path = MODELS_DIR / "clause_type_model.joblib"
    joblib.dump(type_pipeline, type_model_path)
    print(f"[+] Serialized model saved to: {type_model_path}")

    # =========================================================================
    # TASK 2: RISK SEVERITY CLASSIFIER
    # =========================================================================
    print("\n" + "-" * 70)
    print("TASK 2: TRAINING RISK SEVERITY CLASSIFIER (TF-IDF + Calibrated LinearSVC)")
    print("-" * 70)

    X_train_risk, X_test_risk, y_train_risk, y_test_risk = train_test_split(
        texts, risks, test_size=0.25, random_state=42, stratify=risks
    )

    base_svc = LinearSVC(C=1.5, random_state=42, max_iter=2000)
    calibrated_svc = CalibratedClassifierCV(base_svc, cv=3)

    risk_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=800, stop_words='english')),
        ('clf', calibrated_svc)
    ])

    risk_pipeline.fit(X_train_risk, y_train_risk)
    y_pred_risk = risk_pipeline.predict(X_test_risk)

    acc_risk = accuracy_score(y_test_risk, y_pred_risk)
    prec_risk, rec_risk, f1_risk, _ = precision_recall_fscore_support(y_test_risk, y_pred_risk, average='weighted', zero_division=0)
    cm_risk = confusion_matrix(y_test_risk, y_pred_risk, labels=["Critical", "High", "Medium", "Low"])
    report_risk_dict = classification_report(y_test_risk, y_pred_risk, output_dict=True, zero_division=0)

    print(f"\n>> Risk Severity Results on Held-out Test Set ({len(y_test_risk)} clauses):")
    print(f"   Accuracy:  {acc_risk * 100:.2f}%")
    print(f"   Precision: {prec_risk * 100:.2f}%")
    print(f"   Recall:    {rec_risk * 100:.2f}%")
    print(f"   F1-Score:  {f1_risk * 100:.2f}%")
    print("\nClassification Report (per risk level):")
    print(classification_report(y_test_risk, y_pred_risk, zero_division=0))

    print("\nConfusion Matrix (Labels: Critical, High, Medium, Low):")
    print("                Pred_Crit  Pred_High  Pred_Med  Pred_Low")
    risk_labels = ["Critical", "High", "Medium", "Low"]
    for row_idx, row in enumerate(cm_risk):
        print(f"Actual_{risk_labels[row_idx]:<8}   {row[0]:>8}   {row[1]:>8}  {row[2]:>8}  {row[3]:>8}")

    # Save Model
    risk_model_path = MODELS_DIR / "risk_level_model.joblib"
    joblib.dump(risk_pipeline, risk_model_path)
    print(f"\n[+] Serialized model saved to: {risk_model_path}")

    # =========================================================================
    # SAVE STRUCTURED EVALUATION REPORT
    # =========================================================================
    eval_report = {
        "dataset_name": "NyayaLens Synthetic Indian Legal Clauses Benchmark",
        "dataset_size": len(data),
        "test_split_ratio": 0.25,
        "clause_classifier": {
            "algorithm": "TF-IDF + LogisticRegression(C=2.0)",
            "accuracy": round(float(acc_type), 4),
            "precision": round(float(prec_type), 4),
            "recall": round(float(rec_type), 4),
            "f1_score": round(float(f1_type), 4),
            "per_class": report_type_dict
        },
        "risk_classifier": {
            "algorithm": "TF-IDF + CalibratedClassifierCV(LinearSVC)",
            "accuracy": round(float(acc_risk), 4),
            "precision": round(float(prec_risk), 4),
            "recall": round(float(rec_risk), 4),
            "f1_score": round(float(f1_risk), 4),
            "confusion_matrix": cm_risk.tolist(),
            "labels": ["Critical", "High", "Medium", "Low"],
            "per_class": report_risk_dict
        }
    }

    eval_json_path = MODELS_DIR / "evaluation_report.json"
    with open(eval_json_path, "w", encoding="utf-8") as f:
        json.dump(eval_report, f, indent=2)

    print(f"[+] Comprehensive evaluation metrics exported to: {eval_json_path}")
    print("=" * 70)
    print("TRAINING & EVALUATION COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    train_and_evaluate()
