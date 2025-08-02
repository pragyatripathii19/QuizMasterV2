<template>
  <div class="fullpage d-flex justify-content-center align-items-center">
    <!-- Back button -->
    <div class="position-absolute top-0 start-0 m-4">
      <router-link to="/user-dashboard">
        <button class="btn btn-outline-primary">← Back to Dashboard</button>
      </router-link>
    </div>
    <div class="card shadow-lg p-4 scoreboard-card">
      <div class="card-body">
        <!-- Heading -->
        <div class="text-center mb-4">
          <h1 class="display-5 fw-bold text-primary">Scoreboard</h1>
          <p class="lead text-muted">Your quiz performance overview</p>
        </div>

        <!-- Charts -->
        <div class="row mb-5">
          <!-- Line Chart -->
          <div class="col-md-8 mb-4">
            <div class="card p-3 shadow-sm">
              <h5 class="text-center">Score % Over Time</h5>
              <canvas ref="lineChartRef"></canvas>
            </div>
          </div>

          <!-- Pie Chart -->
          <div class="col-md-4 mb-4">
            <div class="card p-3 shadow-sm">
              <h5 class="text-center">Quiz Completion Summary</h5>
              <canvas ref="pieChartRef"></canvas>
            </div>
          </div>
        </div>

        <!-- Score Table -->
        <div class="card shadow-sm p-4">
          <h5 class="text-center mb-3">Attempt History</h5>
          <div class="table-responsive">
            <table
              class="table table-bordered table-hover text-center align-middle"
            >
              <thead class="table-dark">
                <tr>
                  <th>#</th>
                  <th>Quiz ID</th>
                  <th>Attempt Time</th>
                  <th>Score</th>
                  <th>%</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="scores.length === 0">
                  <td colspan="5" class="text-muted">
                    No attempts recorded yet.
                  </td>
                </tr>
                <tr v-for="(score, index) in scores" :key="score.id">
                  <td>{{ index + 1 }}</td>
                  <td>{{ score.quiz_id }}</td>
                  <td>{{ formatDate(score.time_stamp_of_attempt) }}</td>
                  <td>{{ score.total_scored }}</td>
                  <td>{{ score.percentage }}%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  LineController,
  PieController,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  LineController,
  PieController
);

export default {
  name: "ScoreBoard",
  data() {
    return {
      scores: [],
      summary: {
        total_quizzes: 0,
        attempted_quizzes: 0,
      },
    };
  },
  mounted() {
    this.fetchScores();
    this.fetchSummary();
  },
  methods: {
    async fetchScores() {
      const token = localStorage.getItem("token");
      const res = await fetch("http://localhost:5000/quiz/user/scores", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      this.scores = data;
      this.renderLineChart(data);
    },

    async fetchSummary() {
      const token = localStorage.getItem("token");
      const res = await fetch("http://localhost:5000/quiz/user/quiz-summary", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      this.summary = data;
      this.renderPieChart(data);
    },

    renderLineChart(data) {
      const labels = data.map((score) =>
        this.formatDate(score.time_stamp_of_attempt)
      );
      const values = data.map((score) => score.percentage);

      new ChartJS(this.$refs.lineChartRef, {
        type: "line",
        data: {
          labels,
          datasets: [
            {
              label: "Score %",
              data: values,
              borderColor: "#36a2eb",
              backgroundColor: "rgba(54,162,235,0.2)",
              fill: true,
              tension: 0.3,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: "top" },
            title: { display: false },
          },
        },
      });
    },

    renderPieChart(summary) {
      const attempted = summary.attempted_quizzes;
      const remaining = summary.total_quizzes - attempted;

      new ChartJS(this.$refs.pieChartRef, {
        type: "pie",
        data: {
          labels: ["Attempted", "Remaining"],
          datasets: [
            {
              data: [attempted, remaining],
              backgroundColor: ["#4CAF50", "#ddd"],
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: "bottom" },
            title: { display: false },
          },
        },
      });
    },

    formatDate(rawDate) {
      const d = new Date(rawDate);
      return d.toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
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
.scoreboard-card {
  width: 100%;
  max-width: 1100px;
  border-radius: 1rem;
  background-color: #ffffff;
}
canvas {
  max-width: 100%;
  margin-top: 10px;
}
</style>
