import { createRouter, createWebHistory } from "vue-router";
import ArticleView from "@/views/ArticleView.vue";
import DetailView from "@/views/DetailView.vue";
import CreateView from "@/views/CreateView.vue";
import SignUpView from "@/views/SignUpView.vue";
import LogInView from "@/views/LogInView.vue";
import HomeView from "@/views/HomeView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";
import FilteredMoviesView from "@/views/FilteredMoviesView.vue";
import ChartView from "@/views/ChartView.vue";
import EditArticleView from "@/views/EditArticleView.vue";
import MoviesByYearView from "@/views/MoviesByYearView.vue";
import EditProfileView from "@/views/EditProfileView.vue";
import UserProfileView from "@/views/UserProfileView.vue";
import AiChatView from "@/views/AiChatView.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/articles",
      name: "ArticleView",
      component: ArticleView,
    },
    {
      path: "/articles/:id",
      name: "DetailView",
      component: DetailView,
    },
    {
      path: "/articles/:id/edit",
      name: "EditArticle",
      component: EditArticleView,
    },
    {
      path: "/create",
      name: "CreateView",
      component: CreateView,
    },
    {
      path: "/signup",
      name: "SignUpView",
      component: SignUpView,
    },
    {
      path: "/login",
      name: "LogInView",
      component: LogInView,
    },
    {
      path: "/",
      name: "HomeView",
      component: HomeView,
    },
    {
      path: "/:movieId",
      name: "MovieDetailView",
      component: MovieDetailView,
    },
    {
      path: "/filtered-movies",
      name: "FilteredMoviesView",
      component: FilteredMoviesView,
    },
    {
      path: "/charts",
      name: "ChartView",
      component: ChartView,
    },
    {
      path: "/movies-by-year",
      name: MoviesByYearView,
      component: MoviesByYearView,
    },
    {
      path: '/profile/:id',
      name: 'UserProfileView',
      component: UserProfileView,
    },
    {
      path: '/profile/edit',
      name: 'EditProfileView',
      component: EditProfileView,
    },
    {
      path: '/aichats',
      name: 'AiChatView',
      component: AiChatView,
    },
    
  ],
});

export default router;
