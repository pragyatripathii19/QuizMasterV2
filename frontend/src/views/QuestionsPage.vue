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
            {{ chapterName }}, {{ quizId }}. {{ quizTitle }})
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
                <th style="width: 25%">Question Statement</th>
                <th style="width: 25%">Options</th>
                <th style="width: 15%">Correct Answer</th>
                <th style="width: 15%">Operations</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="questions.length === 0">
                <td colspan="5" class="text-muted">No questions added yet</td>
              </tr>
              <tr v-for="q in questions" :key="q.id">
                <td>{{ q.id }}</td>
                <td class="text-start">{{ q.question_statement }}</td>
                <td class="text-start">
                  1. {{ q.option1 }}<br />
                  2. {{ q.option2 }}<br />
                  3. {{ q.option3 }}<br />
                  4. {{ q.option4 }}
                </td>
                <td>{{ q.correct_answer }}</td>
                <td>
                  <button
                    class="btn btn-sm btn-outline-primary me-2 rounded-pill"
                    @click="editQuestion(q)"
                  >
                    Edit
                  </button>
                  <button
                    class="btn btn-sm btn-outline-danger rounded-pill"
                    @click="deleteQuestion(q.id)"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Add Question Button -->
        <div class="text-center">
          <button
            class="btn btn-success btn-lg rounded-pill w-100"
            @click="openModalForAdd"
          >
            Add Question
          </button>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div class="modal fade" id="questionModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ isEditMode ? "Edit Question" : "Add Question" }}
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="mb-2">
              <label class="form-label fw-bold">Quiz ID</label>
              <input
                type="text"
                class="form-control"
                :value="quizId"
                readonly
              />
            </div>
            <div class="mb-2">
              <label class="form-label fw-bold">Chapter ID</label>
              <input
                type="text"
                class="form-control"
                :value="chapterId"
                readonly
              />
            </div>
            <textarea
              v-model="form.question_statement"
              class="form-control mb-2"
              placeholder="Question Statement"
              rows="2"
            ></textarea>
            <input
              v-model="form.option1"
              class="form-control mb-2"
              placeholder="Option 1"
            />
            <input
              v-model="form.option2"
              class="form-control mb-2"
              placeholder="Option 2"
            />
            <input
              v-model="form.option3"
              class="form-control mb-2"
              placeholder="Option 3"
            />
            <input
              v-model="form.option4"
              class="form-control mb-2"
              placeholder="Option 4"
            />
            <input
              v-model="form.correct_answer"
              class="form-control"
              placeholder="Correct Answer"
            />
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Cancel
            </button>
            <button type="button" class="btn btn-primary" @click="saveQuestion">
              Save
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from "bootstrap";
import axios from "axios";

export default {
  name: "QuestionsPage",
  props: [
    "subjectId",
    "subjectName",
    "chapterId",
    "chapterName",
    "quizId",
    "quizTitle",
  ],
  data() {
    return {
      questions: [],
      isEditMode: false,
      editingQuestionId: null,
      form: {
        question_statement: "",
        option1: "",
        option2: "",
        option3: "",
        option4: "",
        correct_answer: "",
      },
      modalInstance: null,
    };
  },
  mounted() {
    this.fetchQuestions();
  },
  methods: {
    async fetchQuestions() {
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get(
          `http://localhost:5000/quiz/chapters/${this.chapterId}/quizzes/${this.quizId}/questions`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        this.questions = res.data;
      } catch (err) {
        console.error("Failed to fetch questions:", err);
      }
    },
    openModalForAdd() {
      this.isEditMode = false;
      this.form = {
        question_statement: "",
        option1: "",
        option2: "",
        option3: "",
        option4: "",
        correct_answer: "",
      };
      this.showModal();
    },
    editQuestion(q) {
      this.isEditMode = true;
      this.editingQuestionId = q.id;
      this.form = {
        question_statement: q.question_statement,
        option1: q.option1,
        option2: q.option2,
        option3: q.option3,
        option4: q.option4,
        correct_answer: q.correct_answer,
      };
      this.showModal();
    },
    async saveQuestion() {
      const token = localStorage.getItem("token");
      if (!this.form.question_statement.trim()) return;

      try {
        if (this.isEditMode) {
          await axios.put(
            `http://localhost:5000/quiz/questions/${this.editingQuestionId}`,
            this.form,
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
        } else {
          await axios.post(
            `http://localhost:5000/quiz/chapters/${this.chapterId}/quizzes/${this.quizId}/questions`,
            this.form,
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
        }
        this.hideModal();
        this.fetchQuestions(); // Refresh
      } catch (err) {
        console.error("Failed to save question:", err);
      }
    },
    async deleteQuestion(id) {
      const token = localStorage.getItem("token");
      if (!confirm("Are you sure you want to delete this question?")) return;

      try {
        await axios.delete(`http://localhost:5000/quiz/questions/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.fetchQuestions(); // Refresh
      } catch (err) {
        console.error("Failed to delete question:", err);
      }
    },
    showModal() {
      if (!this.modalInstance) {
        this.modalInstance = new Modal(
          document.getElementById("questionModal")
        );
      }
      this.modalInstance.show();
    },
    hideModal() {
      if (this.modalInstance) this.modalInstance.hide();
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
.btn-outline-danger {
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
