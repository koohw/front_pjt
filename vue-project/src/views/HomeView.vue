<script setup>
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";
import { onMounted, computed, ref } from "vue";
import axios from "axios";

const store = useCounterStore();
const router = useRouter();
const isLoading = ref(true); // 로딩 상태를 추적할 변수
const trailerUrl = ref(""); // 예고편 URL
const latestMovies = ref([]); // 최신 영화 데이터
const apikey = import.meta.env.VITE_TMDB_API_KEY; // TMDB API 키
const selectedYear = new Date().getFullYear(); // 현재 연도를 기본값으로 설정

// 영화 데이터 로드 함수
const loadMovies = async () => {
  try {
    await store.getMovies();
  } catch (err) {
    console.error("영화 데이터를 가져오는데 실패했습니다:", err);
  }
};

// 예고편 데이터 로드 함수
const loadTrailer = async () => {
  try {
    if (store.movies.results) {
      const topMovie = store.movies.results[0]; // 첫 번째 영화
      if (topMovie) {
        const youtubeOptions = {
          method: "GET",
          url: "https://www.googleapis.com/youtube/v3/search",
          params: {
            part: "snippet",
            q: `${topMovie.original_title} Official Trailer`,
            type: "video",
            key: import.meta.env.VITE_YOUTUBE_API_KEY, // 유튜브 API 키
          },
        };

        const youtubeResponse = await axios.request(youtubeOptions);
        const trailer = youtubeResponse.data.items[0]; // 첫 번째 결과
        if (trailer) {
          trailerUrl.value = `https://www.youtube.com/embed/${trailer.id.videoId}?autoplay=1&mute=1`;
        }
      }
    }
  } catch (err) {
    console.error("예고편 데이터를 가져오는데 실패했습니다:", err);
  }
};

// 최신 영화 데이터 로드 함수
const loadLatestMovies = async () => {
  try {
    const response = await axios.get(
      `https://api.themoviedb.org/3/discover/movie?api_key=${apikey}&language=ko-KR&primary_release_year=${selectedYear}&page=1`
    );
    latestMovies.value = response.data.results;
  } catch (err) {
    console.error("최신 영화를 가져오는데 실패했습니다:", err);
  }
};

// 컴포넌트 마운트 시 실행
onMounted(async () => {
  // 로딩 화면을 표시
  setTimeout(async () => {
    try {
      await loadMovies(); // 영화 데이터 로드
      await loadTrailer(); // 예고편 로드
      await loadLatestMovies(); // 최신 영화 데이터 로드
    } finally {
      isLoading.value = false; // 로딩 상태 완료
    }
  }, 500); // 0.5초 대기 후 로딩 완료 처리
});

// 평점 기준 정렬된 영화 목록 계산
const sortedMovies = computed(() => {
  const movies = store.movies.results || [];
  return movies.sort((a, b) => b.vote_average - a.vote_average).slice(0, 50); // 상위 50개 영화만
});

// 한 페이지에 표시할 영화 수
const moviesPerPage = 5;

// 페이지 단위로 나누기
const paginatedMovies = computed(() => {
  const pages = [];
  for (let i = 0; i < sortedMovies.value.length; i += moviesPerPage) {
    pages.push(sortedMovies.value.slice(i, i + moviesPerPage));
  }
  return pages;
});

// 영화 상세 페이지로 이동
const goDetail = (movie) => {
  router.push(`/${movie.id}`);
};
</script>


