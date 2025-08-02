<template>
  <div class="fullpage d-flex justify-content-center align-items-center">
    <div class="card shadow-lg p-4 dashboard-card">
      <div class="card-body">
        <!-- Heading -->
        <div class="text-center mb-4">
          <h1 class="display-5 fw-bold text-primary">QuizMaster</h1>
          <p class="lead text-muted">Admin Dashboard</p>
        </div>

        <!-- Search Filter -->
        <div class="mb-4 row">
          <div class="col-md-4">
            <select v-model="searchFilter" class="form-select">
              <option value="">Select Filter</option>
              <option value="users">Users</option>
              <option value="subjects">Subjects</option>
              <option value="quizzes">Quizzes</option>
            </select>
          </div>
          <div class="col-md-6">
            <input
              type="text"
              v-model="searchQuery"
              class="form-control"
              placeholder="Enter your search term"
            />
          </div>
          <div class="col-md-2">
            <button class="btn btn-primary w-100" @click="performSearch">
              Search
            </button>
          </div>
        </div>

        <!-- Search Results -->
        <div v-if="searchResults.length > 0">
          <h5 class="mb-3">Search Results</h5>
          <ul class="list-group mb-4">
            <li
              v-for="item in searchResults"
              :key="item.id"
              class="list-group-item list-group-item-action"
              @click="selectItem(item)"
              style="cursor: pointer"
            >
              {{ displayItem(item) }}
            </li>
          </ul>
        </div>

        <!-- Details and Charts -->
        <div v-if="selectedItem">
          <div class="mb-4">
            <h5>Details</h5>
            <div v-if="searchFilter === 'users'">
              <p><strong>ID:</strong> {{ selectedItem.id }}</p>
              <p><strong>Username:</strong> {{ selectedItem.username }}</p>
              <p><strong>Full Name:</strong> {{ selectedItem.full_name }}</p>
              <p>
                <strong>Qualification:</strong> {{ selectedItem.qualification }}
              </p>
              <p><strong>DOB:</strong> {{ selectedItem.dob }}</p>
              <canvas id="userLineChart"></canvas>
            </div>
            <div v-else-if="searchFilter === 'quizzes'">
              <canvas id="quizBarChart"></canvas>
            </div>
            <div v-else-if="searchFilter === 'subjects'">
              <canvas id="subjectBarChart"></canvas>
            </div>
          </div>
        </div>

        <!-- Table -->
        <div class="table-responsive mb-4">
          <table
            class="table table-bordered table-hover text-center align-middle"
          >
            <thead class="table-dark">
              <tr>
                <th style="width: 10%">S.No</th>
                <th style="width: 40%">Subject Name</th>
                <th style="width: 30%">Description</th>
                <th style="width: 20%">Operations</th>
              </tr>
            </thead>
            <tbody>
              <!-- Show message when no subjects -->
              <tr v-if="subjects.length === 0">
                <td colspan="4" class="text-muted">No subjects added yet</td>
              </tr>

              <!-- Loop over subjects -->
              <tr v-for="(subject, index) in subjects" :key="subject.id">
                <td>{{ index + 1 }}</td>
                <td>{{ subject.name }}</td>
                <td>{{ subject.description }}</td>
                <td>
                  <!-- Edit Button -->
                  <button
                    class="btn btn-sm btn-outline-primary me-2 rounded-pill"
                    @click="editSubject(subject)"
                  >
                    Edit
                  </button>

                  <!-- Delete Button -->
                  <button
                    class="btn btn-sm btn-outline-danger me-2 rounded-pill"
                    @click="deleteSubject(subject.id)"
                  >
                    Delete
                  </button>

                  <!-- Open Button -->
                  <button
                    class="btn btn-sm btn-outline-success rounded-pill"
                    @click="openChapters(subject)"
                  >
                    Open
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Add Button -->
        <div class="text-center">
          <button
            class="btn btn-success btn-lg rounded-pill w-100"
            @click="openModalForAdd"
          >
            Add Subject
          </button>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div class="modal fade" id="subjectModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ isEditMode ? "Edit Subject" : "Add Subject" }}
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
              v-model="form.name"
              class="form-control mb-3"
              placeholder="Subject Name"
            />
            <textarea
              v-model="form.description"
              class="form-control"
              placeholder="Description"
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
            <button type="button" class="btn btn-primary" @click="saveSubject">
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
import Chart from "chart.js/auto";

