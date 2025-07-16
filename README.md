# 🌍 Early Warning Dashboard for Conflict & Unrest Prevention

> A project for the **Commonwealth's Good Offices** under the **Commonwealth Secretariat**  
> Designed, developed, and deployed as a Prototype + Proof of Concept (PoC) for conflict anticipation and early intervention across 56 Commonwealth nations.

---

## 🧠 Project Overview

**Codeforces** presents a real-time, AI-powered **Early Warning Dashboard** that aggregates, analyzes, and visualizes critical news events from across Commonwealth countries. Our system detects **potential and active conflicts** using a **severity scoring model**, powered by **fine-tuned large language models (LLMs)** and real-time data from news sources and RSS feeds.

This dashboard enhances the Commonwealth Secretariat’s ability to **monitor geopolitical, social, economic, and environmental unrest**, and respond with informed, data-backed interventions.

---

## ✨ Features

### 🏠 Home Page – Central Intelligence Hub
- 🌐 **Interactive World Map**: Red blinking markers show unrest locations in real-time.
- 🗂️ **Three Smart Tabs**:
  - **Active** – Events with severity score > 0.8
  - **Potential** – Events between 0.6 and 0.8
  - **All News** – Complete stream of news articles from 56 countries
- 📰 **Categorized News**: Articles are grouped into events (Political, Economic, Social, Environmental, etc.)
- 📊 **Severity Score Calculation**: Events are dynamically ranked and prioritized using a multi-parameter scoring model.

### 📌 Event Detail Page
- 🧵 **Timeline View**: Visual sequence of related articles, leading up to and following the core event.
- 📈 **Severity Score & Stability Index**: Updated in real time using incoming data trends.
- 🔍 **Country-Specific Dashboard**:
  - View top events
  - Trend lines for **Stability Index**, **Political**, **Social**, and **Economic Indicators**

### 🖌️ UI/UX & Design
- 🧑‍🎨 Modern and clean interface developed using **React.js** with **Mapbox** integration.
- 🎨 Initial wireframes and high-fidelity UI prototypes created in **Figma**.
- ⚙️ Responsive layout with emphasis on clarity, accessibility, and actionable intelligence.

---

## 🤖 Intelligence Behind the Scenes

### 🧠 NLP + ML Model Architecture
- ⚙️ **Custom LLM Pipeline** using **Hugging Face Transformers**, fine-tuned on:
  - Historical conflict event datasets 
  - Commonwealth-specific news datasets
- 🧾 **Named Entity Recognition** (NER): Filters news articles by location relevance to Commonwealth countries.
- 🧠 **Topic Modeling** (LDA & BERTopic): Categorizes articles into meaningful themes.
- 📍 **Geospatial Filtering**: Retains only location-mapped, crisis-related articles.
- 📊 **Trend & Anomaly Detection**: Highlights unusual spikes in unrest-related topics across time.
- 🧮 **Severity Score Formula**:  
  \[
  \text{Score} = w_1 \cdot \text{Sentiment} + w_2 \cdot \text{Frequency} + w_3 \cdot \text{Impact Magnitude} + w_4 \cdot \text{Geographical Spread}
  \]

---

## ⚙️ Tech Stack

| Layer          | Technology                                                                 |
|----------------|----------------------------------------------------------------------------|
| Frontend       | React.js, Tailwind CSS, Mapbox, Chart.js                                   |
| Backend        | Node.js, Express.js, Flask (for ML integration)                            |
| Databases      | MongoDB (news/events), Redis (caching), PostgreSQL (stability index)       |
| ML & NLP       | Hugging Face Transformers, spaCy, Gensim (LDA), BERTopic                   |
| Scraping Tools | RSS Feeds, BeautifulSoup, Selenium                                         |                       

---

## 📌 Architecture Flow

```text
[News Scraper (RSS/NGO/Twitter)] 
        ↓
[Keyword + NER + Geospatial Filtering] 
        ↓
[Topic Modeling + Trend Detection] 
        ↓
[Severity Score Calculation & Event Grouping] 
        ↓
[Dashboard Visualization & Stability Index Update]
```

## Project Team

Team Name: Codeforces

Members: 
- Ritul Kulkarni
- Anish Ketkar
- Parth Desai

Students of K. J. Somaiya School of Engineering, under the Commonwealth Secretariat’s Good Offices programme.
Focused on peacebuilding, timely conflict prevention, and data-driven diplomacy.

## License

This project is developed for research and demonstration under the Commonwealth Secretariat and is not intended for commercial use.

## Acknowledgements

Commonwealth Secretariat – Good Offices team

Hugging Face & spaCy – For powerful open-source NLP tools

Open Source community ❤️

## Report

[Detailed Report_Team CodeForces.pdf](https://github.com/user-attachments/files/21264672/Detailed.Report_Team.CodeForces.pdf)

## Team PPT

[Codeforces.pptx](https://github.com/user-attachments/files/21264805/Codeforces.pptx)
