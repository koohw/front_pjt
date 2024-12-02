<script setup>
import { RouterLink, useRouter, useRoute } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import { ref, computed } from "vue";
import axios from "axios";

const store = useCounterStore();
const router = useRouter();
const route = useRoute();

const userId = computed(() => store.userProfile?.pk);

// 현재 경로가 ArticleView인지 확인
const isArticleView = computed(() => {
  return route.name === "AiChatView" || route.name === "ArticleView" || route.name === "DetailView" || route.name === "CreateView" || route.name === "EditArticleView" || route.name === "LogInView" || route.name === "SignUpView";
});

// 로그아웃 처리 함수
const handleLogOut = async () => {
  await store.logOut();
  router.push({ name: "LogInView" }); // 로그아웃 후 로그인 페이지로 이동
};

// 로그인 클릭 시 처리
const handleLoginClick = () => {
  if (store.isLogin) {
    alert("이미 로그인 되어있습니다.");
  }
};

// 검색 상태 관리
const searchQuery = ref(""); // 검색어 입력 상태
const searchResults = ref([]); // 검색 결과 저장

// 검색 핸들러
const handleSearch = async (e) => {
  e.preventDefault(); // 기본 폼 제출 동작 방지

  if (!searchQuery.value.trim()) {
    alert("영화 제목을 입력해주세요.");
    return;
  }

  try {
    const response = await axios.get(
      `https://api.themoviedb.org/3/search/movie`,
      {
        params: {
          query: searchQuery.value,
          api_key: import.meta.env.VITE_TMDB_API_KEY, // TMDB API 키
          language: "ko-KR",
        },
      }
    );

    // 검색 결과 저장
    searchResults.value = response.data.results;

    if (searchResults.value.length === 0) {
      alert("해당 제목의 영화를 찾을 수 없습니다.");
    }
  } catch (error) {
    console.error("검색 오류:", error);
    alert("영화 검색 중 오류가 발생했습니다.");
  }
};

// 영화 상세 페이지 이동 핸들러
const handleMovieClick = (movieId) => {
  searchResults.value = []; // 검색 결과 초기화
  const detailUrl = router.resolve({ name: "MovieDetailView", params: { movieId } }).href;
  window.location.href = detailUrl; // 새로고침과 함께 상세 페이지로 이동
};

</script>

<template>
  <!-- 메인 로고 포함 첫번째 navbar -->
  <div class="a">
    <nav class="navbar navbar-expand-lg" style="background-color: white;">
      <div class="container-fluid">
        <RouterLink :to="{ name: 'HomeView' }" class="nav-link text-success"
          ><img
          src="https://img.icons8.com/?size=100&id=dklqpDh7Fu1t&format=png&color=000000"
          alt="메인 아이콘"
        /></RouterLink>

        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav ms-auto">
            <!-- 로그인 버튼: 로그인하지 않은 상태에서만 보이도록 -->
            <RouterLink
              v-if="!store.isLogin"
              :to="{ name: 'SignUpView' }"
              class="nav-link"
            >
              <img
                src="https://img.icons8.com/?size=100&id=yPLLSMVy0oHZ&format=png&color=000000"
                alt="회원가입 아이콘"
                class="icon"
              />
              <span class="text">회원가입</span>
            </RouterLink>

            <RouterLink
              v-if="!store.isLogin"
              :to="{ name: 'LogInView' }"
              class="nav-link"
            >
              <img
                src="https://img.icons8.com/?size=100&id=26211&format=png&color=000000"
                alt="로그인 아이콘"
                class="icon"
              />
              <span class="text">로그인</span>
            </RouterLink>

            <!-- 로그아웃 버튼: 로그인 상태에서만 보이도록 -->
            <button
              v-if="store.isLogin"
              @click="handleLogOut"
              class="nav-link btn btn-link"
            >
              <img
                src="https://img.icons8.com/?size=100&id=24337&format=png&color=000000"
                alt="로그아웃 아이콘"
                class="icon"
              />
              <span class="text">로그아웃</span>
            </button>

            <span class="separator"></span>
            <RouterLink :to="{ name: 'ArticleView' }" class="nav-link">
              <img
                src="https://img.icons8.com/?size=100&id=11168&format=png&color=000000"
                alt="커뮤니티 아이콘"
                class="icon"
              />
              <span class="text">커뮤니티</span></RouterLink
            >
            <RouterLink v-if="userId" :to="{ name: 'UserProfileView',params: { id: userId } }" class="nav-link">
              <img
                src="https://img.icons8.com/?size=100&id=6RlaHUy2CmGh&format=png&color=000000"
                alt="커뮤니티 아이콘"
                class="icon"
              />
              <span class="text">마이페이지</span></RouterLink
            >
            <RouterLink :to="{ name: 'AiChatView' }" class="nav-link">
              <img
                src="https://img.icons8.com/?size=100&id=TaMzetXJx8tA&format=png&color=000000"
                alt="커뮤니티 아이콘"
                class="icon"
              />
              <span class="text">AI 기능</span></RouterLink
            >
          </div>
        </div>
      </div>
    </nav>
  </div>
  <hr style="color: grey;">

  <!-- 상세 페이지 이동하는 두번째 navbar -->
  <nav 
    v-if="!isArticleView"
    class="navbar navbar-expand-lg" 
    style="background-color: white;">
    <div class="container-fluid">
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink to="/charts" class="nav-link2">
                <span class="text">차트별</span>
              </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink to="/filtered-movies" class="nav-link2">
                <span class="text">장르별</span>
              </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink to="/movies-by-year" class="nav-link2">
                <span class="text">연도별</span>
              </RouterLink>
          </li>
        </ul>
        
        <!-- 검색 창 -->
        <form class="d-flex mb-3" role="search" @submit="handleSearch">
          <input
            class="form-control me-2"
            type="search"
            placeholder="ex) 대부"
            aria-label="Search"
            v-model="searchQuery"
          />
          <button class="btn btn-outline-success" type="submit">
            <img
              src="https://img.icons8.com/?size=100&id=132&format=png&color=000000"
              alt="검색 아이콘"
              style="width: 20px; height: 20px; margin-right: 5px; "
            />
          </button>
        </form>
      </div>
    </div>  
  <hr>
