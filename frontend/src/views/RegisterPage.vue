<template>
  <div class="fullpage d-flex justify-content-center align-items-center">
    <div class="card shadow-lg p-4 card-box">
      <div class="card-body">
        <h2 class="card-title mb-3 text-success">Create Account</h2>
        <p class="card-text mb-4 text-muted">
          Register to join QuizMaster and test your knowledge!
        </p>

        <form @submit.prevent="register">
          <div class="mb-3">
            <input
              v-model="username"
              type="text"
              class="form-control form-control-lg rounded-pill"
              placeholder="Username (Email)"
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
          <div class="mb-3">
            <input
              v-model="full_name"
              type="text"
              class="form-control form-control-lg rounded-pill"
              placeholder="Full Name"
            />
          </div>
          <div class="mb-3">
            <input
              v-model="qualification"
              type="text"
              class="form-control form-control-lg rounded-pill"
              placeholder="Qualification"
            />
          </div>
          <div class="mb-3">
            <input
              v-model="dob"
              type="date"
              class="form-control form-control-lg rounded-pill"
              placeholder="Date of Birth"
            />
          </div>
          <button type="submit" class="btn btn-success w-100 rounded-pill">
            Register
          </button>
        </form>

        <p v-if="error" class="text-danger mt-3">{{ error }}</p>

        <router-link
          to="/login"
          class="d-block mt-3 text-center text-decoration-underline"
        >
          Already have an account? Login here
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RegisterPage",
  data() {
    return {
      username: "",
      password: "",
      full_name: "",
      qualification: "",
      dob: "",
      error: "",
    };
  },
  methods: {
    async register() {
      try {
        await axios.post("http://localhost:5000/auth/register", {
          username: this.username,
          password: this.password,
          full_name: this.full_name,
          qualification: this.qualification,
          dob: this.dob,
        });
        this.$router.push("/login");
      } catch (err) {
        this.error = err.response?.data?.msg || "Registration failed";
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
  overflow: hidden;
}

.card-box {
  width: 100%;
  max-width: 480px; /* Slightly bigger than 420px for register form */
  min-width: 320px; /* Prevent shrinking too much */
  border-radius: 1rem;
  background-color: #ffffff;
}

.card-title {
  font-weight: 700;
}

/* Make all inputs big and pill shaped */
.form-control {
  padding: 0.75rem 1.25rem;
  font-size: 1rem;
  border-radius: 2rem;
}

/* Specifically target date inputs to make them larger */
input[type="date"].form-control {
  height: 3.2rem;
  font-size: 1.1rem;
  padding: 0.75rem 1.25rem;
}

/* Button styling */
.btn-success {
  background-color: #28a745;
  border-color: #28a745;
}

.btn-success:hover {
  background-color: #218838;
  border-color: #1e7e34;
}

/* Link styling */
.text-decoration-underline {
  text-decoration: underline;
  color: #28a745;
}

.text-decoration-underline:hover {
  text-decoration: none;
  color: #1e7e34;
}
</style>
