<template>
  <div class="container py-5">
    <div v-if="!quizFinished" class="card shadow p-4">
      <h2 class="mb-3 text-primary">{{ quizTitle }}</h2>
      <p><strong>Time Left:</strong> {{ formattedTime }}</p>

      <div v-if="currentQuestion">
        <h5>
          Q{{ currentQuestionIndex + 1 }}:
          {{ currentQuestion.question_statement }}
        </h5>

        <div v-for="option in options" :key="option" class="form-check">
          <input
            class="form-check-input"
            type="radio"
            :id="option"
            :value="option"
            v-model="userAnswers[currentQuestion.id]"
          />
          <label class="form-check-label" :for="option">
            {{ option }}
          </label>
        </div>
      </div>

      <div class="mt-3 d-flex justify-content-between">
        <button
          class="btn btn-secondary"
          :disabled="currentQuestionIndex === 0"
          @click="prevQuestion"
        >
          Previous
        </button>
        <button
          class="btn btn-secondary"
          :disabled="currentQuestionIndex === questions.length - 1"
          @click="nextQuestion"
        >
          Next
        </button>
        <button class="btn btn-success" @click="submitQuiz">Submit</button>
      </div>
    </div>

    <div v-else class="text-center">
      <h2 class="text-success">Quiz Submitted!</h2>
      <p><strong>Your Score:</strong> {{ score.correct }}/{{ score.total }}</p>
      <router-link class="btn btn-primary mt-3" to="/user-dashboard"
        >Back to Dashboard</router-link
      >
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TakeQuizPage",
  props: ["quizId"],
  data() {
    return {
      questions: [],
      quizTitle: "",
      duration: 0, // in seconds
      timer: null,
      timeLeft: 0,
      currentQuestionIndex: 0,
      userAnswers: {}, // { question_id: selected_option }
      quizFinished: false,
      score: {
        correct: 0,
        total: 0,
      },
    };
  },
  computed: {
    currentQuestion() {
      return this.questions[this.currentQuestionIndex];
    },
    options() {
      return this.currentQuestion
        ? [
            this.currentQuestion.option1,
            this.currentQuestion.option2,
            this.currentQuestion.option3,
            this.currentQuestion.option4,
          ]
        : [];
    },
    formattedTime() {
      const mins = Math.floor(this.timeLeft / 60)
        .toString()
        .padStart(2, "0");
      const secs = (this.timeLeft % 60).toString().padStart(2, "0");
      return `${mins}:${secs}`;
    },
  },
  methods: {
    async fetchQuizData() {
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get(
          `http://localhost:5000/quiz/quizzes/${this.quizId}/questions`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        this.questions = res.data.questions;
        this.quizTitle = res.data.quiz_title || "Untitled Quiz";

        const [mins, secs] = res.data.duration.split(":").map(Number);
        this.duration = mins * 60 + secs;
        this.timeLeft = this.duration;

        this.startTimer();
      } catch (error) {
        console.error("Failed to fetch quiz:", error);
        alert("Could not load quiz. Please try again.");
      }
    },
    startTimer() {
      this.timer = setInterval(() => {
        this.timeLeft--;
        if (this.timeLeft <= 0) {
          clearInterval(this.timer);
          this.submitQuiz();
        }
      }, 1000);
    },
    nextQuestion() {
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestionIndex++;
      }
    },
    prevQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--;
      }
    },
    async submitQuiz() {
      clearInterval(this.timer);

      const token = localStorage.getItem("token");
      try {
        const res = await axios.post(
          `http://localhost:5000/quiz/quizzes/${this.quizId}/submit`,
          {
            answers: Object.entries(this.userAnswers).map(
              ([question_id, selected_option]) => ({
                question_id: parseInt(question_id),
                selected_option,
              })
            ),
          },

          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.score.correct = res.data.correct;
        this.score.total = res.data.total;
        this.quizFinished = true;
      } catch (error) {
        console.error("Quiz submission failed:", error);
        alert("Could not submit quiz. Please try again.");
      }
    },
  },
  created() {
    this.fetchQuizData();
  },
  beforeUnmount() {
    clearInterval(this.timer);
  },
};
</script>

<style scoped>
.container {
  max-width: 700px;
}
.card {
  border-radius: 1rem;
}
</style>
