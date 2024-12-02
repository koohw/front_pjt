<template>
  <div>
    <br>
    <h2 style="text-align: center;">영화 장르 선택</h2>
    <hr>
    <br>
    <!-- 장르 선택 드롭다운 -->
    <div style="text-align: right;">
      <select id="genre-select" v-model="selectedGenre">
        <option value="">All Genre</option>
        <option
          v-for="genre in genres"
          :key="genre.id"
          :value="genre.id"
        >
          {{ genre.name }}
        </option>
      </select>
    </div>

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
      movies: [], // 전체 영화 목록
      genres: [], // 영화 장르 목록
      apikey: import.meta.env.VITE_TMDB_API_KEY, // TMDB API 키
      selectedGenre: "", // 선택된 장르
      currentPage: 1, // 현재 페이지
      moviesPerPage: 24, // 한 페이지당 영화 개수
      totalPages: 10, // 총 페이지 수
    };
  },
  computed: {
    // 현재 페이지의 영화 데이터
    paginatedMovies() {
      const start = (this.currentPage - 1) * this.moviesPerPage;
      const end = start + this.moviesPerPage;
      return this.movies.slice(start, end);
    },
  },
  methods: {
    // TMDB에서 장르 목록 가져오기
    async fetchGenres() {
      try {
        const response = await axios.get(
          `https://api.themoviedb.org/3/genre/movie/list?api_key=${this.apikey}&language=ko-KR`
        );
        this.genres = response.data.genres || [];
      } catch (error) {
        console.error("장르 정보를 가져오는 중 오류 발생:", error);
      }
    },

    // 선택된 장르에 따라 영화 목록 가져오기 (1~10페이지)
    async fetchFilteredMovies() {
      const genreParam = this.selectedGenre ? `&with_genres=${this.selectedGenre}` : "";

      // 1부터 10페이지까지의 데이터를 병렬로 가져오기
      const requests = [];
      for (let page = 1; page <= this.totalPages; page++) {
        requests.push(
          axios.get(
            `https://api.themoviedb.org/3/discover/movie?api_key=${this.apikey}&language=ko-KR&page=${page}${genreParam}`
          )
        );
      }

      try {
        const responses = await Promise.all(requests);

        // 모든 페이지의 결과를 합침
        this.movies = responses.flatMap((response) => response.data.results || []);
      } catch (error) {
        console.error("영화 데이터를 가져오는 중 오류 발생:", error);
      }
    },

    // 영화 포스터 URL 생성
    getMoviePoster(posterPath) {
      return posterPath
        ? `https://image.tmdb.org/t/p/w500${posterPath}`
        : "https://via.placeholder.com/500x750?text=No+Image"; // 이미지 없을 때 대체 이미지
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
  watch: {
    // 선택된 장르 변경 시 영화 목록 업데이트
    selectedGenre() {
      this.currentPage = 1; // 선택된 장르가 바뀌면 첫 페이지로 이동
      this.fetchFilteredMovies();
    },
  },
  mounted() {
    this.fetchGenres(); // 페이지 로드 시 장르 가져오기
    this.fetchFilteredMovies(); // 페이지 로드 시 기본 영화 목록 가져오기
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

h5 {
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'NanumSquareExtraBold';
}

option {
  font-family: 'NanumSquareBold';
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

#genre-select {
  padding: 5px;
  font-size: 15px;
  margin-bottom: 20px;
}
</style>
