<template>
  <div class="fullpage d-flex justify-content-center align-items-center">
    <div class="card shadow-lg p-4 dashboard-card">
      <div class="card-body">
        <h2 class="text-center text-primary mb-4">Subject Details</h2>
        <div v-if="subject">
          <p><strong>ID:</strong> {{ subject.id }}</p>
          <p><strong>Name:</strong> {{ subject.name }}</p>
          <p><strong>Description:</strong> {{ subject.description }}</p>

          <canvas id="subjectChart"></canvas>
        </div>
        <div v-else>
          <p>Loading subject details...</p>
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
  name: "SubjectDetailPage",
  setup() {
    const route = useRoute();
    const subjectId = route.params.id;
    const subject = ref(null);

    onMounted(async () => {
      const token = localStorage.getItem("token");
      const res = await axios.get(
        `http://localhost:5000/quiz/subject/${subjectId}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      subject.value = res.data.subject;
      const chartData = res.data.chart;

      new Chart(document.getElementById("subjectChart"), {
        type: "bar",
        data: {
          labels: chartData.labels,
          datasets: [
            {
              label: "Average Score %",
              data: chartData.data,
              backgroundColor: "rgba(153, 102, 255, 0.6)",
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

    return { subject };
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
