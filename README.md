# The Quiz Master – V2

## 📌 Project Overview
**The Quiz Master – V2** is a multi-user interactive application designed to help students improve their exam preparation through targeted quizzes and performance tracking.  

This project builds upon **Quiz Master – V1**, adding enhanced features for managing subjects, chapters, quizzes, and users, along with analytics and visualization support.  

The platform supports two roles:
- **Admin** – Can manage subjects, chapters, quizzes, and users.
- **User** – Can take quizzes, track scores, and monitor progress over time.

---

## ⚙️ Tech Stack

### Frontend
- **Vue.js** (Vue CLI advanced setup) for a modular, dynamic **SPA** (Single-Page Application).  
- **Bootstrap** for clean, responsive styling and layout.

### Backend
- **Flask** for building a RESTful API and handling business logic.  
- **JWT (JSON Web Tokens)** for secure authentication and protecting restricted routes.

### Database
- **SQLite** for persistent storage of users, subjects, chapters, quizzes, and scores.

### Graphs & Analytics
- **Chart.js** integrated for visualizations such as line and pie charts to track quiz performance.

---

## 💻 Development Environment
- IDE: **Visual Studio Code**  
- Backend runs inside a **Python Virtual Environment**  


---

## 📂 Database Schema (High-Level)
- **User** – Stores user information and authentication data.  
- **Subject** – Represents subjects created by admins.  
- **Chapter** – Chapters linked to subjects.  
- **Quiz** – Quiz details including subject, chapter, and metadata.  
- **Question** – Individual questions linked to quizzes.  
- **Score** – Tracks quiz attempts, user scores, and progress.

---

## 🚀 Features
- User authentication (JWT-secured).  
- Role-based access (Admin/User).  
- CRUD operations for subjects, chapters, quizzes, and questions.  
- Quiz-taking functionality with score tracking.  
- Performance analytics using charts and visual reports.  
- Responsive UI with Bootstrap.  

