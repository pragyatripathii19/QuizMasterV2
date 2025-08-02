<template>
  <div class="fullpage d-flex justify-content-center align-items-center">
    <div class="card shadow-lg p-4 card-box">
      <div class="card-body">
        <h2 class="card-title mb-3 text-primary">Welcome Back!</h2>
        <p class="card-text mb-4 text-muted">
          Please log in to continue to QuizMaster.
        </p>

        <form @submit.prevent="login">
          <div class="mb-3">
            <input
              v-model="username"
              class="form-control form-control-lg rounded-pill"
              placeholder="Username"
              required
            />
          </div>
          <div class="mb-3">
            <input
              v-model="password"
              type="password"
              class="form-control form-control-lg rounded-pill"
              placeholder="Password"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary w-100 rounded-pill">
            Login
          </button>
        </form>

        <p v-if="error" class="text-danger mt-3">{{ error }}</p>

        <router-link
          to="/register"
          class="d-block mt-3 text-center text-decoration-underline"
        >
          Don't have an account? Register here
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
      error: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://localhost:5000/auth/login", {
          username: this.username,
          password: this.password,
        });

        localStorage.setItem("token", response.data.access_token);
        localStorage.setItem(
          "is_admin",
          response.data.is_admin ? "true" : "false"
        );

        if (response.data.is_admin) {
          this.$router.push("/admin-dashboard");
        } else {
          this.$router.push("/user-dashboard");
        }
      } catch (err) {
        this.error = err.response?.data?.msg || "Login failed";
      }
    },
  },
};
</script>

<style scoped>
.fullpage {
  height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #f6d365, #fda085);
}

.card-box {
  width: 100%;
  max-width: 420px;
  border-radius: 1rem;
  background-color: #ffffff;
}

.card-title {
  font-weight: 700;
}

.form-control {
  padding: 0.75rem 1rem;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0069d9;
  border-color: #0062cc;
}

.text-decoration-underline {
  text-decoration: underline;
  color: #007bff;
}

.text-decoration-underline:hover {
  text-decoration: none;
  color: #0056b3;
}
</style>
