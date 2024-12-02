<script>
import axios from "axios";
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";

export default {
  setup() {
    const router = useRouter();
    const movies = ref([]); // 전체 영화 목록
    const currentPage = ref(1); // 현재 페이지
    const moviesPerPage = 24; // 한 페이지에 표시할 영화 수
    const totalPages = ref(10); // 총 페이지 수
    const apikey = import.meta.env.VITE_TMDB_API_KEY; // TMDB API 키

    // 영화 데이터 가져오기 (1~10페이지)
    const fetchMovies = async () => {
      const requests = [];
      for (let page = 1; page <= totalPages.value; page++) {
        requests.push(
          axios.get(
            `https://api.themoviedb.org/3/movie/popular?api_key=${apikey}&language=ko-KR&page=${page}`
          )
        );
      }

      try {
        const responses = await Promise.all(requests);
        movies.value = responses.flatMap((response) => response.data.results || []); // 모든 페이지 결과 병합
      } catch (error) {
        console.error("영화 데이터를 가져오는 중 오류 발생:", error);
      }
    };

    // 현재 페이지의 영화 데이터 계산
    const paginatedMovies = computed(() => {
      const start = (currentPage.value - 1) * moviesPerPage;
      const end = start + moviesPerPage;
      return movies.value.slice(start, end);
    });

    // 영화의 포스터 URL 생성
    const getMoviePoster = (posterPath) => {
      return posterPath
        ? `https://image.tmdb.org/t/p/w500${posterPath}`
        : "https://via.placeholder.com/500x750?text=No+Image"; // 이미지 없을 때 대체 이미지
    };

    // 페이지 변경
    const changePage = (direction) => {
      if (direction === "next" && currentPage.value < totalPages.value) {
        currentPage.value += 1;
      } else if (direction === "prev" && currentPage.value > 1) {
        currentPage.value -= 1;
      }
    };

    // 영화 상세 페이지로 이동
    const goDetail = (movie) => {
      router.push({ name: "MovieDetailView", params: { movieId: String(movie.id) } });
    };

    // 페이지 로드 시 영화 데이터 가져오기
    onMounted(() => {
      fetchMovies();
    });

    return {
      paginatedMovies,
      currentPage,
      totalPages,
      getMoviePoster,
      changePage,
      goDetail,
    };
  },
};
</script>

<template>
  <div>
    <br />
    <h2 style="text-align: center;">평점 순위별 영화 차트</h2>
    <hr />
    <br />

    <!-- 영화 목록 표시 -->
    <div id="movies-list" class="movies-container">
      <div
        v-for="movie in paginatedMovies"
        :key="movie.id"
        class="movie-card"
        @click="goDetail(movie)"
      >
        <img :src="getMoviePoster(movie.poster_path)" alt="movie poster" />
        <div class="movie-info">
          <h4>{{ movie.title }}</h4>
          <p>평점: {{ movie.vote_average }}</p>
        </div>
      </div>
    </div>

    <!-- 페이지네이션 -->
    <div class="pagination">
      <button
        :disabled="currentPage === 1"
        @click="changePage('prev')"
      >
        이전
      </button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button
        :disabled="currentPage === totalPages"
        @click="changePage('next')"
      >
        다음
      </button>
    </div>
  </div>
</template>

<style scoped>
h2,
h4 {
  font-family: 'NanumSquareExtraBold';
}

hr {
  background-color: #ea3e54;
  height: 5px;
  width: 50%;
  margin: 0 auto;
  border: none;
}

.movies-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.movie-card {
  width: 200px;
  border-radius: 5px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.movie-card:hover {
  transform: scale(1.05);
}

.movie-card img {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.movie-info {
  padding: 10px;
  text-align: center;
}

p {
  margin-top: 5px;
  color: gray;
  font-family: 'NanumSquareAcr';
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination button {
  padding: 10px 20px;
  margin: 0 10px;
  background-color: #ea3e54;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-family: 'NanumSquareBold';
}

.pagination button:disabled {
  background-color: gray;
  cursor: not-allowed;
}

.pagination span {
  font-family: 'NanumSquareBold';
}
</style>
