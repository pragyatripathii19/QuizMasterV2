<template>
  <div class="fullpage d-flex justify-content-center align-items-center">
    <div class="card shadow-lg p-4 dashboard-card">
      <div class="card-body">
        <h2 class="text-center text-primary mb-4">Quiz Details</h2>
        <div v-if="quiz">
          <p><strong>ID:</strong> {{ quiz.id }}</p>
          <p><strong>Chapter:</strong> {{ quiz.chapter_id }}</p>
          <p><strong>Title:</strong> {{ quiz.title }}</p>
          <p><strong>Date:</strong> {{ quiz.date }}</p>
          <p><strong>Duration:</strong> {{ quiz.time_duration }}</p>
          <p><strong>Remarks:</strong> {{ quiz.remarks }}</p>

          <canvas id="quizChart"></canvas>
        </div>
        <div v-else>
          <p>Loading quiz details...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import Chart from "chart.js/auto";

export default {
  name: "QuizDetailPage",
  setup() {
    const route = useRoute();
    const quizId = route.params.id;
    const quiz = ref(null);

    onMounted(async () => {
      const token = localStorage.getItem("token");
      const res = await axios.get(
        `http://localhost:5000/quiz/details/${quizId}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      quiz.value = res.data.quiz;
      const chartData = res.data.chart;

      new Chart(document.getElementById("quizChart"), {
        type: "bar",
        data: {
          labels: chartData.labels,
          datasets: [
            {
              label: "Average Score %",
              data: chartData.data,
              backgroundColor: "rgba(75, 192, 192, 0.6)",
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
            },
          },
        },
      });
    });

    return { quiz };
  },
};
</script>

<style scoped>
.fullpage {
  height: 100vh;
  background-color: #f9f9f9;
}
.dashboard-card {
  width: 700px;
}
</style>
