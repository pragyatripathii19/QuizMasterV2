<template>
  <div class="fullpage d-flex justify-content-center align-items-center">
    <div class="card shadow-lg p-4 dashboard-card">
      <div class="card-body">
        <div class="text-center mb-4">
          <h1 class="display-5 fw-bold text-primary">QuizMaster</h1>
          <p class="lead text-muted">Admin Dashboard</p>
          <p class="fw-semibold text-dark">
            {{ subjectId }}. {{ subjectName }}
          </p>
        </div>

        <div class="table-responsive mb-4">
          <table
            class="table table-bordered table-hover text-center align-middle"
          >
            <thead class="table-dark">
              <tr>
                <th style="width: 10%">ID</th>
                <th style="width: 30%">Name</th>
                <th style="width: 40%">Description</th>
                <th style="width: 20%">Operations</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="chapters.length === 0">
                <td colspan="4" class="text-muted">No chapters added yet</td>
              </tr>
              <tr v-for="chapter in chapters" :key="chapter.id">
                <td>{{ chapter.id }}</td>
                <td>{{ chapter.name }}</td>
                <td>{{ chapter.description }}</td>
                <td>
                  <button
                    class="btn btn-sm btn-outline-primary me-2 rounded-pill"
                    @click="editChapter(chapter)"
                  >
                    Edit
                  </button>
                  <button
                    class="btn btn-sm btn-outline-danger me-2 rounded-pill"
                    @click="deleteChapter(chapter.id)"
                  >
                    Delete
                  </button>
                  <button
                    class="btn btn-sm btn-outline-success rounded-pill"
                    @click="openQuizzesPage(chapter)"
                  >
                    Open
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="text-center">
          <button
            class="btn btn-success btn-lg rounded-pill w-100"
            @click="openModalForAdd"
          >
            Add Chapter
          </button>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div class="modal fade" id="chapterModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ isEditMode ? "Edit Chapter" : "Add Chapter" }}
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
              placeholder="Chapter Name"
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
            <button type="button" class="btn btn-primary" @click="saveChapter">
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
  name: "ChaptersPage",
  props: ["id", "name"],
  data() {
    return {
      subjectId: null,
      subjectName: null,
      chapters: [],
      isEditMode: false,
      editingChapterId: null,
      form: { name: "", description: "" },
      modalInstance: null,
    };
  },

  mounted() {
    this.modalInstance = new Modal(document.getElementById("chapterModal"));

    // Fallback for direct page load or browser refresh
    this.subjectId = this.$route.params.id;
    this.subjectName = this.$route.params.name;

    if (this.subjectId) {
      this.fetchChapters();
    }
  },

  watch: {
    // Handles browser navigation (back/forward)
    $route(to) {
      this.subjectId = to.params.id;
      this.subjectName = to.params.name;
      if (this.subjectId) {
        this.fetchChapters();
      }
    },
  },

  methods: {
    async fetchChapters() {
      const token = localStorage.getItem("token");
      try {
        console.log("Fetching chapters for subject ID:", this.subjectId); // For debugging
        const res = await axios.get(
          `http://localhost:5000/quiz/subjects/${this.subjectId}/chapters`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        this.chapters = res.data;
      } catch (err) {
        console.error("Error fetching chapters:", err);
      }
    },

    openModalForAdd() {
      this.isEditMode = false;
      this.form = { name: "", description: "" };
      this.modalInstance.show();
    },

    editChapter(chapter) {
      this.isEditMode = true;
      this.editingChapterId = chapter.id;
      this.form = { name: chapter.name, description: chapter.description };
      this.modalInstance.show();
    },

    async saveChapter() {
      const token = localStorage.getItem("token");
      try {
        if (this.isEditMode) {
          await axios.put(
            `http://localhost:5000/quiz/chapters/${this.editingChapterId}`,
            this.form,
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          const index = this.chapters.findIndex(
            (c) => c.id === this.editingChapterId
          );
          if (index !== -1) {
            this.chapters[index] = { ...this.chapters[index], ...this.form };
          }
        } else {
          const res = await axios.post(
            `http://localhost:5000/quiz/chapters`,
            {
              ...this.form,
              subject_id: this.subjectId,
            },
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          this.chapters.push(res.data);
        }
        this.modalInstance.hide();
      } catch (err) {
        console.error("Error saving chapter:", err);
      }
    },

    async deleteChapter(id) {
      const token = localStorage.getItem("token");
      try {
        await axios.delete(`http://localhost:5000/quiz/chapters/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.chapters = this.chapters.filter((c) => c.id !== id);
      } catch (err) {
        console.error("Error deleting chapter:", err);
      }
    },

    openQuizzesPage(chapter) {
      this.$router.push({
        name: "QuizzesPage",
        params: {
          subjectId: this.subjectId,
          subjectName: this.subjectName,
          chapterId: chapter.id,
          chapterName: chapter.name,
        },
      });
    },
  },

  beforeRouteEnter(to, _, next) {
    next((vm) => {
      vm.subjectId = to.params.id;
      vm.subjectName = to.params.name;
      if (vm.subjectId) {
        vm.fetchChapters();
      }
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