export default {
  name: "AdminDashboard",
  data() {
    return {
      subjects: [],
      isEditMode: false,
      editingSubjectId: null,
      chartInstance: null,
      form: {
        name: "",
        description: "",
      },
      modalInstance: null,
      searchFilter: "",
      searchQuery: "",
      searchResults: [],
      selectedItem: null,
    };
  },
  mounted() {
    this.fetchSubjects();
    this.modalInstance = new Modal(document.getElementById("subjectModal"));
  },
  methods: {
    async performSearch() {
      if (!this.searchFilter || !this.searchQuery) return;
      const token = localStorage.getItem("token");
      try {
        const res = await axios.get(`http://localhost:5000/quiz/search`, {
          params: {
            type: this.searchFilter,
            q: this.searchQuery,
          },
          headers: {
            Authorization: `Bearer ${token}`,
          },
          withCredentials: true,
        });
        this.searchResults = res.data;
        this.selectedItem = null;
      } catch (error) {
        console.error("Search failed:", error);
      }
    },
    async selectItem(item) {
      this.selectedItem = item;
      const token = localStorage.getItem("token");

      if (this.searchFilter === "users") {
        const res = await axios.get(
          `http://localhost:5000/quiz/user/${item.id}/scores`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        const timestamps = res.data.map((s) => s.time_stamp_of_attempt);
        const scores = res.data.map((s) => s.percentage);

        // Destroy previous chart if it exists
        if (this.chartInstance) {
          this.chartInstance.destroy();
        }

        // Wait for DOM to update before accessing canvas
        this.$nextTick(() => {
          const ctx = document.getElementById("userLineChart");
          if (ctx) {
            this.chartInstance = new Chart(ctx, {
              type: "line",
              data: {
                labels: timestamps,
                datasets: [
                  {
                    label: "Score %",
                    data: scores,
                    borderColor: "blue",
                    fill: false,
                  },
                ],
              },
            });
          }
        });
      }

      if (this.searchFilter === "quizzes") {
        const res = await axios.get(
          `http://localhost:5000/quiz/details/${item.id}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        new Chart(document.getElementById("quizBarChart"), {
          type: "bar",
          data: {
            labels: res.data.chart.labels,
            datasets: [
              {
                label: "Average Score",
                data: res.data.chart.data,
                backgroundColor: "orange",
              },
            ],
          },
        });
      }
      if (this.searchFilter === "subjects") {
        const res = await axios.get(
          `http://localhost:5000/quiz/subject-stats/${item.id}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        new Chart(document.getElementById("subjectBarChart"), {
          type: "bar",
          data: {
            labels: res.data.chart.labels,
            datasets: [
              {
                label: "Average Score",
                data: res.data.chart.data,
                backgroundColor: "green",
              },
            ],
          },
        });
      }
    },
    displayItem(item) {
      if (this.searchFilter === "users") return item.username;
      if (this.searchFilter === "quizzes") return item.title;
      if (this.searchFilter === "subjects") return item.name;
      return "";
    },
    async fetchSubjects() {
      try {
        const token = localStorage.getItem("token");
        const res = await axios.get("http://localhost:5000/quiz/subjects", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.subjects = res.data;
      } catch (err) {
        console.error("Error fetching subjects:", err);
      }
    },
    openModalForAdd() {
      this.isEditMode = false;
      this.form = { name: "", description: "" };
      this.showModal();
    },
    editSubject(subject) {
      this.isEditMode = true;
      this.editingSubjectId = subject.id;
      this.form = {
        name: subject.name,
        description: subject.description || "",
      };
      this.showModal();
    },
    async saveSubject() {
      const token = localStorage.getItem("token");
      try {
        if (this.isEditMode) {
          await axios.put(
            `http://localhost:5000/quiz/subjects/${this.editingSubjectId}`,
            {
              name: this.form.name,
              description: this.form.description,
            },
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          const index = this.subjects.findIndex(
            (s) => s.id === this.editingSubjectId
          );
          if (index !== -1) {
            this.subjects[index].name = this.form.name;
            this.subjects[index].description = this.form.description;
          }
        } else {
          const res = await axios.post(
            "http://localhost:5000/quiz/subjects",
            {
              name: this.form.name,
              description: this.form.description,
            },
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          this.subjects.push(res.data);
        }
        this.hideModal();
      } catch (err) {
        console.error("Error saving subject:", err);
      }
    },
    async deleteSubject(id) {
      const token = localStorage.getItem("token");
      try {
        await axios.delete(`http://localhost:5000/quiz/subjects/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.subjects = this.subjects.filter((s) => s.id !== id);
      } catch (err) {
        console.error("Error deleting subject:", err);
      }
    },
    openChapters(subject) {
      this.$router.push({
        name: "ChaptersPage",
        params: { id: subject.id, name: subject.name },
      });
    },
    showModal() {
      if (!this.modalInstance) {
        this.modalInstance = new Modal(document.getElementById("subjectModal"));
      }
      this.modalInstance.show();
    },
    hideModal() {
      if (this.modalInstance) this.modalInstance.hide();
    },
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.fetchSubjects();
    });
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
