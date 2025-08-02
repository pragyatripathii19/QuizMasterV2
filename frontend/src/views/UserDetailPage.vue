<template>
  <div class="container mt-4">
    <h2>User Details</h2>
    <p><strong>ID:</strong> {{ user.id }}</p>
    <p><strong>Username:</strong> {{ user.username }}</p>
    <p><strong>Full Name:</strong> {{ user.full_name }}</p>
    <p><strong>Qualification:</strong> {{ user.qualification }}</p>
    <p><strong>DOB:</strong> {{ user.dob }}</p>

    <canvas id="userProgressChart" width="400" height="200"></canvas>
  </div>
</template>

<script>
import axios from "axios";
import Chart from "chart.js/auto";

export default {
  name: "UserDetailPage",
  data() {
    return {
      user: {},
      scores: [],
      chartInstance: null, // store chart to destroy later if needed
    };
  },
  watch: {
    "$route.params.id": {
      immediate: true,
      handler() {
        this.fetchUserAndScores();
      },
    },
  },
  methods: {
    async fetchUserAndScores() {
      try {
        const token = localStorage.getItem("token");
        const userId = this.$route.params.id;

        // Fetch user details
        const userRes = await axios.get(
          `http://localhost:5000/quiz/user/${userId}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        this.user = userRes.data;

        // Fetch score history
        const scoresRes = await axios.get(
          `http://localhost:5000/quiz/user/${userId}/scores`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        this.scores = scoresRes.data;

        this.$nextTick(() => {
          this.renderChart();
        });
      } catch (err) {
        console.error("Error fetching user or scores:", err);
      }
    },
    renderChart() {
      try {
        const ctx = document.getElementById("userProgressChart");

        if (!ctx) {
          console.warn("Canvas element not found.");
          return;
        }

        // If an old chart exists, destroy it before rendering a new one
        if (this.chartInstance) {
          this.chartInstance.destroy();
        }
        console.log("Scores:", this.scores); // DEBUG

        const labels = this.scores.map(
          (s) => s.time_stamp_of_attempt.split("T")[0]
        );
        const data = this.scores.map((s) => parseFloat(s.percentage));

        this.chartInstance = new Chart(ctx, {
          type: "line",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Score Percentage Over Time",
                data: data,
                borderColor: "blue",
                backgroundColor: "rgba(0, 0, 255, 0.1)",
                tension: 0.3,
                fill: true,
                pointRadius: 5,
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: { display: true },
              tooltip: { enabled: true },
            },
            scales: {
              y: {
                beginAtZero: true,
                max: 100,
                title: {
                  display: true,
                  text: "Percentage",
                },
              },
              x: {
                title: {
                  display: true,
                  text: "Date",
                },
              },
            },
          },
        });
      } catch (e) {
        console.error("Chart rendering error:", e);
      }
    },
  },
};
</script>
