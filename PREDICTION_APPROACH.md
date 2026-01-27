# Booking Confirmation Prediction Approach

## Overview

This document explains the **mock AI/ML logic** used to predict the **confirmation probability (%)** of a waitlisted booking in the *Sleeper Bus Booking System (Ahmedabad → Mumbai)*.

The objective is to demonstrate **analytical thinking, feature selection, and model reasoning** using a **simulated historical dataset**, as required by the assignment.

---

## Prediction Goal

To estimate the **percentage probability** that a waitlisted ticket will be confirmed before the travel date.

This prediction helps users understand the likelihood of seat clearance on busy routes.

---

## Mock Historical Dataset

A simulated dataset is included in the repository: `mock_booking_data.csv`

This file represents **historical booking and waitlist behavior** and is used for feature selection and weight reasoning. Below is a sample of the data structure used:

| booking_id | waitlist_position | days_before_travel | route_category | outcome |
|:-----------|:------------------|:-------------------|:---------------|:--------|
| B001       | 2                 | 15                 | Long           | 1       |
| B002       | 25                | 1                  | Long           | 0       |
| B003       | 5                 | 10                 | Short          | 1       |

> **Note:**
> * `outcome`: **1** represents a Confirmed booking, **0** represents Cancelled/Not Cleared.
> * `route_category`: A derived feature where "Long" represents Ahmedabad → Mumbai and "Short" represents intermediate stops.
> * The dataset is **not used at runtime** and exists purely for analytical and documentation purposes.

---

## Dataset Structure

The mock CSV (`mock_booking_data.csv`) contains records with the following fields:

| Column Name | Description |
|------------|------------|
| booking_id | Unique booking identifier |
| waitlist_position | Position in waitlist queue |
| days_before_travel | Days remaining before departure |
| route_category | Derived feature ('Long' for Abd-Mum, 'Short' for others) |
| outcome | Target Variable (1 = Confirmed, 0 = Cancelled/Not Cleared) |

This structure represents a **pre-processed** dataset ready for model training, where raw station names have already been categorized into route types.

---

## Input Features Used for Prediction

Based on analysis of the mock dataset, the following features were selected:

### 1. Waitlist Position
- Strongest predictor of confirmation probability
- Lower position → higher chance of clearance

### 2. Days Before Travel
- More days remaining → higher likelihood of cancellations
- Last-minute requests have significantly lower probability

### 3. Route Demand
- Long, high-demand routes (Ahmedabad → Mumbai) have lower clearance rates
- Shorter segments show better availability patterns

---

## Model Choice (Mock)

### Simulated Logistic Regression (Rule-Based)

A **rule-based heuristic model inspired by Logistic Regression** is used instead of training a real ML model.

### Rationale
- Limited dataset
- Clear explainability
- Explicitly allowed by assignment
- Demonstrates ML reasoning without unnecessary complexity

---

## Prediction Logic Breakdown

1. **Base Probability**
   - Initial probability score set to 100%

2. **Waitlist Penalty**
   - Probability decreases linearly with waitlist position

3. **Time-Based Adjustment**
   - >10 days before travel → bonus
   - <5 days → penalty
   - <2 days → heavy penalty

4. **Route Demand Adjustment**
   - Busy routes apply an additional reduction

5. **Stochastic Noise**
   - Small random variance (±5%)
   - Simulates real-world uncertainty

6. **Clamping**
   - Final output restricted between **0% and 99%**

---

## Sample Prediction Scenarios

### Scenario 1: High Probability
- Waitlist Position: 2
- Days Before Travel: 12
- Route: Ahmedabad → Mumbai

Predicted Probability: **~80–90%**

---

### Scenario 2: Medium Probability
- Waitlist Position: 6
- Days Before Travel: 5
- Route: Ahmedabad → Surat

Predicted Probability: **~40–60%**

---

### Scenario 3: Low Probability
- Waitlist Position: 12
- Days Before Travel: 1
- Route: Ahmedabad → Mumbai

Predicted Probability: **<10%**

---

## Output Format

The prediction API returns:

- `probability` → Confirmation chance in percentage
- `confidence_score` → High / Medium
- `drivers` → Key contributing factors

Example:
```json
{
  "probability": 72,
  "confidence_score": "High",
  "drivers": {
    "queue_impact": -15,
    "time_impact": "Positive"
  }
}
