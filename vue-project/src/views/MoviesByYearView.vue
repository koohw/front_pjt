<template>
  <div>
    <br>
    <h2 style="text-align: center;">연도별 영화 검색</h2>
    <hr>
    <!-- 연도 입력 -->
    <div class="year-select" style="text-align: center; margin-top: 20px; margin-right: 20px;">
      <label for="year-input"></label>
      <input
        type="number"
        id="year-input"
        v-model="selectedYear"
        placeholder="ex) 2022"
        @keyup.enter="fetchMoviesByYear"
      />
      <button class="btn btn-outline-success" type="submit" @click="fetchMoviesByYear">
        <img
          src="https://img.icons8.com/?size=100&id=132&format=png&color=000000"
          alt="검색 아이콘"
          style="width: 20px; height: 20px; margin-right: 5px;"
        />
      </button>
    </div>
    <br>

    <!-- 영화 목록 -->
    <div id="movies-list" class="movies-container">
      <div
        v-for="movie in paginatedMovies"
        :key="movie.id"
        class="movie-card"
        @click="goDetail(movie.id)"
      >
        <img :src="getMoviePoster(movie.poster_path)" alt="movie poster" />
        <div class="movie-info">
          <h5>{{ movie.title }}</h5>
          <p>{{ movie.release_date }}</p>
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

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedYear: new Date().getFullYear().toString(), // 기본값: 현재 연도
      movies: [], // 전체 영화 목록
      apikey: import.meta.env.VITE_TMDB_API_KEY, // TMDB API 키
      currentPage: 1, // 현재 페이지
      moviesPerPage: 24, // 한 페이지당 영화 개수
      totalPages: 10, // 총 페이지 수
    };
  },
  computed: {
    // 현재 페이지에 표시할 영화 데이터
    paginatedMovies() {
      const start = (this.currentPage - 1) * this.moviesPerPage;
      const end = start + this.moviesPerPage;
      return this.movies.slice(start, end);
    },
  },
  methods: {
    // 연도별 영화 데이터 가져오기
    async fetchMoviesByYear() {
      const requests = [];
      for (let page = 1; page <= this.totalPages; page++) {
        requests.push(
          axios.get(
            `https://api.themoviedb.org/3/discover/movie?api_key=${this.apikey}&language=ko-KR&page=${page}&primary_release_year=${this.selectedYear}`
          )
        );
      }

      try {
        const responses = await Promise.all(requests);

        // 모든 페이지 데이터를 병합하여 movies 배열 업데이트
        this.movies = responses.flatMap((response) => response.data.results || []);
        this.currentPage = 1; // 검색 결과가 바뀌면 첫 페이지로 이동
      } catch (error) {
        console.error("영화 데이터를 가져오는 중 오류 발생:", error);
      }
    },

    // 영화 포스터 URL 생성
    getMoviePoster(posterPath) {
      return posterPath
        ? `https://image.tmdb.org/t/p/w500${posterPath}`
        : "https://via.placeholder.com/500x750?text=No+Image";
    },

    // 영화 상세 페이지로 이동
    goDetail(movieId) {
      this.$router.push({ name: "MovieDetailView", params: { movieId: String(movieId) } });
    },

    // 페이지 변경
    changePage(direction) {
      if (direction === "next" && this.currentPage < this.totalPages) {
        this.currentPage += 1;
      } else if (direction === "prev" && this.currentPage > 1) {
        this.currentPage -= 1;
      }
    },
  },
  mounted() {
    this.fetchMoviesByYear(); // 페이지 로드 시 현재 연도의 영화 목록 출력
  },
};
</script>

<style scoped>
h2 {
  font-family: 'NanumSquareExtraBold';
}

hr { 
  background-color: #ea3e54;
  height: 5px;
  width: 50%;
  margin: 0 auto; 
  border: none;
}

.year-select input {
  width: 250px;
  padding: 12px;
  font-size: 18px;
  border: 1px solid #ccc;
  border-radius: 10px;
  outline: none;
  transition: box-shadow 0.3s ease;
  font-family: 'NanumSquareBold';
  margin-right: 10px;
}
.year-select input:focus {
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
  border-color: #007bff;
}

button[type="submit"] {
  font-family: 'NanumSquare';
  font-weight: bold;
  border: none;
  margin-left: -70px;
  background-color: white;
}

button[type="submit"]:hover {
  background-color: transparent;
  border: none;
}

.movies-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  font-family: 'NanumSquareBold';
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
}

.pagination button:disabled {
  background-color: gray;
  cursor: not-allowed;
}

.pagination span {
  font-family: 'NanumSquareBold';
}
</style>
