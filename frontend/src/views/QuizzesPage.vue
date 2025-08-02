<template>
  <div class="fullpage d-flex justify-content-center align-items-center">
    <div class="card shadow-lg p-4 dashboard-card">
      <div class="card-body">
        <!-- Heading -->
        <div class="text-center mb-4">
          <h1 class="display-5 fw-bold text-primary">QuizMaster</h1>
          <p class="lead text-muted">Admin Dashboard</p>
          <p class="fw-semibold text-dark mt-2">
            {{ subjectId }}. {{ subjectName }} ({{ chapterId }}.
            {{ chapterName }})
          </p>
        </div>

        <!-- Table -->
        <div class="table-responsive mb-4">
          <table
            class="table table-bordered table-hover text-center align-middle"
          >
            <thead class="table-dark">
              <tr>
                <th style="width: 5%">ID</th>
                <th style="width: 25%">Title of Quiz</th>
                <th style="width: 15%">Date of Quiz</th>
                <th style="width: 15%">Time Duration</th>
                <th style="width: 20%">Remarks</th>
                <th style="width: 20%">Operations</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="quizzes.length === 0">
                <td colspan="6" class="text-muted">No quizzes added yet</td>
              </tr>
              <tr v-for="quiz in quizzes" :key="quiz.id">
                <td>{{ quiz.id }}</td>
                <td>{{ quiz.title }}</td>
                <td>{{ quiz.date_of_quiz }}</td>
                <td>{{ quiz.time_duration }}</td>
                <td>{{ quiz.remarks }}</td>
                <td>
                  <button
                    class="btn btn-sm btn-outline-primary me-2 rounded-pill"
                    @click="editQuiz(quiz)"
                  >
                    Edit
                  </button>
                  <button
                    class="btn btn-sm btn-outline-danger me-2 rounded-pill"
                    @click="deleteQuiz(quiz.id)"
                  >
                    Delete
                  </button>
                  <button
                    class="btn btn-sm btn-outline-success rounded-pill"
                    @click="openQuestions(quiz)"
                  >
                    Open
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Add Quiz Button -->
        <div class="text-center">
          <button
            class="btn btn-success btn-lg rounded-pill w-100"
            @click="openModalForAdd"
          >
            Add Quiz
          </button>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div class="modal fade" id="quizModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ isEditMode ? "Edit Quiz" : "Add Quiz" }}
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <input
              v-model="form.title"
              class="form-control mb-3"
              placeholder="Title of Quiz"
            />
            <input
              type="date"
              v-model="form.date_of_quiz"
              class="form-control mb-3"
              placeholder="Date of Quiz"
            />
            <input
              type="time"
              v-model="form.time_duration"
              class="form-control mb-3"
              placeholder="Time Duration"
            />
            <textarea
              v-model="form.remarks"
              class="form-control"
              placeholder="Remarks"
              rows="3"
            ></textarea>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Cancel
            </button>
            <button type="button" class="btn btn-primary" @click="saveQuiz">
              Save
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
  name: "QuizzesPage",
  props: ["subjectId", "subjectName", "chapterId", "chapterName"],
  data() {
    return {
      // Local copies to avoid mutating props
      localSubjectId: this.subjectId,
      localSubjectName: this.subjectName,
      localChapterId: this.chapterId,
      localChapterName: this.chapterName,

      quizzes: [],
      isEditMode: false,
      editingQuizId: null,
      form: {
        title: "",
        date_of_quiz: "",
        time_duration: "",
        remarks: "",
      },
      modalInstance: null,
    };
  },
  watch: {
    "$route.params": {
      immediate: true,
      handler(params) {
        this.localSubjectId = params.subjectId;
        this.localSubjectName = params.subjectName;
        this.localChapterId = params.chapterId;
        this.localChapterName = params.chapterName;
        this.fetchQuizzes();
      },
    },
  },
  mounted() {
    this.modalInstance = new Modal(document.getElementById("quizModal"));
  },
  methods: {
    async fetchQuizzes() {
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get(
          `http://localhost:5000/quiz/chapters/${this.localChapterId}/quizzes`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        this.quizzes = res.data;
      } catch (err) {
        console.error("Error fetching quizzes:", err);
      }
    },

    openModalForAdd() {
      this.isEditMode = false;
      this.form = {
        title: "",
        date_of_quiz: "",
        time_duration: "",
        remarks: "",
      };
      this.modalInstance.show();
    },

    editQuiz(quiz) {
      this.isEditMode = true;
      this.editingQuizId = quiz.id;
      this.form = {
        title: quiz.title,
        date_of_quiz: quiz.date_of_quiz,
        time_duration: quiz.time_duration,
        remarks: quiz.remarks,
      };
      this.modalInstance.show();
    },

    async saveQuiz() {
      const token = localStorage.getItem("token");
      try {
        if (this.isEditMode) {
          await axios.put(
            `http://localhost:5000/quiz/quizzes/${this.editingQuizId}`,
            this.form,
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          const index = this.quizzes.findIndex(
            (q) => q.id === this.editingQuizId
          );
          if (index !== -1) {
            this.quizzes[index] = { ...this.quizzes[index], ...this.form };
          }
        } else {
          const res = await axios.post(
            `http://localhost:5000/quiz/quizzes`,
            {
              ...this.form,
              chapter_id: this.localChapterId,
            },
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          this.quizzes.push(res.data);
        }
        this.modalInstance.hide();
      } catch (err) {
        console.error("Error saving quiz:", err);
      }
    },

    async deleteQuiz(id) {
      const token = localStorage.getItem("token");
      try {
        await axios.delete(`http://localhost:5000/quiz/quizzes/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.quizzes = this.quizzes.filter((q) => q.id !== id);
      } catch (err) {
        console.error("Error deleting quiz:", err);
      }
    },

    openQuestions(quiz) {
      this.$router.push({
        name: "QuestionsPage",
        params: {
          subjectId: this.localSubjectId,
          subjectName: this.localSubjectName,
          chapterId: this.localChapterId,
          chapterName: this.localChapterName,
          quizId: quiz.id,
          quizTitle: quiz.title,
        },
      });
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
.btn-outline-danger,
.btn-outline-success {
  padding: 0.4rem 1rem;
  font-size: 0.9rem;
  border-radius: 2rem;
}

.btn-success {
  background-color: #28a745;
  border-color: #28a745;
}

.btn-success:hover {
  background-color: #218838;
  border-color: #1e7e34;
}
</style>
