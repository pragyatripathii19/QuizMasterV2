import { createRouter, createWebHistory } from "vue-router";

// === Page Imports ===
import LoginPage from "../views/LoginPage.vue";
import RegisterPage from "../views/RegisterPage.vue";

// User Dashboard
import UserDashboard from "../views/UserDashboard.vue";

// Admin views
import AdminDashboard from "../views/AdminDashboard.vue";
import ChaptersPage from "../views/ChaptersPage.vue";
import QuizzesPage from "../views/QuizzesPage.vue";
import QuestionsPage from "../views/QuestionsPage.vue";

// === Route Definitions ===
const routes = [
  { path: "/", redirect: "/login" },

  // Authentication routes
  { path: "/login", name: "LoginPage", component: LoginPage },
  { path: "/register", name: "RegisterPage", component: RegisterPage },

  // Admin Dashboard
  {
    path: "/admin-dashboard",
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { requiresAuth: true, requiresAdmin: true },
  },

  // User Dashboard
  {
    path: "/user-dashboard",
    name: "UserDashboard",
    component: UserDashboard,
    meta: { requiresAuth: true, requiresAdmin: false },
  },

  // Chapters under a subject
  {
    path: "/chapters/:id/:name",
    name: "ChaptersPage",
    component: ChaptersPage,
    props: true,
  },

  // Quizzes under a chapter
  {
    path: "/quizzes/:subjectId/:subjectName/:chapterId/:chapterName",
    name: "QuizzesPage",
    component: QuizzesPage,
    props: true,
  },

  // Questions under a quiz
  {
    path: "/questions/:subjectId/:subjectName/:chapterId/:chapterName/:quizId/:quizTitle",
    name: "QuestionsPage",
    component: QuestionsPage,
    props: true,
  },

  {
    path: "/quiz/:quizId/start",
    name: "TakeQuizPage",
    component: () => import("../views/TakeQuizPage.vue"),
    props: true,
    meta: { requiresAuth: true, requiresAdmin: false },
  },

  {
    path: "/scoreboard",
    name: "ScoreBoardPage",
    component: () => import("@/views/ScoreBoard.vue"),
  },

  {
    path: "/admin/user/:id",
    name: "UserDetailPage",
    component: () => import("@/views/UserDetailPage.vue"),
    props: true,
  },
  {
    path: "/admin/quiz/:id",
    name: "QuizDetailPage",
    component: () => import("@/views/QuizDetailPage.vue"),
    props: true,
  },
  {
    path: "/admin/subject/:id",
    name: "SubjectDetailPage",
    component: () => import("@/views/SubjectDetailPage.vue"),
    props: true,
  },
];

// === Create the router ===
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// === Global Navigation Guard ===
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const isAdmin = localStorage.getItem("is_admin") === "true";

  // If route requires authentication
  if (to.meta.requiresAuth) {
    if (!token) {
      return next("/login");
    }

    // Admin trying to access user-only route
    if (to.meta.requiresAdmin === false && isAdmin) {
      return next("/admin-dashboard");
    }

    // User trying to access admin-only route
    if (to.meta.requiresAdmin === true && !isAdmin) {
      return next("/user-dashboard");
    }
  }

  next();
});

export default router;