<template>
  <!-- 로딩 상태 체크 -->
  <div v-if="isLoading" class="loading-screen">
      <!-- <img 
        src="https://img.icons8.com/?size=100&id=dklqpDh7Fu1t&format=png&color=000000" 
        alt="logo"> -->
      <h1>Welcome!</h1>
      <div class="spinner"></div>
    </div>
  <div>
    <!-- 예고편 배너 -->
    <div v-if="trailerUrl" class="trailer-banner">
      <div class="text-overlay">
        <h1 style="color:white; text-shadow: 4px 4px 6px rgba(0, 0, 0, 0.7);">쇼생크 탈출</h1>
        <p>촉망받는 은행 간부 앤디 듀프레인은 아내와 그녀의 정부를 살해했다는 누명을 쓰게 되는데...</p>
        <div class="buttons" style="text-shadow: 4px 4px 6px rgba(0, 0, 0, 0.7);">
          <a href="https://www.youtube.com/watch?v=PLl99DlL6b4&t=1s">
            <button class="play-button">▶ 예고편 보기</button>
          </a>
        </div>
      </div>
      <!-- 예고편 재생 -->
      <iframe
        :src="trailerUrl"
        title="Official Trailer"
        frameborder="0"
        allow="autoplay; fullscreen; encrypted-media; gyroscope; accelerometer"
        allowfullscreen
      ></iframe>
    </div>

    <!-- 로딩 상태 체크 -->
    <div v-if="isLoading" class="text-center">
      <p>영화 데이터를 불러오는 중...</p>
    </div>

    <!-- 영화 데이터가 로드되면 표시 -->
    <div v-else>
      <h1 class="text-center my-4">무비 차트</h1>

      <!-- 캐러셀 -->
      <div
        id="movieCarousel"
        class="carousel slide carousel-fade"
        data-bs-ride="carousel"
        style="width: 100%; max-width: 1400px; margin: 0 auto;"
      >
        <div class="carousel-inner">
          <!-- 페이지 단위로 렌더링 -->
          <div
            class="carousel-item"
            :class="{ active: index === 0 }"
            v-for="(movies, index) in paginatedMovies"
            :key="index"
          >
            <div class="row row-cols-5 g-4">
              <!-- 페이지 내의 영화 카드 -->
              <div
                class="col"
                v-for="(movie, movieIndex) in movies"
                :key="movie.id"
                @click="goDetail(movie)"
                style="cursor: pointer"
              >
                <div class="card">
                  <div class="position-relative">
                    <img
                      :src="`https://image.tmdb.org/t/p/w500${movie.backdrop_path}`"
                      class="card-img-top"
                      alt="movie poster"
                    />
                    <div class="ranking-badge">
                      {{ index * moviesPerPage + movieIndex + 1 }}
                    </div>
                  </div>
                </div>
                <div class="card-body" style="margin-top: 15px;">
                  <h5 class="card-title text-truncate">{{ movie.title }}</h5>
                  <p class="text-muted">
                    <img 
                      src="https://img.icons8.com/?size=100&id=bPUk4fjTpwMV&format=png&color=000000" 
                      alt="score_img"
                      style="width:15px; margin-right: 5px;">평점: {{ movie.vote_average }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- 캐러셀 화살표 -->
        <button
          class="carousel-btn prev-btn"
          type="button"
          data-bs-target="#movieCarousel"
          data-bs-slide="prev"
        >
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button
          class="carousel-btn next-btn"
          type="button"
          data-bs-target="#movieCarousel"
          data-bs-slide="next"
        >
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>

      <br>
      <!-- 두번째 캐러셀 -->
      <div>
        <!-- 기존 캐러셀 아래에 새 캐러셀 추가 -->
        <h1 class="text-center my-4">최신 영화</h1>
        <div
          class="scrollable-carousel"
          style="display: flex; overflow-x: auto; gap: 20px; scroll-snap-type: x mandatory; width: 100%; max-width: 1400px; margin: 0 auto;"
        >
          <div
            v-for="movie in latestMovies"
            :key="movie.id"
            class="scroll-card"
            style="scroll-snap-align: start; flex: 0 0 auto; cursor: pointer; width: 400px; transition: transform 0.3s ease, box-shadow 0.3s;"
            @click="goDetail(movie)"
          >
            <div class="card" style="height: 250px">
              <img
                :src="`https://image.tmdb.org/t/p/w500${movie.backdrop_path}`"
                class="card-img-top"
                alt="movie poster"
                style="height: 250px; object-fit: cover; border-radius: 10px; "
              />
            </div>
            <div class="card-body" style="margin-top:15px;">
              <h5 class="card-title text-truncate">{{ movie.title }}</h5>
              <p>개봉일: {{ movie.release_date }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <br>
  <br>
</template>


<style scoped>
    @import url("https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css");
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

/* 예고편 배너 스타일 */
/* 로딩 화면 스타일 */
.loading-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* background: linear-gradient(to right, #FFAFBD, #ffc3a0); */
  background: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 2rem;
  font-family: "Pacifico", cursive;
  z-index: 9999;
}

.spinner {
  margin-top: 10px;
  border: 2px solid transparent; /* 배경 색상 */
  border-top: 10px solid #ea3e54; /* 회전하는 부분 색상 */
  border-radius: 50%;
  width: 60px;
  height: 60px;
  animation: spin 2s linear infinite; /* 2초마다 회전 */
  margin-bottom: 20px;
}

/* 회전 애니메이션 */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-screen h1 {
  color: black;
  font-size: 4rem;
  margin: 20px 0; /* 상하 여백 추가 */
  font-family: "Pacifico", cursive;
}

.trailer-banner {
  position: relative;
  width: 100%;
  height: 0; /* 초기 높이를 제거 */
  padding-top: 56.25%; /* 16:9 비율 (9 / 16 * 100) */
  margin-bottom: 20px;
  overflow: hidden;
  background-color: #000;
}

.trailer-banner iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover; /* 비율 유지하며 부모 요소 크기에 맞게 설정 */
  pointer-events: none; /* 클릭 방지 */
}


/* 텍스트 오버레이 스타일 */
.text-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  text-align: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 1; /* 텍스트가 영상 위로 보이게 설정 */
  font-family: 'NanumSquareExtraBold';
}