</nav>


<!-- 검색 결과 -->
<div v-if="searchResults.length > 0">
  <h5>검색 결과</h5>
  <br>
  <br>
  <ul class="list-group">
    <li
      v-for="movie in searchResults"
      :key="movie.id"
      class="list-group-item d-flex justify-content-between align-items-center"
    >
      <!-- 제목 클릭 시 상세 페이지 이동 -->
      <span @click="handleMovieClick(movie.id)" style="cursor: pointer;">
          {{ movie.title }} ({{ movie.release_date?.slice(0, 4) || "N/A" }})
        </span>
    </li>
  </ul>
<br>
</div>
</template>


<style scoped>
@import url("https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css");
/* 아이콘 크기와 정렬 */
.nav-link,
.nav-link2 {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: inherit; /* 텍스트 색상 상속 */
  margin-top: 10px; /* 기본 위쪽 간격 */
  font-family: 'NanumSquare';
}

/* 첫 번째 Navbar 관련 */
.nav-link {
  margin-bottom: -20px; /* 아래 간격 조정 */
}

/* 두 번째 Navbar 관련 */
.nav-link2 {
  margin-top: -25px; /* 위쪽 간격 */
  margin-left: 20px; /* 좌측 여백 */
}

.icon {
  width: 25px; /* 아이콘 너비 */
  height: 25px; /* 아이콘 높이 */
  margin-bottom: 8px; /* 텍스트와 간격 */
}

.d-flex {
  margin-top: -10px;
}

.text {
  font-size: 17px; /* 텍스트 크기 */
  font-weight: bold; /* 텍스트 굵게 */
  color: black; /* 텍스트 색상 */
  font-family: 'NanumSquare';
}

input[type="search"] {
  /* border-radius: 5px; /* 입력 창 테두리 둥글게 */
  /* border: 1px solid #ccc; 테두리 색상 */
  border: none;
  text-decoration: underline;
}

button[type="submit"] {
  font-family: 'NanumSquare';
  font-weight: bold;
  border: none;
  margin-left: -70px;
  background-color: white;
}

button[type="submit"]:hover {
  background-color: transparent; /* 배경색 제거 */
  border: none; /* 테두리 제거 */
}

/* 검색 결과 리스트 */
.list-group-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding: 10px 15px; /* 리스트 항목 여백 */
  border: 1px solid #ddd; /* 항목 테두리 */
  border-radius: 5px; /* 항목 둥근 모서리 */
  margin-bottom: 10px; /* 리스트 항목 간 간격 */
  transition: background-color 0.2s; /* 호버 애니메이션 */
  font-family: 'NanumSquareAcr';
}

.list-group-item:hover {
  background-color: #f8f9fa; /* 호버 시 배경색 */
}

h5 {
  text-align: center; 
  font-size: 30px;
  font-family: 'NanumSquareAcr';
}


</style>
