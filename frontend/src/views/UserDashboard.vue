<template>
  <div class="fullpage d-flex justify-content-center align-items-center">
    <div class="card shadow-lg p-4 dashboard-card">
      <div class="card-body">
        <!-- Heading -->
        <div class="text-center mb-4">
          <h1 class="display-5 fw-bold text-primary">QuizMaster</h1>
          <p class="lead text-muted">User Dashboard</p>
        </div>

        <!-- Table -->
        <div class="table-responsive mb-4">
          <table
            class="table table-bordered table-hover text-center align-middle"
          >
            <thead class="table-dark">
              <tr>
                <th>ID</th>
                <th>Quiz Title</th>
                <th>Subject</th>
                <th>Chapter</th>
                <th>No. of Questions</th>
                <th>Duration</th>
                <th>Operation</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="quizzes.length === 0">
                <td colspan="7" class="text-muted">No quizzes available</td>
              </tr>
              <tr v-for="quiz in quizzes" :key="quiz.id">
                <td>{{ quiz.id }}</td>
                <td>{{ quiz.title }}</td>
                <td>{{ quiz.subject_name }}</td>
                <td>{{ quiz.chapter_name }}</td>
                <td>{{ quiz.number_of_questions }}</td>
                <td>{{ quiz.duration }}</td>
                <td>
                  <button
                    class="btn btn-sm btn-outline-primary me-2 rounded-pill"
                    @click="viewQuiz(quiz)"
                  >
                    View
                  </button>
                  <button
                    class="btn btn-sm btn-outline-success rounded-pill"
                    @click="startQuiz(quiz)"
                  >
                    Start
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Scoreboard Button -->
        <div class="text-center mb-2">
          <button
            class="btn btn-info btn-lg rounded-pill w-100"
            @click="goToScoreboard"
          >
            View Scoreboard
          </button>
        </div>

        <!-- Logout Button -->
        <div class="text-center">
          <button
            class="btn btn-secondary btn-lg rounded-pill w-100"
            @click="logout"
          >
            Logout
          </button>
        </div>
      </div>
    </div>

    <!-- View Modal -->
    <div class="modal fade" id="viewModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Quiz Details</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <p>
              <strong>Subject:</strong> {{ selectedQuiz.subject_id }}.
              {{ selectedQuiz.subject_name }}
            </p>
            <p>
              <strong>Chapter:</strong> {{ selectedQuiz.chapter_id }}.
              {{ selectedQuiz.chapter_name }}
            </p>
            <p>
              <strong>Quiz:</strong> {{ selectedQuiz.id }}.
              {{ selectedQuiz.title }}
            </p>
            <p>
              <strong>Number of Questions:</strong>
              {{ selectedQuiz.number_of_questions }}
            </p>
            <p><strong>Date:</strong> {{ selectedQuiz.date }}</p>
            <p><strong>Duration:</strong> {{ selectedQuiz.duration }}</p>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Modal } from "bootstrap";

export default {
  name: "UserDashboard",
  data() {
    return {
      quizzes: [],
      selectedQuiz: {},
      viewModalInstance: null,
    };
  },
  created() {
    const token = localStorage.getItem("token");
    if (!token) {
      this.$router.push("/login");
    } else {
      this.fetchQuizzes();
    }
  },
  methods: {
    fetchQuizzes() {
      const token = localStorage.getItem("token");
      axios
        .get("http://localhost:5000/quiz/quizzes/all", {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((response) => {
          this.quizzes = response.data;
        })
        .catch((error) => {
          console.error("Error fetching quizzes:", error);
          this.quizzes = [];
        });
    },
    viewQuiz(quiz) {
      this.selectedQuiz = quiz;
      this.showViewModal();
    },
    startQuiz(quiz) {
      this.$router.push({
        name: "TakeQuizPage",
        params: { quizId: quiz.id },
      });
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },
    showViewModal() {
      if (!this.viewModalInstance) {
        this.viewModalInstance = new Modal(
          document.getElementById("viewModal")
        );
      }
      this.viewModalInstance.show();
    },
    goToScoreboard() {
      this.$router.push("/scoreboard");
    },
  },
};
</script>

<style scoped>
.fullpage {
  height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #f6d365, #fda085);
  overflow: auto;
  padding: 20px;
}
.dashboard-card {
  width: 100%;
  max-width: 1000px;
  border-radius: 1rem;
  background-color: #ffffff;
}
.table {
  margin-bottom: 0;
}
.table th,
.table td {
  vertical-align: middle;
}
.btn-outline-primary,
.btn-outline-success,
.btn-secondary {
  padding: 0.4rem 1rem;
  font-size: 0.9rem;
  border-radius: 2rem;
}
.btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
}
.btn-secondary:hover {
  background-color: #5a6268;
  border-color: #545b62;
}
</style>