.text-overlay h3 {
  font-size: 3rem;
  font-weight: bold;
  margin: 0;
}

.text-overlay p {
  font-size: 1.5rem;
  margin-top: 10px;
}

.buttons button {
  font-size: 1.2rem;
  background-color: rgba(255, 255, 255, 0.7);
  color: #000;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
}

.buttons button:hover {
  background-color: rgba(255, 255, 255, 1);
}

/* 호버 시 배경 흐림 해제 */
.trailer-banner:hover iframe {
  filter: blur(8px); /* 커서를 올렸을 때 흐림 해제 */
}

.trailer-banner:hover .text-overlay {
  opacity: 1; /* 텍스트 표시 */
}

/* 커서를 배너에서 뗐을 때 */
.trailer-banner:not(:hover) iframe {
  filter: none; /* 블러 해제 */
}

.trailer-banner:not(:hover) .text-overlay {
  opacity: 0; /* 텍스트 숨기기 */
}

h5 {
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'NanumSquareBold';
}

p {
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'NanumSquareAcr';
}

h1 {
  color: black;
  font-weight: bold;
  font-family: 'NanumSquareExtraBold';
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.4), 0 0 25px rgba(255, 255, 255, 0.6);
}


.card-img-top {
  height: 270px;
  object-fit: cover;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  transition: transform 0.3s ease;
}

.card {
  cursor: pointer;
  border-radius: 5px;
  border: none;
  transition: box-shadow 0.2s ease;
  /* height: 400px; 카드 전체 높이 고정 */
  display: flex;
  flex-direction: column; /* 텍스트와 이미지를 세로로 정렬 */
  justify-content: space-between; /* 이미지와 텍스트 간격 조정 */
  position: relative;
  overflow: hidden;
}

.card:hover {
  /* transform: scale(1.05); */
  box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.3);
  opacity: 0.6;
}

.card:hover .card-img-top {
  transform: scale(1.1); /* 이미지 확대 */
}

.carousel-item {
  display: flex;
  justify-content: center;
}

.carousel-inner {
  display: flex;
}

.carousel-item .row {
  margin-left: 100px;
  margin-right: 100px;
}

/* .card-body {
  height: 70px;
} */

/* .scroll-card {
  position: relative;
} */

@media (max-width: 576px) {
  .carousel-item .row {
    margin-left: 20px;
    margin-right: 20px;
  }
}

/* 순위 배지 스타일 */
.ranking-badge {
  position: absolute;
  bottom: -15px;
  left: -5px;
  color: white;
  padding: 5px 10px;
  font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
  border-radius: 80%;
  font-size: 3em;
  text-shadow: 4px 4px 6px rgba(0, 0, 0, 0.7);
}

/* 캐러셀 버튼 스타일 */
.carousel-btn {
  position: absolute;
  top: 50%;
  z-index: 10;
  background-color: rgba(255, 255, 255, 0.7);
  border: none;
  border-radius: 50%;
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.prev-btn {
  left: 40px;
}

.next-btn {
  right: 40px;
}

.carousel-control-prev-icon,
.carousel-control-next-icon {
  filter: invert(1);
}

.carousel-control-prev-icon:hover {
  filter: brightness(2.0); /* 마우스 오버 시 밝기 효과 */
}

.carousel-control-next-icon:hover {
  filter: brightness(2.0); /* 마우스 오버 시 밝기 효과 */
}


/* 두번째 캐러셀 */
.scrollable-carousel {
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
}

/* 스크롤 캐러셀에서 카드 호버 스타일 */
/* .scroll-card:hover {
  transform: scale(1);
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
} */

/* 스크롤 캐러셀 내 이미지 어두워짐 */
.scroll-card:hover .card-img-top {
  opacity: 0.3;
}
</style>
